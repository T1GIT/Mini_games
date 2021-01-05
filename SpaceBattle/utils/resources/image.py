import os
from threading import Thread
from time import time_ns

import numpy as np
import pygame as pg
import pygame_menu

from config import Configuration as Conf


class Image:
    """
    Class containing objects' images, already prepared for using
    """
    _ROOT = "./resources/images"
    _SHIPS: [[pg.Surface]] = None
    _ROCKETS: [pg.Surface] = None
    _METEORS: np.ndarray = None
    _BACKGROUND: pg.Surface = None
    _PIECES: [pg.Surface] = None
    _MENU: [pygame_menu.baseimage] = None
    _LIFE: pg.Surface = None
    _ANIMATIONS: {str: [pg.Surface]} = dict()

    SHIPS_AMOUNT = len([f for f in os.listdir("./resources/images/ship") if "raw" not in f])
    ROCKETS_AMOUNT = len([f for f in os.listdir("./resources/images/rocket")
                          if "raw" not in f and os.path.isfile(os.path.join("./resources/images/rocket", f))])
    METEORS_AMOUNT = len([f for f in os.listdir("./resources/images/meteor")
                          if "raw" not in f and os.path.isfile(os.path.join("./resources/images/meteor", f))])

    @staticmethod
    def get_menu() -> pygame_menu.baseimage.BaseImage:
        if Image._MENU is None:
            Image._MENU = pygame_menu.baseimage.BaseImage(
                image_path=f"{Image._ROOT}/bg/menu/{Conf.Image.MENU_BG}.{Conf.Image.Format.BASIC}")
        return Image._MENU

    @staticmethod
    def get_ship(with_fire: bool) -> pg.Surface:
        if Image._SHIPS is None:
            Image._SHIPS = []
            for x in range(Image.SHIPS_AMOUNT):
                Image._SHIPS.append([
                    pg.image.load(f"{Image._ROOT}/ship/{x}/normal.{Conf.Image.Format.SPRITE}").convert_alpha(),
                    pg.image.load(f"{Image._ROOT}/ship/{x}/fire.{Conf.Image.Format.SPRITE}").convert_alpha()
                ])
        return Image._SHIPS[Conf.Image.SHIP][1 if with_fire else 0]

    @staticmethod
    def get_meteors() -> np.ndarray:
        if Image._METEORS is None:
            pack = []
            path = f"{Image._ROOT}/meteor"
            for x in range(Image.METEORS_AMOUNT):
                pack.append(pg.image.load(f"{path}/{x}.{Conf.Image.Format.SPRITE}").convert_alpha())
            cnf = Conf.Meteor
            Image._METEORS = Image.get_cache_angles(pack, list(np.linspace(cnf.MIN_SIZE, cnf.MAX_SIZE, cnf.SIZES)))
        return Image._METEORS

    @staticmethod
    def get_rocket(model: int) -> pg.Surface:
        if Image._ROCKETS is None:
            Image._ROCKETS = []
            for x in range(Image.ROCKETS_AMOUNT):
                Image._ROCKETS.append(pg.image.load(
                    f"{Image._ROOT}/rocket/{x}.{Conf.Image.Format.SPRITE}").convert_alpha())
        return Image._ROCKETS[model]

    @staticmethod
    def get_life() -> pg.Surface:
        if Image._LIFE is None:
            Image._LIFE = pg.image.load(
                f"{Image._ROOT}/life/{Conf.Image.LIFE}.{Conf.Image.Format.SPRITE}").convert_alpha()
        return Image._LIFE

    @staticmethod
    def get_background() -> pg.Surface:
        if Image._BACKGROUND is None:
            Image._BACKGROUND = pg.image.load(
                f"{Image._ROOT}/bg/static/{Conf.Image.STATIC_BG}.{Conf.Image.Format.BASIC}").convert()
        return Image._BACKGROUND

    @staticmethod
    def get_animation(name: str) -> [pg.Surface]:
        if name not in Image._ANIMATIONS:
            pack = []
            path = f"{Image._ROOT}/anim/{name}"
            for frame in range(len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])):
                pack.append(pg.image.load(f"{path}/{frame}.{Conf.Image.Format.ANIM}").convert_alpha())
            Image._ANIMATIONS.update({name: pack})
        return Image._ANIMATIONS[name]

    @staticmethod
    def get_pieces() -> [pg.Surface]:
        if Image._PIECES is None:
            Image._PIECES = []
            path = f"{Image._ROOT}/piece"
            for x in range(len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])):
                Image._PIECES.append(pg.image.load(f"{path}/{x}.{Conf.Image.Format.SPRITE}").convert_alpha())
        return Image._PIECES

    @staticmethod
    def preload(func: callable):
        def preload_inside():
            print("Caching started ...")
            t = time_ns()
            Image.get_menu()
            Image.get_ship(True)
            Image.get_rocket(0)
            Image.get_life()
            Image.get_background()
            Image.get_meteors()
            Image.get_animation("ship")
            Image.get_animation("meteor")
            Image.get_pieces()
            print(f"Caching took {round((time_ns() - t) / 1e6, 2)} ms")
            func()
        Thread(target=preload_inside).start()

    @staticmethod
    def get_cache_angles(textures: list[pg.Surface], sizes: list[int]) -> np.ndarray:
        res = np.zeros((len(textures), len(sizes), 181), dtype=pg.Surface)
        for img_i, img in enumerate(textures):
            img_ar = res[img_i]
            for size_i, size in enumerate(sizes):
                size_ar = img_ar[size_i]
                scaled_img = Image.scale(img, size)
                for angle in range(181):
                    size_ar[angle] = pg.transform.rotate(scaled_img, angle)
        return res

    @staticmethod
    def get_cache_by_angle(cache: np.ndarray, model: int, size: int, angle: int):
        if angle <= 180:
            return cache[model][size][angle]
        else:
            return pg.transform.flip(cache[model][size][angle - 180], True, True)

    @staticmethod
    def scale(texture: pg.Surface, size: float) -> pg.Surface:
        width, height = map(lambda x: round(x * size / max(texture.get_size())), texture.get_size())
        return pg.transform.scale(texture, (width, height))
