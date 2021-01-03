from math import cos, sin, atan2, sqrt, degrees, tan, hypot

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.basic import TextureUpdatable, Rotatable, Acceleratable
from sprites.interfaces.extended import Shootable
from sprites.interfaces.bound import Bound
from utils.resources.image import Image as Img
from utils.resources.sound import Sound as Snd


class Ship(TextureUpdatable, Shootable, Acceleratable, Bound.Resistable):
    """
    Class of the player's mob
    Can shooting rockets
    Can by destroyed by meteors
    """
    texture_num = Conf.Image.SHIP
    needs_update = False

    def __init__(self):
        self.texture_normal = Img.scale(Img.get_ship(Ship.texture_num, False), Conf.Ship.SIZE)
        self.texture_fire = Img.scale(Img.get_ship(Ship.texture_num, True), Conf.Ship.SIZE)
        super().__init__(texture=self.texture_normal)
        # Variables
        self.with_fire = False

    def update(self):
        """
        Updates ship coordinates.
        Adds the axis speed in the current time
        period to it's coordinates
        Called every frame.
        """
        if Ship.needs_update:
            self.update_texture(Img.get_ship(Ship.texture_num, self.with_fire), Conf.Ship.SIZE)
            self.vector_rotate(1, tan(self.angle), False)
        if abs(self.speed_x) < Conf.Ship.DEAD_SPEED and abs(self.speed_y) < Conf.Ship.DEAD_SPEED:
            self.speed_x, self.speed_y = 0, 0
        else:
            super().bound_resist()
            super().move()

    def vector_accelerate(self, x, y):
        cnf = Conf.Ship
        super().accelerate(x, -y, cnf.WEIGHT, cnf.POWER, cnf.RESIST)
        self.wear_fire((x, y) != (0, 0))

    def vector_rotate(self, x: float, y: float, smooth: bool):
        """
        Rotates player's sprite in the direction of the vector.
        :param x: coordinate of the axel vector
        :param y: coordinate of the axel vector
        :param smooth: rotates not on the whole vector, but partially
        """
        delta = degrees(atan2(y, x)) - (self.angle + 90) % 360
        if delta > 180: delta -= 360
        elif delta < -180: delta += 360
        if smooth:
            if abs(delta) > 50 / Conf.Control.Mouse.ACCURACY * Conf.System.SCALE:
                delta = delta / Conf.Control.Mouse.SMOOTH
                super().rotate(delta)
        else:
            super().rotate(delta)

    def shoot(self):
        super().shoot()
        Snd.shoot()

    def wear_fire(self, with_fire: bool):
        if with_fire != self.with_fire:
            self.with_fire = with_fire
            self.texture = self.texture_fire if with_fire else self.texture_normal
            super().rotate()
            self.rect = self.image.get_rect(center=self.rect.center)
            if with_fire: Snd.engine()

    def update_texture(self, raw_texture: pg.Surface, size: float) -> None:
        self.texture_normal = Img.scale(Img.get_ship(Ship.texture_num, False), size)
        self.texture_fire = Img.scale(Img.get_ship(Ship.texture_num, True), size)
        super().update_texture(raw_texture, size)
