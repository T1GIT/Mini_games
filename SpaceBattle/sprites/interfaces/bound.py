import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.basic import Movable


class Bound:
    class BoundInteractable(Movable):
        pass

    class Teleportable(BoundInteractable):
        def bound_teleport(self) -> None:
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
        def bound_kill(self) -> None:
            if (self.rect.right < 0 or self.rect.left > Conf.Window.WIDTH
                    or self.rect.bottom < 0 or self.rect.top > Conf.Window.HEIGHT):
                super().kill()

    class Stopable(BoundInteractable):
        def __init__(self, texture: pg.Surface, speed_x: float = 0, speed_y: float = 0):
            super().__init__(texture, speed_x, speed_y)
            self.radius: float = min(self.image.get_size()) / 2

        def bound_stop(self) -> None:
            if not (0 + self.radius < self.rect.centerx + self.speed_x < Conf.Window.WIDTH - self.radius):
                self.speed_x = 0
            if not (0 + self.radius < self.rect.centery + self.speed_y < Conf.Window.HEIGHT - self.radius):
                self.speed_y = 0
