from abc import ABC, abstractmethod
from math import radians, cos, sin

import pygame as pg

from sprites.interfaces.basic import Rotatable, Group, Sprite
from sprites.interfaces.extended import Groupable
from sprites.rockets.rocket import Rocket
from utils.tools.groups import Groups
from utils.tools.timer import Timer


class Shootable(Rotatable, Groupable, ABC):
    """ An interface Shootable

    Allows sprite to shoot.

    Attributes
    ----------
    shoot_radius : int
        distance from the center of the sprite to first bound of the rocket
    """
    def __init__(self, texture: pg.Surface, speed_x: float = 0, speed_y: float = 0, period: float = 0):
        Rotatable.__init__(self, texture, speed_x, speed_y)
        Groupable.__init__(self)
        self.shoot_timer: Timer = Timer(period)
        self.shoot_radius: int = self.get_shoot_radius(texture)

    def can_shoot(self) -> bool:
        """
        Checks if the shooting timer is over.
        :return: True if the timer is over
        """
        return self.shoot_timer.is_ready()

    @abstractmethod
    def shoot(self) -> tuple[Sprite, ...]:
        pass

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


class RocketShootable(Shootable):
    def shoot(self) -> tuple[Sprite]:
        angle = -self.angle - 90
        rad = radians(angle)
        x = self.rect.centerx + self.shoot_radius * cos(rad)
        y = self.rect.centery + self.shoot_radius * sin(rad)
        rocket = Rocket()
        rocket.run(x, y, angle)
        self.group.add(rocket)
        self.shoot_timer.start()
        return rocket,


class ThreeRocketShootable(Shootable):
    def shoot(self) -> tuple[Sprite, ...]:
        rocket_list: list[Rocket] = []
        angle = -self.angle - 90
        rad = radians(angle)
        x = self.rect.centerx + self.shoot_radius * cos(rad)
        y = self.rect.centery + self.shoot_radius * sin(rad)
        for i in range(-1, 2):
            rocket = Rocket()
            rocket_list.append(rocket)
            rocket.run(x, y, angle + 10 * i)
            self.group.add(rocket)
        self.shoot_timer.start()
        return tuple(rocket_list)
