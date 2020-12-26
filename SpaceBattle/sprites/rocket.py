import random as rnd
from math import cos, sin, radians, sqrt

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.movable import Movable
from sprites.interfaces.texture_updatable import TextureUpdatable
from utils.resources.image import Image as Img


class Rocket(Movable, TextureUpdatable):
    """
    Class of the rocket's mobs.
    Flies out from the rocket's nose.
    Destroys meteors
    """
    needs_update = False

    def __init__(self):
        super().__init__(texture=Img.scale(Img.get_rocket(), Conf.Rocket.SIZE))
        # Settings
        self.start_x, self.start_y = 0, 0

    def shoot(self, x, y, deg):
        rad = radians(deg)
        self.start_x, self.start_y = x, y
        self.set_speed(
            x=Conf.Rocket.SPEED * cos(rad) * Conf.System.SCALE,
            y=Conf.Rocket.SPEED * sin(rad) * Conf.System.SCALE
        )
        self.image = pg.transform.rotate(self.texture, -deg)
        self.locate(x, y)

    def update(self):
        if self.needs_update:
            self.update_texture(Img.get_rocket(), Conf.Rocket.SIZE)
            Rocket.needs_update = False
        c_x, c_y = self.rect.center
        if Conf.Rocket.UNLIMITED:
            if 0 < c_x < Conf.Window.WIDTH and 0 < c_y < Conf.Window.HEIGHT:
                self.move()
            else:
                self.kill()
        else:
            if sqrt(pow(c_x - self.start_x, 2) + pow(c_y - self.start_y, 2)) <= Conf.Rocket.MAX_DISTANCE:
                self.move()
            else:
                self.kill()

    @staticmethod
    def set_texture(num: int):
        Conf.Image.ROCKET = num
        Rocket.needs_update = True
