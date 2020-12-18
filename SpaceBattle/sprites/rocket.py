from math import cos, sin, radians, sqrt

import pygame as pg

from config import Configuration as Conf
from utils.resources.image import Image as Img


class Rocket(pg.sprite.Sprite):
    """
    Class of the rocket's mobs.
    Flies out from the rocket's nose.
    Destroys meteors
    """
    def __init__(self):
        super().__init__()
        # Settings
        self.angle = 0
        self.start_x, self.start_y = 0, 0
        self.a_x, self.a_y = 0, 0
        # Init sprite
        pg.sprite.Sprite.__init__(self)
        raw_image = Img.get_rocket()
        w0, h0 = raw_image.get_size()
        scale = Conf.Rocket.SIZE / h0
        w1, h1 = map(lambda x: round(x * scale), [w0, h0])
        self.texture_num = Conf.Image.ROCKET
        self.texture = pg.transform.scale(raw_image, (w1, h1))
        self.image = self.texture
        self.start_x, self.start_y = 0, 0
        self.speed_x, self.speed_y = 0, 0
        self.pos_x, self.pos_y = 0, 0
        self.angle = 0

    def locate(self, x, y, deg):
        """
        Shows sprite in the screen
        :param x: position
        :param y: position
        :param deg: angle of rotation
        """
        self.angle = deg
        rad = radians(self.angle)
        self.start_x, self.start_y = x, y
        self.speed_x = Conf.Rocket.SPEED * cos(rad) * Conf.System.SCALE
        self.speed_y = Conf.Rocket.SPEED * sin(rad) * Conf.System.SCALE
        self.image = pg.transform.rotate(self.texture, -self.angle)
        self.rect = self.image.get_rect(center=(self.start_x, self.start_y))
        self.pos_x, self.pos_y = self.rect.x, self.rect.y

    def update(self):
        if self.texture_num != Conf.Image.ROCKET:
            self.texture_num = Conf.Image.ROCKET
            self.update_texture()
        c_x, c_y = self.rect.center
        if Conf.Rocket.UNLIMITED:
            if 0 < c_x < Conf.Window.WIDTH and 0 < c_y < Conf.Window.HEIGHT:
                self.pos_x += self.speed_x
                self.pos_y += self.speed_y
            else:
                self.kill()
        else:
            if sqrt(pow(c_x - self.start_x, 2) + pow(c_y - self.start_y, 2)) <= Conf.Rocket.MAX_DISTANCE:
                self.pos_x += self.speed_x
                self.pos_y += self.speed_y
            else:
                self.kill()
        self.rect.x, self.rect.y = self.pos_x, self.pos_y

    def update_texture(self):
        raw_image = Img.get_rocket()
        w0, h0 = raw_image.get_size()
        scale = Conf.Rocket.SIZE / h0
        w1, h1 = map(lambda x: round(x * scale), [w0, h0])
        self.texture = pg.transform.scale(raw_image, (w1, h1))
        self.image = self.texture

    @staticmethod
    def set_texture(num: int):
        Conf.Image.ROCKET = num
