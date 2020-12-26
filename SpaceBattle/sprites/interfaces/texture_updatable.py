from abc import ABC, abstractmethod

import pygame as pg

from sprites.interfaces.sprite import Sprite
from utils.resources.image import Image as Img


class TextureUpdatable(Sprite, ABC):
    def __init__(self, texture: pg.Surface):
        super().__init__(texture)

    def update_texture(self, raw_texture: pg.Surface, size: float) -> None:
        self.texture = Img.scale(raw_texture, size)
        self.image = self.texture

    @staticmethod
    @abstractmethod
    def set_texture(num: int) -> None:
        pass
