from collections import deque

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.locatable import Locatable
from utils.tools.group import Group
from utils.resources.image import Image as Img


class Animation(Locatable):
    """
    Class that shows an animation of exploding objects
    """

    def __init__(self, name: str, size: int = Conf.Animation.DEFAULT_SIZE):
        self.frames = deque(map(lambda x: Img.scale(x, size), Img.get_animation(name)))
        super().__init__(texture=self.frames.popleft())
        self.skipped = 1

    def update(self):
        if self.skipped % (Conf.System.FPS // Conf.Animation.FPS) == 0:
            if len(self.frames) > 0:
                self.image = self.frames.popleft()
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.kill()
        self.skipped += 1

    @staticmethod
    def on_sprite(name: str, sprite: pg.sprite.Sprite, size: int):
        """
        Animation is invoked
        :param size: size of the animation
        :param name: name of animation package
        :param sprite: the sprite for which the animation is called
        """
        x, y = sprite.rect.centerx, sprite.rect.centery
        animation = Animation(name, size)
        Group.ALL.add(animation)
        animation.locate(x, y)
