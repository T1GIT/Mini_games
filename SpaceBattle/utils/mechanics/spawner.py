import random as rnd

from config import Configuration as Conf
from sprites.interfaces.basic import Sprite, Movable, Group
from sprites.interfaces.extended import Spawnable, Groupable
from sprites.loot.bonuses import Heal
from sprites.mobs.meteor import Meteor
from sprites.effects.piece import Piece
from utils.tools.groups import Groups


class Spawner(Groupable):
    def __init__(self, cls):
        super().__init__()
        self.cls = cls

    def spawn(self, amount: int = 1) -> tuple[Sprite]:
        sprite_list: list[Sprite] = []
        for _ in range(amount):
            sprite: Spawnable = self.cls()
            sprite.spawn()
            sprite_list.append(sprite)
        self.group.add(*sprite_list)
        return tuple(sprite_list)
