import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.locatable import Locatable


class Movable(Locatable):
    def __init__(self, texture: pg.Surface, speed_x: float = 0, speed_y: float = 0):
        super().__init__(texture)
        self.speed_x: float = speed_x
        self.speed_y: float = speed_y

    def set_speed(self, x: float, y: float) -> None:
        self.speed_x, self.speed_y = x, y

    def move(self) -> None:
        self.pos_x += self.speed_x * Conf.System.SCALE
        self.pos_y += self.speed_y * Conf.System.SCALE
        self.rect.x = round(self.pos_x)
        self.rect.y = round(self.pos_y)
