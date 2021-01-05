from math import radians, cos, sin, hypot, atan2

import pygame as pg

from sprites.interfaces.basic import Rotatable, Movable
from sprites.player.rocket import Rocket
from utils.tools.groups import Groups
from utils.tools.timer import Timer


class Shootable(Rotatable):
    """ An interface Shootable

    Allows sprite to shoot.

    Attributes
    ----------
    shoot_radius : int
        distance from the center of the sprite to first bound of the rocket
    """
    def __init__(self, texture: pg.Surface, speed_x: float = 0, speed_y: float = 0, period: float = 0):
        super().__init__(texture, speed_x, speed_y)
        self.shoot_timer: Timer = Timer(period)
        self.shoot_radius: int = self.get_shoot_radius(texture)

    def can_shoot(self) -> bool:
        """
        Checks if the shooting timer is over.
        :return: True if the timer is over
        """
        return self.shoot_timer.is_ready()

    def shoot(self) -> None:
        """ Creates and shoot the new rocket """
        angle = -self.angle - 90
        rad = radians(angle)
        x = self.rect.centerx + self.shoot_radius * cos(rad)
        y = self.rect.centery + self.shoot_radius * sin(rad)
        rocket = Rocket()
        rocket.shoot(x, y, angle)
        rocket.add(Groups.ROCKETS, Groups.ALL)
        self.shoot_timer.start()

    def set_texture(self, texture: pg.Surface) -> None:
        """
        Overriding <Sprite.object>.set_texture with updating
        shoot_radius
        """
        super().set_texture(texture)
        self.shoot_radius = self.get_shoot_radius(texture)

    @staticmethod
    def get_shoot_radius(texture: pg.Surface) -> int:
        """
        Gets shoot_radius from the image by the closest to center
        untransparent pixel.
        :param texture: image to scan
        :return: length of the radius
        """
        mask = pg.mask.from_surface(texture)
        c_x, c_y = map(lambda x: x // 2, mask.get_size())
        alpha = 0
        for i in range(mask.get_size()[1]):
            if not mask.get_at((c_x, i)): alpha += 1
            else: break
        return c_y - alpha


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
            self.texture = self.texture_pack[1] if with_fire else self.texture_pack[0]
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