import pygame as pg

from sprites.interfaces.sprite import Sprite


class Locatable(Sprite):
    def __init__(self, texture: pg.Surface):
        super().__init__(texture)

    def locate(self, x, y) -> None:
        self.rect = self.image.get_rect(center=(x, y))
        self.pos_x, self.pos_y = self.rect.x, self.rect.y
