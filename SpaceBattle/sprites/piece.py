import random as rnd

import pygame as pg

from config import Configuration as Conf
from utils.resources.image import Image as Img


class Piece(pg.sprite.Sprite):
    """
    Class of the moving Pieces background
    Moves all the time
    """
    def __init__(self):
        super().__init__()
        # Settings
        self.speed_x = rnd.uniform(-Conf.Piece.MAX_SPEED, Conf.Piece.MAX_SPEED) * Conf.System.SCALE
        self.speed_y = rnd.uniform(-Conf.Piece.MAX_SPEED, Conf.Piece.MAX_SPEED) * Conf.System.SCALE
        self.pos_x, self.pos_y = 0, 0
        # Initialising sprite
        pg.sprite.Sprite.__init__(self)
        raw_image = Img.get_pieces()
        self.amount = rnd.randint(0, len(raw_image) - 1)
        w0, h0 = raw_image[self.amount].get_size()
        scale = rnd.randint(Conf.Piece.MIN_SIZE, Conf.Piece.MAX_SIZE) / max(w0, h0)
        w1, h1 = map(lambda x: round(x * scale), [w0, h0])
        self.texture = pg.transform.scale(raw_image[self.amount], (w1, h1))
        self.texture.set_alpha(rnd.randint(Conf.Piece.MIN_OPACITY, Conf.Piece.MAX_OPACITY))
        self.image = pg.transform.rotate(self.texture, rnd.randint(0, 360))

    def locate(self, x, y):
        """
        Shows sprite in the screen
        :param x: position of the end
        :param y: position of the end
        """
        self.rect = self.image.get_rect(center=(x, y))
        self.pos_x, self.pos_y = self.rect.x, self.rect.y

    def update(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        self.rect.x, self.rect.y = self.pos_x, self.pos_y
        if (self.rect.left > Conf.Window.WIDTH or self.rect.right < 0
                or self.rect.top > Conf.Window.HEIGHT or self.rect.bottom < 0):
            self.kill()

    class GetCoord:
        @staticmethod
        def get_on_field():
            """
            Get coordinates on field for Piece object
            :return: horizontally and vertically position
            """
            x = rnd.uniform(0, Conf.Window.WIDTH)
            y = rnd.uniform(0, Conf.Window.HEIGHT)
            return x, y

        @staticmethod
        def get_out_field():
            """
            Get coordinates out of field for Piece object
            :return: horizontally and vertically position
            """
            if rnd.random() > 0.5:
                x = rnd.choice((-Conf.Piece.MAX_SIZE / 2, Conf.Window.WIDTH + Conf.Piece.MAX_SIZE / 2))
                y = rnd.uniform(-Conf.Piece.MAX_SIZE / 2, Conf.Window.HEIGHT + Conf.Piece.MAX_SIZE / 2)
            else:
                x = rnd.uniform(-Conf.Piece.MAX_SIZE / 2, Conf.Window.WIDTH + Conf.Piece.MAX_SIZE / 2)
                y = rnd.choice((-Conf.Piece.MAX_SIZE / 2, Conf.Window.HEIGHT + Conf.Piece.MAX_SIZE / 2))
            return x, y
