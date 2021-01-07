import random as rnd

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.bound import Bound
from utils.resources.image import Image as Img


class Bonus(Bound.Killable):
    """
    Class of the moving bonuses.
    Moves all the time
    """

    def __init__(self, texture: pg.Surface):
        cnf = Conf.Bonus
        super().__init__(
            texture=Img.scale(texture, cnf.SIZE),
            speed_x=rnd.uniform(-cnf.MAX_SPEED, cnf.MAX_SPEED),
            speed_y=rnd.uniform(-cnf.MAX_SPEED, cnf.MAX_SPEED)
        )

    def update(self):
        super().move()
        super().bound_kill()


class Heal(Bonus):
    def __init__(self):
        super().__init__(Img.get_heal())
