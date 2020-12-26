import random as rnd

from config import Configuration as Conf
from sprites.interfaces.movable import Movable
from utils.resources.image import Image as Img


class Piece(Movable):
    """
    Class of the moving Pieces background
    Moves all the time
    """
    def __init__(self):
        cnf = Conf.Piece
        texture = Img.scale(rnd.choice(Img.get_pieces()), rnd.randint(cnf.MIN_SIZE, cnf.MAX_SIZE))
        texture.set_alpha(rnd.randint(Conf.Piece.MIN_OPACITY, Conf.Piece.MAX_OPACITY))
        super().__init__(
            texture=texture,
            speed_x=rnd.uniform(-cnf.MAX_SPEED, Conf.Meteor.MAX_SPEED) * Conf.System.SCALE,
            speed_y=rnd.uniform(-cnf.MAX_SPEED, Conf.Meteor.MAX_SPEED) * Conf.System.SCALE
        )

    def update(self):
        self.move()
        if (self.rect.left > Conf.Window.WIDTH or self.rect.right < 0
                or self.rect.top > Conf.Window.HEIGHT or self.rect.bottom < 0):
            self.kill()
