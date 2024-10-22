from math import atan2, degrees, hypot

from config import Configuration as Conf
from sprites.interfaces.basic import Rotatable, Sprite
from sprites.interfaces.bound import Stopable
from sprites.interfaces.extended import AcceleratableWithFire
from sprites.interfaces.shooting import RocketShootable, ThreeRocketShootable
from utils.resources.image import Image as Img
from utils.resources.sound import Sound as Snd


class Ship(AcceleratableWithFire, RocketShootable, Stopable, Rotatable):
    """
    Class of the player's mob
    Can shooting rockets
    Can by destroyed by meteors
    """

    def __init__(self):
        texture_pack = (
           Img.scale(Img.get_ship(Conf.Image.SHIP, False), Conf.Ship.SIZE),
           Img.scale(Img.get_ship(Conf.Image.SHIP, True), Conf.Ship.SIZE)
        )
        AcceleratableWithFire.__init__(
            self,
            texture_pack=texture_pack,
            weight=Conf.Ship.WEIGHT,
            power=Conf.Ship.POWER,
            resist=Conf.Ship.RESIST
        )
        Rotatable.__init__(self, texture_pack[0])
        RocketShootable.__init__(self, texture_pack[0], period=Conf.Rocket.PERIOD)
        Stopable.__init__(self, texture_pack[0])

    def update(self):
        """
        Updates ship coordinates.
        Adds the axis speed in the current time
        period to it's coordinates
        """
        super().move()
        if hypot(self.speed_x, self.speed_y) < Conf.Ship.DEAD_SPEED:
            self.speed_x, self.speed_y = 0, 0

    def accelerate(self, x, y):
        if not self.with_fire and (x, y) != (0, 0):
            Snd.engine()
        super().accelerate(x, y)

    def vector_rotate(self, x: float, y: float, smooth: bool):
        """
        Rotates player's sprite in the direction of the vector.
        :param x: coordinate of the axel vector
        :param y: coordinate of the axel vector
        :param smooth: rotates not on the whole vector, but partially
        """
        delta = degrees(atan2(y, x)) - (self.angle + 90) % 360
        if delta > 180:
            delta -= 360
        elif delta < -180:
            delta += 360
        if smooth:
            if abs(delta) > 50 / Conf.Control.Mouse.ACCURACY * Conf.System.SCALE:
                delta = delta / Conf.Control.Mouse.SMOOTH
                super().rotate(delta)
        else:
            super().rotate(delta)

    def shoot(self) -> tuple[Sprite, ...]:
        Snd.shoot()
        return super().shoot()
