import random as rnd

from config import Configuration as Conf
from sprites.loot.heal import Heal
from sprites.mobs.meteor import Meteor
from sprites.effects.piece import Piece
from utils.tools.groups import Groups


class Spawner:
    @staticmethod
    def heal():
        heal = Heal()
        heal.locate(*Spawner.GetCoord.get_out_field(heal.image.get_size(), heal.get_speed()))
        heal.add(Groups.HEALS, Groups.ALL)

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
            piece.locate(*Spawner.GetCoord.get_out_field(piece.image.get_size(), piece.get_speed()))
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
            meteor.locate(*Spawner.GetCoord.get_out_field(meteor.image.get_size(), meteor.get_speed()))
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
        def get_on_field() -> tuple[float, float]:
            """
            Get coordinates on field
            :return: horizontally and vertically position
            """
            x = rnd.uniform(0, Conf.Window.WIDTH)
            y = rnd.uniform(0, Conf.Window.HEIGHT)
            return x, y

        @staticmethod
        def get_out_field(size: tuple[float, float], speed: tuple[float, float]) -> tuple[float, float]:
            """
            Get coordinates out of field
            :param size: size of the object on x and y axis
            :param speed: x and y axis speed of the sprite
            :return: horizontally and vertically position of the center
            """
            if rnd.random() > 0.5:
                x = (-size[0] / 2) if speed[0] > 0 else (Conf.Window.WIDTH + size[0] / 2)
                y = rnd.uniform(-size[1] / 2, Conf.Window.HEIGHT + size[1] / 2)
            else:
                x = rnd.uniform(-size[0] / 2, Conf.Window.WIDTH + size[0] / 2)
                y = (-size[1] / 2) if speed[1] > 0 else (Conf.Window.HEIGHT + size[1] / 2)
            return x, y
