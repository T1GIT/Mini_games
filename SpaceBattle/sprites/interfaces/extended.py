from math import cos, sin, hypot, atan2
import random as rnd

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.basic import Rotatable, Movable, Group
from sprites.interfaces.bound import Killable


class Groupable:
    def __init__(self):
        self.group: Group = Group()

    def get_group(self) -> Group:
        return self.group


class Spawnable(Killable):
    def spawn(self) -> None:
        super().locate(*self.get_coord())

    def get_coord(self) -> tuple[float, float]:
        size = super().get_size()
        speed = super().get_speed()
        if rnd.random() > 0.5:
            x = (-size[0] / 2) if speed[0] > 0 else (Conf.Window.WIDTH + size[0] / 2)
            y = rnd.uniform(-size[1] / 2, Conf.Window.HEIGHT + size[1] / 2)
        else:
            x = rnd.uniform(-size[0] / 2, Conf.Window.WIDTH + size[0] / 2)
            y = (-size[1] / 2) if speed[1] > 0 else (Conf.Window.HEIGHT + size[1] / 2)
        return x, y


class Acceleratable(Movable):
    """ An interface Acceleratable

    Allows moving sprite consider to Physics.
    Use <Acceleratable.object>.accelerate(x, y, weight, power, resist) to
    give axel to sprite and to change axes speed.

    Attributes
    ----------
    weight : float
        abstract of the sprite
    power : float
        power of the sprite
    resist : float
        abstract resisting multiplier of the environment
    """

    def __init__(self, texture: pg.Surface, weight: float, power: float, resist: float):
        super().__init__(texture)
        self.weight = weight
        self.power = power
        self.resist = resist

    def set_power(self, power: float):
        """
        Changes value of the power
        :param power: new power value
        """
        self.power = power

    def accelerate(self, x: float, y: float):
        """
        Changes axis speed, from axel vector
        :param x: coordinate of the axel vector -1 <= x <= 1
        :param y: coordinate of the axel vector -1 <= y <= 1
        """
        assert -1 <= x <= 1 and -1 <= y <= 1
        a = Acceleratable.PhysCalc.axel(x, y, self.power)
        r = Acceleratable.PhysCalc.resist(self.speed_x, self.speed_y, self.resist)
        self.speed_x += (a[0] - r[0]) / self.weight
        self.speed_y += (a[1] - r[1]) / self.weight

    class PhysCalc:
        """ A static class for calculating physics metrics:
        for axel: PhysCalc.axel(x, y, power),
        for resist: PhysCalc.resist(speed_x, speed_y, resist)
        """
        @staticmethod
        def axel(x: float, y: float, power: float) -> tuple[float, float]:
            """
            Calculates axel by the vector coordinates
            :param x: vector coordinate
            :param y: vector coordinate
            :param power: strength
            :return: axel vector
            """
            force = min(1.0, hypot(x, y))
            rad = atan2(y, x)
            a_x = power * cos(rad) * force
            a_y = power * sin(rad) * force
            return a_x, a_y

        @staticmethod
        def resist(speed_x: float, speed_y: float, resist: float) -> tuple[float, float]:
            """
            Calculates resisting by the vector coordinates
            :param speed_x: sprite's speed on x axis
            :param speed_y: sprite's speed on y axis
            :param resist: resisting multiplier
            :return: resisting vector
            """
            speed = hypot(speed_x, speed_y)
            rad = atan2(speed_y, speed_x)
            r = resist * pow(speed, 2)
            r_x = r * cos(rad)
            r_y = r * sin(rad)
            return r_x, r_y


class AcceleratableWithFire(Acceleratable):
    """ An interface AcceleratableWithFire

    Wrap for the Acceleratable with possibility of changing
    textures when it has power and it doesn't.

    Attributes
    ----------
    texture_pack : tuple[pg.Surface, pg.Surface]
        tuple of textures: normal and with fire
    with_fire : bool
        flag, if fire texture is turned on
    """
    def __init__(self, texture_pack: tuple[pg.Surface, pg.Surface], weight: float, power: float, resist: float):
        super().__init__(texture_pack[0], weight, power, resist)
        self.texture_pack: tuple[pg.Surface, pg.Surface] = texture_pack
        self.with_fire: bool = False

    def accelerate(self, x: float, y: float) -> None:
        """
        Wrap for the <Acceleratable.object>.accelerate(x, y), changing textures

        Changes axis speed, from axel vector
        :param x: coordinate of the axel vector -1 <= x <= 1
        :param y: coordinate of the axel vector -1 <= y <= 1
        """
        self.wear_fire((x, y) != (0, 0))
        super().accelerate(x, y)

    def wear_fire(self, with_fire: bool) -> None:
        """
        Changes textures consider to with_fire
        :param with_fire: True if fire texture should be turned on
        """
        if with_fire != self.with_fire:
            self.with_fire = with_fire
            self.texture = self.texture_pack[1 if with_fire else 0]
            if isinstance(self, Rotatable):
                self.rotate()
            else:
                self.image = self.texture
            self.rect = self.image.get_rect(center=self.rect.center)

    def set_texture(self, texture_pack: tuple[pg.Surface, pg.Surface]) -> None:
        """
        Overriding <Sprite.object>.set_texture(texture), receiving tuple of textures
        :param texture_pack: new textures for 2 states
        """
        self.texture_pack = texture_pack
        super().set_texture(texture_pack[1 if self.with_fire else 0])
