from math import cos, sin, radians, dist

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.basic import Movable
from sprites.interfaces.bound import Killable
from utils.resources.image import Image as Img


class Rocket(Killable, Movable):
    """
    Class of the rocket's mobs.
    Flies out from the rocket's nose.
    Destroys meteors
    """

    def __init__(self):
        super().__init__(texture=Img.scale(Img.get_rocket(Conf.Image.ROCKET), Conf.Rocket.SIZE))
        # Settings
        self.start_pos: tuple[int, int] = (0, 0)

    def run(self, x: float, y: float, deg: float):
        rad = radians(deg)
        super().set_speed(
            speed_x=Conf.Rocket.SPEED * cos(rad),
            speed_y=Conf.Rocket.SPEED * sin(rad)
        )
        self.start_pos = (x, y)
        self.image = pg.transform.rotate(self.texture, -deg)
        super().locate(x, y)

    def update(self):
        super().move()
        if not Conf.Rocket.UNLIMITED and dist(self.start_pos, self.rect.center) > Conf.Rocket.MAX_DISTANCE:
            super().kill()
