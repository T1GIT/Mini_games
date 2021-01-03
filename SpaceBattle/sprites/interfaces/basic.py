from math import hypot, atan2, cos, sin

import pygame as pg

from config import Configuration as Conf
from utils.resources.image import Image as Img


class Sprite(pg.sprite.Sprite):
    def __init__(self, texture: pg.Surface):
        super().__init__()
        self.texture: pg.Surface = texture
        self.image = texture

    def set_texture(self, texture: pg.Surface):
        self.texture = texture
        self.image = texture


class TextureUpdatable(Sprite):
    needs_update: bool
    texture_num: int

    def update_texture(self, raw_texture: pg.Surface, size: float) -> None:
        super().set_texture(Img.scale(raw_texture, size))
        type(self).needs_update = False

    @classmethod
    def set_texture_num(cls, num: int) -> None:
        cls.texture_num = num
        cls.needs_update = True


class Locatable(Sprite):
    def __init__(self, texture: pg.Surface):
        super().__init__(texture)
        self.pos_x: float = 0
        self.pos_y: float = 0

    def locate(self, x: float = None, y: float = None, **kwargs) -> None:
        if x is None or y is None:
            self.rect = self.image.get_rect(**kwargs)
        else:
            self.rect = self.image.get_rect(center=(x, y))
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y


class Transparent(Locatable):
    def __init__(self, texture: pg.Surface, opacity: int = 100):
        texture.set_alpha(opacity)
        super().__init__(texture)
        self.opacity = opacity

    def set_opacity(self, opacity: int):
        self.opacity = opacity
        self.texture.set_alpha(opacity)

    def get_opacity(self) -> int:
        return self.opacity

    def set_texture(self, texture: pg.Surface):
        texture.set_alpha(self.opacity)
        super().set_texture(texture)


class Text(Locatable):
    def __init__(self, font: pg.font.Font, color: tuple[int, int, int], value: object = ""):
        super().__init__(
            texture=font.render("resources/fonts/opensans.ttf", True, color)
        )
        self._args: dict = {}
        self.font: pg.font.Font = font
        self.color: tuple[int, int, int] = color
        self.value: str = str(value)
        self._text_needs_update: bool = False

    def locate(self, x: float = None, y: float = None, **kwargs) -> None:
        super().locate()
        self._args = dict(x=x, y=y, **kwargs)

    def set_value(self, value: object):
        self.value = str(value)
        super().set_texture(self.font.render(self.value, True, self.color))
        super().locate(**self._args)

    def get_value(self) -> str:
        return self.value


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


class Group(pg.sprite.Group):
    def kill(self):
        for sprite in self:
            sprite.kill()
