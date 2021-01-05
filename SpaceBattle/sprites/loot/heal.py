import random as rnd

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.bound import Bound
from utils.resources.image import Image as Img


class Heal(Bound.Killable):
    """
    Class of the moving Pieces background
    Moves all the time
    """

    def __init__(self):
        cnf = Conf.Heal
        super().__init__(
            texture=Img.scale(Img.get_heal(), cnf.SIZE),
            speed_x=rnd.uniform(-cnf.MAX_SPEED, cnf.MAX_SPEED),
            speed_y=rnd.uniform(-cnf.MAX_SPEED, cnf.MAX_SPEED)
        )

    def update(self):
        super().move()
        super().bound_kill()
