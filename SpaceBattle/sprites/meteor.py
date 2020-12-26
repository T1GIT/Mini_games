import random as rnd

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.movable import Movable
from utils.resources.image import Image as Img


class Meteor(Movable):
    """
    Class of the meteor's mobs
    Can destroy ship
    Can be destroyed by rockets
    """

    def __init__(self):
        self.model = rnd.randrange(len(Img.get_meteors()))
        self.lifes = self.size = rnd.randrange(Conf.Meteor.SIZES)
        cnf = Conf.Meteor
        super().__init__(
            texture=Img.get_meteors()[self.model][self.size][0],
            speed_x=rnd.uniform(-cnf.MAX_SPEED, Conf.Meteor.MAX_SPEED),
            speed_y=rnd.uniform(-cnf.MAX_SPEED, Conf.Meteor.MAX_SPEED)
        )
        # Variables
        self.angle = 0
        self.angle_speed = rnd.uniform(-cnf.MAX_ROTATE_SPEED, cnf.MAX_ROTATE_SPEED)

    def update(self):
        self.move()
        if Conf.Meteor.ROTATING:
            self.rotate()
        if Conf.Meteor.TELEPORT:
            self.teleport()
        elif (self.rect.left > Conf.Window.WIDTH or self.rect.right < 0
                or self.rect.top > Conf.Window.HEIGHT or self.rect.bottom < 0):
            self.kill()

    def rotate(self):
        x_offset = self.pos_x - self.rect.x
        y_offset = self.pos_y - self.rect.y
        self.angle = (self.angle + self.angle_speed * Conf.System.SCALE) % 360
        if round(self.angle) <= 180:
            image = Img.get_meteors()[self.model][self.size][round(self.angle)]
        else:
            image = Img.get_meteors()[self.model][self.size][round(self.angle) - 180]
            image = pg.transform.flip(image, True, True)
        self.image = image
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos_x = self.rect.x + x_offset
        self.pos_y = self.rect.y + y_offset

    def teleport(self):
        max_size = Conf.Meteor.MAX_SIZE
        width = Conf.Window.WIDTH
        height = Conf.Window.HEIGHT
        if self.rect.left < -max_size:
            self.rect.left = width
            self.pos_x = self.rect.x
        elif self.rect.right > width + max_size:
            self.rect.right = 0
            self.pos_x = self.rect.x
        if self.rect.top < -max_size:
            self.rect.top = height
            self.pos_y = self.rect.y
        elif self.rect.bottom > height + max_size:
            self.rect.bottom = 0
            self.pos_y = self.rect.y

    def wound(self):
        self.lifes -= 1
        if Conf.Meteor.DECREASE_SIZE:
            self.size -= 1

    def is_alive(self) -> bool:
        return self.lifes > 0
