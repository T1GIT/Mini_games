from config import Configuration as Conf
from sprites.meteor import Meteor
from sprites.piece import Piece
from utils.tools.group import Group


class Spawner:
    @staticmethod
    def all_pieces(on_field: bool):
        while len(Group.PIECES) < Conf.Piece.QUANTITY:
            piece = Piece()
            if on_field:
                piece.locate(*Piece.GetCoord().get_on_field())
            else:
                piece.locate(*Piece.GetCoord().get_out_field())
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
            meteor.locate(*Meteor.GetCoord().get_on_field())
        else:
            meteor.locate(*Meteor.GetCoord().get_out_field())
        meteor.add(Group.METEORS, Group.ALL)

    @staticmethod
    def change_difficulty(value):
        Conf.Meteor.PERIOD = value[0]
        Conf.Meteor.QUANTITY = value[1]

    @staticmethod
    def change_spawn_mode(value: bool):
        Conf.Meteor.BY_TIME = bool(value)
