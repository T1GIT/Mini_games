import os
import random as rnd

import numpy as np
import pygame as pg
import pygame_menu

from config import Configuration as Conf


class Image:
    """
    Class containing objects' images, already prepared for using
    """
    _ROOT = "./resources/images"
    _SHIPS = None
    _ROCKETS = None
    _METEORS = None
    _BACKGROUND = None
    _PIECES = None
    _MENU = None
    _LIFE = None
    _ANIMATIONS = dict()

    SHIPS_AMOUNT = len([f for f in os.listdir("./resources/images/ship") if "raw" not in f])
    ROCKETS_AMOUNT = len([f for f in os.listdir("./resources/images/rocket")
                          if "raw" not in f and os.path.isfile(os.path.join("./resources/images/rocket", f))])
    _METEORS_AMOUNT = len([f for f in os.listdir("./resources/images/meteor")
                           if "raw" not in f and os.path.isfile(os.path.join("./resources/images/meteor", f))])

    @staticmethod
    def get_menu() -> pygame_menu.baseimage.BaseImage:
        if Image._MENU is None:
            Image._MENU = pygame_menu.baseimage.BaseImage(
                image_path=f"{Image._ROOT}/bg/menu/{Conf.Image.MENU_BG}.{Conf.Image.BASIC_FORMAT}")
        return Image._MENU

    @staticmethod
    def get_ship(with_fire: bool) -> pg.Surface:
        if Image._SHIPS is None:
            Image._SHIPS = []
            for x in range(Image.SHIPS_AMOUNT):
                Image._SHIPS.append([
                    pg.image.load(f"{Image._ROOT}/ship/{x}/normal.{Conf.Image.SPRITE_FORMAT}").convert_alpha(),
                    pg.image.load(f"{Image._ROOT}/ship/{x}/fire.{Conf.Image.SPRITE_FORMAT}").convert_alpha()
                ])
        return Image._SHIPS[Conf.Image.SHIP][1 if with_fire else 0]

    @staticmethod
    def get_rocket() -> pg.Surface:
        if Image._ROCKETS is None:
            Image._ROCKETS = []
            for x in range(Image.ROCKETS_AMOUNT):
                Image._ROCKETS.append(pg.image.load(
                    f"{Image._ROOT}/rocket/{x}.{Conf.Image.SPRITE_FORMAT}").convert_alpha())
        return Image._ROCKETS[Conf.Image.ROCKET]

    @staticmethod
    def get_life() -> pg.Surface:
        if Image._LIFE is None:
            Image._LIFE = pg.image.load(
                f"{Image._ROOT}/life/{Conf.Image.LIFE}.{Conf.Image.SPRITE_FORMAT}").convert_alpha()
        return Image._LIFE

    @staticmethod
    def get_background() -> pg.Surface:
        if Image._BACKGROUND is None:
            Image._BACKGROUND = pg.image.load(
                f"{Image._ROOT}/bg/static/{Conf.Image.STATIC_BG}.{Conf.Image.BASIC_FORMAT}").convert()
        return Image._BACKGROUND

    @staticmethod
    def get_meteors():
        if Image._METEORS is None:
            pack = []
            path = f"{Image._ROOT}/meteor"
            for x in range(Image._METEORS_AMOUNT):
                pack.append(pg.image.load(f"{path}/{x}.{Conf.Image.SPRITE_FORMAT}").convert_alpha())
            size_del = (Conf.Meteor.MAX_SIZE - Conf.Meteor.MIN_SIZE) / Conf.Meteor.SIZES
            Image._METEORS = np.zeros((Image._METEORS_AMOUNT, Conf.Meteor.SIZES, 181), dtype=pg.Surface)
            for i, img in enumerate(pack):
                img_ar = Image._METEORS[i]
                for size in range(Conf.Meteor.SIZES):
                    size_ar = img_ar[size]
                    scaled_img = Image.scale(img, Conf.Meteor.MIN_SIZE + size_del * size)
                    for angle in range(181):
                        size_ar[angle] = pg.transform.rotate(scaled_img, angle)
        return Image._METEORS

    @staticmethod
    def get_animation(name: str) -> [pg.Surface]:
        if name not in Image._ANIMATIONS:
            pack = []
            path = f"{Image._ROOT}/anim/{name}"
            for frame in range(len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])):
                pack.append(pg.image.load(f"{path}/{frame}.{Conf.Image.ANIM_FORMAT}").convert_alpha())
            Image._ANIMATIONS.update({name: pack})
        return Image._ANIMATIONS[name]

    @staticmethod
    def get_pieces() -> [pg.Surface]:
        if Image._PIECES is None:
            Image._PIECES = []
            path = f"{Image._ROOT}/piece"
            for x in range(len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])):
                Image._PIECES.append(pg.image.load(f"{path}/{x}.{Conf.Image.SPRITE_FORMAT}").convert_alpha())
        return Image._PIECES

    @staticmethod
    def cache():
        Image.get_menu()
        Image.get_ship(True)
        Image.get_rocket()
        Image.get_life()
        Image.get_background()
        Image.get_meteors()
        Image.get_animation("ship")
        Image.get_pieces()

    @staticmethod
    def scale(texture: pg.Surface, size: float) -> pg.Surface:
        width, height = map(lambda x: round(x * size / max(texture.get_size())), texture.get_size())
        return pg.transform.scale(texture, (width, height))
