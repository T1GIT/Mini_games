from math import radians, cos, sin

import pygame as pg

from sprites.interfaces.basic import Rotatable
from sprites.interfaces.bound import Bound
from sprites.rocket import Rocket
from utils.tools.groups import Groups


class Shootable(Rotatable):
    def __init__(self, texture: pg.Surface, speed_x: float = 0, speed_y: float = 0):
        super().__init__(texture, speed_x, speed_y)
        self.shoot_radius: int = self.get_shoot_radius(texture)

    def shoot(self):
        angle = -self.angle - 90
        rad = radians(angle)
        x = self.rect.centerx + self.shoot_radius * cos(rad)
        y = self.rect.centery + self.shoot_radius * sin(rad)
        rocket = Rocket()
        rocket.shoot(x, y, angle)
        rocket.add(Groups.ROCKETS, Groups.ALL)

    def set_texture(self, texture: pg.Surface):
        super().set_texture(texture)
        self.shoot_radius = self.get_shoot_radius(texture)

    @staticmethod
    def get_shoot_radius(texture: pg.Surface) -> int:
        mask = pg.mask.from_surface(texture)
        c_x, c_y = map(lambda x: x // 2, mask.get_size())
        alpha = 0
        for i in range(mask.get_size()[1]):
            if not mask.get_at((c_x, i)): alpha += 1
            else: break
        return c_y - alpha

