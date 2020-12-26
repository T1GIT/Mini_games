import random as rnd

from config import Configuration as Conf
from sprites.interfaces.rotatable import Rotatable
from utils.resources.image import Image as Img


class Meteor(Rotatable):
    """
    Class of the meteor's mobs
    Can destroy ship
    Can be destroyed by rockets
    """

    def __init__(self):
        cnf = Conf.Meteor
        super().__init__(
            texture=Img.scale(rnd.choice(Img.get_meteors()), rnd.randint(cnf.MIN_SIZE, cnf.MAX_SIZE)),
            speed_x=rnd.uniform(-cnf.MAX_SPEED, Conf.Meteor.MAX_SPEED) * Conf.System.SCALE,
            speed_y=rnd.uniform(-cnf.MAX_SPEED, Conf.Meteor.MAX_SPEED) * Conf.System.SCALE,
            angle_speed=rnd.uniform(-cnf.MAX_ROTATE_SPEED, cnf.MAX_ROTATE_SPEED) * Conf.System.SCALE
        )
        # Variables
        self.lifes = ((max(self.texture.get_size()) - cnf.MIN_SIZE) // ((cnf.MAX_SIZE - cnf.MIN_SIZE) / cnf.MAX_LIFES))

    def update(self):
        self.move()
        if Conf.Meteor.ROTATING:
            self.rotate()
        if Conf.Meteor.TELEPORT:
            self.teleport()
        elif (self.rect.left > Conf.Window.WIDTH or self.rect.right < 0
                or self.rect.top > Conf.Window.HEIGHT or self.rect.bottom < 0):
            self.kill()

    def teleport(self):
        max_size = Conf.Meteor.MAX_SIZE
        width = Conf.Window.WIDTH
        height = Conf.Window.HEIGHT
        if self.rect.left < -max_size:
            self.rect.left = width
            self.pos_x = self.rect.x
        elif self.rect.right > width + max_size:
            self.rect.right = 0
            self.pos_x = self.rect.x
        if self.rect.top < -max_size:
            self.rect.top = height
            self.pos_y = self.rect.y
        elif self.rect.bottom > height + max_size:
            self.rect.bottom = 0
            self.pos_y = self.rect.y

    def wound(self):
        self.lifes -= 1

    def is_alive(self) -> bool:
        return self.lifes > 0
