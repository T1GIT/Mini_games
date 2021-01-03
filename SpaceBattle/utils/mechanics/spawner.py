import random as rnd

from config import Configuration as Conf
from sprites.meteor import Meteor
from sprites.piece import Piece
from utils.tools.groups import Groups


class Spawner:
    @staticmethod
    def all_pieces(on_field: bool):
        while len(Groups.PIECES) < Conf.Piece.QUANTITY:
            Spawner.piece(on_field)

    @staticmethod
    def all_meteors():
        """
        Spawn all meteors by time or quantity configurations
        """
        while len(Groups.METEORS) < Conf.Meteor.QUANTITY:
            Spawner.meteor()

    @staticmethod
    def piece(on_field: bool):
        piece = Piece()
        if on_field:
            piece.locate(*Spawner.GetCoord.get_on_field())
        else:
            piece.locate(*Spawner.GetCoord.get_out_field(*piece.image.get_size()))
        piece.add(Groups.PIECES, Groups.ALL)

    @staticmethod
    def meteor():
        """
        Spawn simple meteor on the field
        """
        meteor = Meteor()
        if Conf.Meteor.ON_FIELD:
            meteor.locate(*Spawner.GetCoord.get_on_field())
        else:
            meteor.locate(*Spawner.GetCoord.get_out_field(*meteor.image.get_size()))
        meteor.add(Groups.METEORS, Groups.ALL)

    @staticmethod
    def change_difficulty(value):
        Conf.Meteor.PERIOD = value[0]
        Conf.Meteor.QUANTITY = value[1]

    @staticmethod
    def change_meteor_spawn_mode(value: bool):
        Conf.Meteor.BY_TIME = bool(value)

    class GetCoord:
        @staticmethod
        def get_on_field():
            """
            Get coordinates on field
            :return: horizontally and vertically position
            """
            x = rnd.uniform(0, Conf.Window.WIDTH)
            y = rnd.uniform(0, Conf.Window.HEIGHT)
            return x, y

        @staticmethod
        def get_out_field(x_size: int, y_size: int):
            """
            Get coordinates out of field
            :param x_size: size of the object on x axis
            :param y_size: size of the object on y axis
            :return: horizontally and vertically position of the center
            """
            if rnd.random() > 0.5:
                x = rnd.choice((-x_size / 2, Conf.Window.WIDTH + x_size / 2))
                y = rnd.uniform(-y_size / 2, Conf.Window.HEIGHT + y_size / 2)
            else:
                x = rnd.uniform(-x_size / 2, Conf.Window.WIDTH + x_size / 2)
                y = rnd.choice((-y_size / 2, Conf.Window.HEIGHT + y_size / 2))
            return x, y
