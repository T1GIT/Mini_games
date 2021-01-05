import random as rnd

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.basic import Rotatable
from sprites.interfaces.bound import Bound
from utils.resources.image import Image as Img


class Meteor(Rotatable, Bound.Teleportable, Bound.Killable):
    """
    Class of the meteor's mobs
    Can destroy ship
    Can be destroyed by rockets
    """
    group: pg.sprite.Group

    def __init__(self):
        cnf = Conf.Meteor
        self.model = rnd.randrange(len(Img.get_meteors()))
        self.lifes = self.size = rnd.randrange(cnf.SIZES)
        super().__init__(
            texture=Img.get_cache_by_angle(Img.get_meteors(), self.model, self.size, 0),
            speed_x=rnd.uniform(-cnf.MAX_SPEED, Conf.Meteor.MAX_SPEED),
            speed_y=rnd.uniform(-cnf.MAX_SPEED, Conf.Meteor.MAX_SPEED),
            rotator=lambda x: Img.get_cache_by_angle(Img.get_meteors(), self.model, self.size, round(x))
        )
        # Variables
        self.angle_speed = rnd.uniform(-cnf.MAX_ROTATE_SPEED, cnf.MAX_ROTATE_SPEED)

    def update(self):
        super().move()
        if Conf.Meteor.ROTATING:
            self.rotate(self.angle_speed)
        if Conf.Meteor.TELEPORT:
            super().bound_teleport()
        else:
            super().bound_kill()

    def wound(self):
        self.lifes -= 1
        if Conf.Meteor.DECREASE_SIZE:
            self.size -= 1

    def is_alive(self) -> bool:
        return self.lifes > 0
