import pygame as pg

from config import Configuration as Conf
from sprites.animation import Animation
from sprites.meteor import Meteor
from sprites.ship import Ship
from utils.tools.group import Group
from utils.resources.sound import Sound as Snd


class Collider:
    @staticmethod
    def ship_meteors(ship: Ship):
        """
        Checks the collision of a meteor and a ship.
        Causes an explosion animation if a collision occurs
        """
        touched = pg.sprite.spritecollide(ship, Group.METEORS, False)
        result = 0
        for meteor in touched:
            if Collider.collide_by_mask(ship, meteor):
                Snd.wound()
                Animation.on_sprite("meteor", meteor, max(meteor.rect.size))
                meteor.kill()
                result += 1
        return result

    @staticmethod
    def rockets_meteors():
        """
        Checks the collision of a meteor and a rocket.
        Causes an explosion animation if a collision occurs
        """
        touched = pg.sprite.groupcollide(Group.METEORS, Group.ROCKETS, False, False)
        result = 0
        meteor: Meteor
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
    def collide_by_mask(sprite1: pg.sprite.Sprite, sprite2: pg.sprite.Sprite):
        mask1 = pg.mask.from_surface(sprite1.image)
        mask2 = pg.mask.from_surface(sprite2.image)
        offset = (sprite2.rect.x - sprite1.rect.x, sprite2.rect.y - sprite1.rect.y)
        return mask1.overlap_area(mask2, offset) > 0
