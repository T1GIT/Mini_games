import random as rnd

import pygame as pg

from config import Configuration as Conf
from sprites.interfaces.extended import Spawnable
from utils.resources.image import Image as Img


class Piece(Spawnable):
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
            speed_x=rnd.uniform(-cnf.MAX_SPEED, cnf.MAX_SPEED),
            speed_y=rnd.uniform(-cnf.MAX_SPEED, cnf.MAX_SPEED)
        )

    def update(self):
        super().move()
