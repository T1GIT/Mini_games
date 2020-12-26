import pygame as pg

from abc import ABC, abstractmethod
from utils.resources.image import Image as Img
from sprites.interfaces.sprite import Sprite


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
