from collections import deque

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.basic import Locatable
from utils.resources.image import Image as Img
from utils.tools.groups import Groups
from utils.tools.timer import Timer


class Animation(Locatable):
    """
    Class that shows an animation of exploding objects
    """
    def __init__(self, name: str, size: float = Conf.Animation.DEFAULT_SIZE):
        self.frames = deque(map(lambda x: Img.scale(x, size), Img.get_animation(name)))
        super().__init__(texture=self.frames.popleft())
        self.frames_timer = Timer(1000 / Conf.Animation.FPS)

    def update(self):
        if self.frames_timer.is_ready():
            self.frames_timer.start()
            if len(self.frames) > 0:
                self.image = self.frames.popleft()
            else:
                super().kill()

    @staticmethod
    def on_sprite(name: str, sprite: pg.sprite.Sprite, size: float):
        """
        Animation is invoked
        :param size: size of the animation
        :param name: name of animation package
        :param sprite: the sprite for which the animation is called
        """
        x, y = sprite.rect.centerx, sprite.rect.centery
        animation = Animation(name, size)
        animation.add(Groups.ANIMATION, Groups.ALL)
        animation.locate(x, y)
