from math import radians, cos, sin

import pygame as pg

from sprites.interfaces.basic import Rotatable
from sprites.interfaces.bound import Bound
from sprites.rocket import Rocket
from utils.tools.group import Group


class Shootable(Rotatable, Bound.Resistable):
    def __init__(self, texture: pg.Surface, speed_x: float = 0, speed_y: float = 0):
        super().__init__(texture, speed_x, speed_y)

    def shoot(self):
        angle = -self.angle - 90
        rad = radians(angle)
        x = self.rect.centerx + self.radius * cos(rad)
        y = self.rect.centery + self.radius * sin(rad)
        rocket = Rocket()
        rocket.shoot(x, y, angle)
        rocket.add(Group.ROCKETS, Group.ALL)
