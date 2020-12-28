from collections import deque

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.basic import Locatable
from utils.tools.group import Group
from utils.resources.image import Image as Img
from utils.tools.timer import Timer


class Animation(Locatable):
    """
    Class that shows an animation of exploding objects
    """

    def __init__(self, name: str, size: int = Conf.Animation.DEFAULT_SIZE):
        self.frames = deque(map(lambda x: Img.scale(x, size), Img.get_animation(name)))
        super().__init__(texture=self.frames.popleft())
        self.frame_timer = Timer()

    def update(self):
        if self.frame_timer.tick():
            self.frame_timer.set(Conf.System.FPS // Conf.Animation.FPS)
            if len(self.frames) > 0:
                self.image = self.frames.popleft()
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.kill()

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
