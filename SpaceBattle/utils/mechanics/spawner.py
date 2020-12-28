from config import Configuration as Conf
from sprites.meteor import Meteor
from sprites.piece import Piece
from utils.tools.group import Group
import random as rnd


class Spawner:
    @staticmethod
    def all_pieces(on_field: bool):
        while len(Group.PIECES) < Conf.Piece.QUANTITY:
            piece = Piece()
            if on_field:
                piece.locate(*Spawner.GetCoord.get_on_field(Conf.Piece.MAX_SIZE))
            else:
                piece.locate(*Spawner.GetCoord.get_out_field(Conf.Piece.MAX_SIZE))
            piece.add(Group.PIECES, Group.ALL)

    @staticmethod
    def all_meteors():
        """
        Spawn all meteors by time or quantity configurations
        """
        while len(Group.METEORS) < Conf.Meteor.QUANTITY:
            Spawner.meteor()

    @staticmethod
    def meteor():
        """
        Spawn simple meteor on the field
        """
        meteor = Meteor()
        if Conf.Meteor.ON_FIELD:
            meteor.locate(*Spawner.GetCoord.get_on_field(Conf.Meteor.MAX_SIZE))
        else:
            meteor.locate(*Spawner.GetCoord.get_out_field(Conf.Meteor.MAX_SIZE))
        meteor.add(Group.METEORS, Group.ALL)

    @staticmethod
    def change_difficulty(value):
        Conf.Meteor.PERIOD = value[0]
        Conf.Meteor.QUANTITY = value[1]

    @staticmethod
    def change_spawn_mode(value: bool):
        Conf.Meteor.BY_TIME = bool(value)

    class GetCoord:
        @staticmethod
        def get_on_field(offset: float):
            """
            Get coordinates on field
            :return: horizontally and vertically position
            """
            x = rnd.uniform(0 + offset, Conf.Window.WIDTH - offset)
            y = rnd.uniform(0 + offset, Conf.Window.HEIGHT - offset)
            return x, y

        @staticmethod
        def get_out_field(offset: float):
            """
            Get coordinates out of field
            :param offset: max size of object
            :return: horizontally and vertically position
            """
            if rnd.random() > 0.5:
                x = rnd.choice((-offset / 2, Conf.Window.WIDTH + offset / 2))
                y = rnd.uniform(-offset / 2, Conf.Window.HEIGHT + offset / 2)
            else:
                x = rnd.uniform(-offset / 2, Conf.Window.WIDTH + offset / 2)
                y = rnd.choice((-offset / 2, Conf.Window.HEIGHT + offset / 2))
            return x, y
