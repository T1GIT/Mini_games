import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.basic import Movable


class Bound:
    """ An class Bound

    Library of bound interactable classes.

    Includes:
    ---------
    * BoundInteractable : parent class
    * Teleportable : teleports the sprite
    * Killable : kills the sprite
    * Stoppable : stops the sprite
    """

    class BoundInteractable(Movable):
        """ An class BoundInteractable

        Parent class for interfaces that can do something when touches edges.
        """

    class Teleportable(BoundInteractable):
        """ An interface Teleportable

        Make sprite teleport to opposite bound, when it is over the field.
        """

        def bound_teleport(self) -> None:
            """
            Checks if is sprite over the field, then teleports it into
            opposite edge, using <Teleportable.object>.bound_teleport()
            every frame.
            """
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

        def bound_kill(self) -> None:
            """ Checks if is sprite over the field, then kills it """
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

        def bound_stop(self) -> None:
            """
            Checks if every bound of the sprite isn't over field, else stops it
            (resets speed)
            """
            if not (0 + self.radius < self.rect.centerx + self.speed_x < Conf.Window.WIDTH - self.radius):
                self.speed_x = 0
            if not (0 + self.radius < self.rect.centery + self.speed_y < Conf.Window.HEIGHT - self.radius):
                self.speed_y = 0
