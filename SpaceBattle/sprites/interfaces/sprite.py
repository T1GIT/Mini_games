import pygame as pg


class Sprite(pg.sprite.Sprite):
    def __init__(self, texture: pg.Surface):
        super().__init__()
        self.texture: pg.Surface = texture
        self.pos_x: float = 0
        self.pos_y: float = 0
        self.image = texture
