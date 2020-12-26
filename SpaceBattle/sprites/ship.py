import random as rnd
from math import cos, sin, atan2, sqrt, degrees, radians, tan

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.movable import Movable
from sprites.interfaces.rotatable import Rotatable
from sprites.interfaces.texture_updatable import TextureUpdatable
from sprites.rocket import Rocket
from utils.resources.image import Image as Img
from utils.resources.sound import Sound as Snd
from utils.tools.group import Group


class Ship(Movable, TextureUpdatable):
    """
    Class of the player's mob
    Can shooting rockets
    Can by destroyed by meteors
    """
    needs_update: bool = False
    _accuracy = 50 / Conf.Control.Mouse.ACCURACY

    def __init__(self):
        self.texture_normal = Img.scale(Img.get_ship(False), Conf.Ship.SIZE)
        self.texture_fire = Img.scale(Img.get_ship(True), Conf.Ship.SIZE)
        super().__init__(texture=self.texture_normal)
        # Variables
        self.half_width = self.texture_normal.get_width() / 2
        self.half_height = self.texture_normal.get_height() / 2
        self.angle = 90
        self.with_fire = False

    def update(self):
        """
        Updates ship coordinates.
        Adds the axis speed in the current time
        period to it's coordinates
        Called every frame.
        """
        if self.needs_update:
            self.update_texture(Img.get_ship(self.with_fire), Conf.Ship.SIZE)
            self.rotate(1, tan(self.angle), False)
            Ship.needs_update = False
        if abs(self.speed_x) < Conf.Ship.DEAD_SPEED and abs(self.speed_y) < Conf.Ship.DEAD_SPEED:
            self.speed_x, self.speed_y = 0, 0
        else:
            next_x, next_y = self.rect.centerx + self.speed_x, self.rect.centery - self.speed_y
            if self.half_width > next_x or next_x > Conf.Window.WIDTH - self.half_width:
                self.speed_x = 0
            else:
                self.pos_x += self.speed_x * Conf.System.SCALE
            if self.half_width > next_y or next_y > Conf.Window.HEIGHT - self.half_width:
                self.speed_y = 0
            else:
                self.pos_y -= self.speed_y * Conf.System.SCALE
            self.rect.x, self.rect.y = self.pos_x, self.pos_y

    def accelerate(self, x, y):
        """
        Changes axis speed, from axel vector
        :param x: coordinate of the axel vector
        :param y: coordinate of the axel vector
        """
        r = self._resist(self.speed_x, self.speed_y)
        a = self._axel(x, y)
        self.speed_x += (a[0] - r[0]) / Conf.Ship.WEIGHT
        self.speed_y += (a[1] - r[1]) / Conf.Ship.WEIGHT
        self._wear_fire(True)

    def brake(self):
        r = self._resist(self.speed_x, self.speed_y)
        self.speed_x -= r[0] / Conf.Ship.WEIGHT
        self.speed_y -= r[1] / Conf.Ship.WEIGHT
        self._wear_fire(False)

    def rotate(self, x: float, y: float, smooth: bool):
        """
        Rotates player's sprite in the direction of the vector.
        :param x: coordinate of the axel vector
        :param y: coordinate of the axel vector
        :param smooth: rotates not on the whole vector, but partially
        """
        d_deg = degrees(atan2(y, x)) - self.angle
        if d_deg > 180: d_deg -= 360
        elif d_deg < -180: d_deg += 360
        if (not smooth) or abs(d_deg) > self._accuracy * Conf.System.SCALE:
            self.angle += (d_deg / Conf.Control.Mouse.SMOOTH * Conf.System.SCALE) if smooth else d_deg
            self.image = pg.transform.rotate(
                self.texture_fire if self.with_fire else self.texture_normal, self.angle - 90)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.pos_x, self.pos_y = self.rect.x, self.rect.y
            if self.angle > 180: self.angle -= 360
            elif self.angle < -180: self.angle += 360

    def shoot(self):
        rocket = Rocket()
        ctr = self.rect.center
        rad = radians(-self.angle)
        x = ctr[0] + self.half_height * cos(rad)
        y = ctr[1] + self.half_height * sin(rad)
        rocket.shoot(x, y, -self.angle)
        Snd.shoot()
        rocket.add(Group.ROCKETS, Group.ALL)

    def update_texture(self, raw_texture: pg.Surface, size: float) -> None:
        self.texture = Img.scale(raw_texture, size)
        self.image = self.texture
        self.texture_normal = Img.scale(Img.get_ship(False), size)
        self.texture_fire = Img.scale(Img.get_ship(True), size)

    def _wear_fire(self, with_fire: bool):
        if with_fire != self.with_fire:
            self.with_fire = with_fire
            self.image = pg.transform.rotate(
                self.texture_fire if with_fire else self.texture_normal, self.angle - 90)
            self.rect = self.image.get_rect(center=self.rect.center)
            if with_fire: Snd.engine()

    @staticmethod
    def _resist(speed_x, speed_y):
        speed = sqrt(pow(speed_x, 2) + pow(speed_y, 2))
        rad = atan2(speed_y, speed_x)
        r = Conf.Ship.RESIST * pow(speed, 2)
        r_x = r * cos(rad)
        r_y = r * sin(rad)
        return r_x, r_y

    @staticmethod
    def _axel(x, y):
        if (x, y) == (0, 0): return 0, 0
        rad = atan2(y, x)
        f = Conf.Ship.POWER
        a_x = f * cos(rad) * pow(x, 2)
        a_y = f * sin(rad) * pow(y, 2)
        return a_x, a_y

    @staticmethod
    def set_texture(num: int):
        Conf.Image.SHIP = num
        Ship.needs_update = True
