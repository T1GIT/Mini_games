
import pygame as pg

from config import Configuration as Conf
from sprites.effects.animation import Animation
from sprites.interfaces.basic import Group
from sprites.mobs.meteor import Meteor
from sprites.player.rocket import Rocket
from sprites.player.ship import Ship
from utils.resources.sound import Sound as Snd
from utils.tools.groups import Groups


class Collider:
    @staticmethod
    def ship_to_group(ship: Ship, group: Group, sound, anim_name: str, anim_size: float = None) -> int:
        touched = pg.sprite.spritecollide(ship, group, False)
        result = 0
        for sprite in touched:
            if Collider.collide_by_mask(ship, sprite):
                sound()
                if anim_size is None:
                    Animation.on_sprite(anim_name, sprite, max(sprite.get_size()))
                else:
                    Animation.on_sprite(anim_name, sprite, anim_size)
                sprite.kill()
                result += 1
        return result

    @staticmethod
    def rockets_meteors() -> int:
        """
        Checks the collision of a meteor and a rocket.
        Causes an explosion animation if a collision occurs
        """
        touched: dict[Meteor, list[Rocket]] = pg.sprite.groupcollide(Groups.METEORS, Groups.ROCKETS, False, False)
        result = 0
        for meteor, rockets in touched.items():
            for rocket in rockets:
                if Collider.collide_by_mask(meteor, rocket):
                    if meteor.is_alive():
                        meteor.wound()
                        Animation.on_sprite("meteor", rocket, max(meteor.rect.size) / 2)
                    else:
                        Snd.ex_meteor()
                        Animation.on_sprite("meteor", meteor, max(meteor.rect.size))
                        meteor.kill()
                        result += 1
                    if Conf.Rocket.DESTROYABLE:
                        rocket.kill()
        return result

    @staticmethod
    def collide_by_mask(sprite1: pg.sprite.Sprite, sprite2: pg.sprite.Sprite) -> bool:
        mask1 = pg.mask.from_surface(sprite1.image)
        mask2 = pg.mask.from_surface(sprite2.image)
        offset = (sprite2.rect.x - sprite1.rect.x, sprite2.rect.y - sprite1.rect.y)
        return mask1.overlap_area(mask2, offset) > 0
