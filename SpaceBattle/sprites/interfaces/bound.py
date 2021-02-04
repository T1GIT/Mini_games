from abc import ABC, abstractmethod

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.basic import Movable


class BoundInteractable(Movable, ABC):
    """ An class BoundInteractable

    Parent class for interfaces that can do something when touches edges.
    """
    @abstractmethod
    def move(self) -> None:
        pass


class Teleportable(BoundInteractable):
    """ An interface Teleportable

    Make sprite teleport to opposite bound, when it is over the field.
    """

    def move(self) -> None:
        """
        Checks if is sprite over the field, then teleports it into
        opposite edge, using <Teleportable.object>.bound_teleport()
        every frame.
        """
        Movable.move(self)
        if self.rect.right < 0:
            self.rect.left = Conf.Window.WIDTH
            self.pos_x = self.rect.centerx
        elif self.rect.left > Conf.Window.WIDTH:
            self.rect.right = 0
            self.pos_x = self.rect.centerx
        if self.rect.bottom < 0:
            self.rect.top = Conf.Window.HEIGHT
            self.pos_y = self.rect.centery
        elif self.rect.top > Conf.Window.HEIGHT:
            self.rect.bottom = 0
            self.pos_y = self.rect.centery


class Killable(BoundInteractable):
    """ An interface Killable

    Kills the sprite, if it is over the field, using
    <Killable.object>.bound_teleport() every frame.
    """
    def move(self) -> None:
        """ Checks if is sprite over the field, then kills it """
        Movable.move(self)
        if (self.rect.right < 0 or self.rect.left > Conf.Window.WIDTH
                or self.rect.bottom < 0 or self.rect.top > Conf.Window.HEIGHT):
            super().kill()


class Stopable(BoundInteractable):
    """ An interface Stopable

    Makes the sprite stop, if it is touching a bound of the field,
    using <Stopable.object>.bound_stop() every frame

    Attributes
    ----------
    radius : float
        min distance from sprite's edge to its center
    """

    def __init__(self, texture: pg.Surface, speed_x: float = 0, speed_y: float = 0):
        super().__init__(texture, speed_x, speed_y)
        self.radius: float = min(self.image.get_size()) / 2

    def move(self) -> None:
        """
        Checks if every bound of the sprite isn't over field, else stops it
        (resets speed)
        """
        Movable.move(self)
        if not (0 + self.radius < self.rect.centerx + self.speed_x < Conf.Window.WIDTH - self.radius):
            self.speed_x = 0
        if not (0 + self.radius < self.rect.centery + self.speed_y < Conf.Window.HEIGHT - self.radius):
            self.speed_y = 0
