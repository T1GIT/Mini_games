from abc import ABC, abstractmethod
from math import hypot, atan2, cos, sin

import pygame as pg

from config import Configuration as Conf
from utils.resources.image import Image as Img


class Sprite(pg.sprite.Sprite):
    def __init__(self, texture: pg.Surface):
        super().__init__()
        self.texture: pg.Surface = texture
        self.pos_x: float = 0
        self.pos_y: float = 0
        self.image = texture


class TextureUpdatable(Sprite, ABC):
    needs_update: bool = False

    def update_texture(self, raw_texture: pg.Surface, size: float) -> None:
        self.texture = Img.scale(raw_texture, size)
        self.image = self.texture

    @staticmethod
    @abstractmethod
    def set_texture(num: int) -> None:
        pass


class Locatable(Sprite):
    def locate(self, x, y) -> None:
        self.rect = self.image.get_rect(center=(x, y))
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y


class Movable(Locatable):
    def __init__(self, texture: pg.Surface, speed_x: float = 0, speed_y: float = 0):
        super().__init__(texture)
        self.speed_x: float = speed_x
        self.speed_y: float = speed_y

    def set_speed(self, x: float, y: float) -> None:
        self.speed_x = x
        self.speed_y = y

    def move(self) -> None:
        self.pos_x += self.speed_x * Conf.System.SCALE
        self.pos_y += self.speed_y * Conf.System.SCALE
        self.rect.x = round(self.pos_x)
        self.rect.y = round(self.pos_y)


class Acceleratable(Movable):
    def accelerate(self, x: float, y: float, weight: float, power: float, resist: float):
        """
        Changes axis speed, from axel vector
        :param x: coordinate of the axel vector
        :param y: coordinate of the axel vector
        :param weight:
        :param power:
        :param resist:
        """
        a = Acceleratable.PhysCalc.axel(x, y, power)
        r = Acceleratable.PhysCalc.resist(self.speed_x, self.speed_y, resist)
        self.speed_x += (a[0] - r[0]) / weight
        self.speed_y += (a[1] - r[1]) / weight

    class PhysCalc:
        @staticmethod
        def axel(x: float, y: float, power: float) -> tuple[float, float]:
            force = min(1.0, hypot(x, y))
            rad = atan2(y, x)
            a_x = power * cos(rad) * force
            a_y = power * sin(rad) * force
            return a_x, a_y

        @staticmethod
        def resist(speed_x: float, speed_y: float, resist: float) -> tuple[float, float]:
            speed = hypot(speed_x, speed_y)
            rad = atan2(speed_y, speed_x)
            r = resist * pow(speed, 2)
            r_x = r * cos(rad)
            r_y = r * sin(rad)
            return r_x, r_y


class Rotatable(Movable):
    def __init__(self, texture: pg.Surface, speed_x: float = 0, speed_y: float = 0):
        super().__init__(texture, speed_x, speed_y)
        self.angle: float = 0

    def rotate(self, delta_angle: float = 0, rotator: callable(float) = None) -> None:
        x_offset = self.pos_x - self.rect.x
        y_offset = self.pos_y - self.rect.y
        self.angle = (self.angle + delta_angle * Conf.System.SCALE) % 360
        if not rotator:
            def rotator(deg: int): return pg.transform.rotate(self.texture, deg)
        self.image = rotator(self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos_x = self.rect.x + x_offset
        self.pos_y = self.rect.y + y_offset


