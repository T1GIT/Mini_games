import random as rnd

from config import Configuration as Conf
from sprites.interfaces.basic import Sprite, Movable
from sprites.loot.bonuses import Heal
from sprites.mobs.meteor import Meteor
from sprites.effects.piece import Piece
from utils.tools.groups import Groups


class Spawner:
    @staticmethod
    def one(cls: type, on_field: bool = False) -> Sprite:
        sprite = cls()
        if on_field:
            sprite.locate(*Spawner.GetCoord.get_on_field())
        else:
            sprite.locate(*Spawner.GetCoord.get_out_field(sprite.get_size(), sprite.get_speed()))
        return sprite

    @staticmethod
    def many(cls: type, amount: int, on_field: bool = False) -> list[Sprite]:
        return list(map(lambda _: Spawner.one(cls, on_field), range(amount)))

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
