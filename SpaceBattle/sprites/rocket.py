from math import cos, sin, radians, dist

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.basic import TextureUpdatable, Movable
from sprites.interfaces.bound import Bound
from utils.resources.image import Image as Img


class Rocket(Bound.Killable, Movable, TextureUpdatable):
    """
    Class of the rocket's mobs.
    Flies out from the rocket's nose.
    Destroys meteors
    """
    texture_num = Conf.Image.ROCKET
    needs_update = False

    def __init__(self):
        super().__init__(texture=Img.scale(Img.get_rocket(Rocket.texture_num), Conf.Rocket.SIZE))
        # Settings
        self.start_center: tuple[int, int] = (0, 0)

    def shoot(self, x: float, y: float, deg: float):
        rad = radians(deg)
        super().set_speed(
            x=Conf.Rocket.SPEED * cos(rad),
            y=Conf.Rocket.SPEED * sin(rad)
        )
        self.start_center = (x, y)
        self.image = pg.transform.rotate(self.texture, -deg)
        super().locate(x, y)

    def update(self):
        if Rocket.needs_update:
            super().update_texture(Img.get_rocket(Rocket.texture_num), Conf.Rocket.SIZE)
        super().move()
        if Conf.Rocket.UNLIMITED:
            super().bound_kill()
        elif dist(self.start_center, self.rect.center) > Conf.Rocket.MAX_DISTANCE:
            super().kill()
