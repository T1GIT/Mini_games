import pygame as pg

from sprites.interfaces.movable import Movable


class Rotatable(Movable):
    def __init__(self, texture: pg.Surface, speed_x: float = 0, speed_y: float = 0, angle_speed: float = 0):
        super().__init__(texture, speed_x, speed_y)
        self.angle_speed: float = angle_speed
        self.angle: float = 0

    def rotate(self) -> None:
        x_offset = self.pos_x - self.rect.x
        y_offset = self.pos_y - self.rect.y
        self.angle = (self.angle + self.angle_speed) % 360
        self.image = pg.transform.rotate(self.texture, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos_x = self.rect.x + x_offset
        self.pos_y = self.rect.y + y_offset

