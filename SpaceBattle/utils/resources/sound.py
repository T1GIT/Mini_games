import pygame as pg

from config import Configuration as Conf


class Sound:
    """
    Class playing sounds of the game
    """
    _ROOT = "./resources/sounds"
    _VOLUME = Conf.Sound.Volume
    _SHOOT = None
    _EX_SHIP = None
    _EX_METEOR = None
    _WOUND = None
    _ENGINE = None
    _GAME_OVER = None

    @staticmethod
    def get_volume(volume: float) -> float:
        return volume * Conf.Sound.Volume.GENERAL / 100

    """
    BACKGROUND
    """
    @staticmethod
    def bg_menu():
        pg.mixer.music.load(
            f'{Sound._ROOT}/background/menu/{Conf.Sound.BG_MENU}.{Conf.Sound.FORMAT}')
        pg.mixer.music.set_volume(Sound.get_volume(Sound._VOLUME.BG))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_pos(10)

    @staticmethod
    def bg_game():
        pg.mixer.music.load(
            f'{Sound._ROOT}/background/game/{Conf.Sound.BG_GAME}.{Conf.Sound.FORMAT}')
        pg.mixer.music.set_volume(Sound.get_volume(Sound._VOLUME.BG))
        pg.mixer.music.play(-1)

    @staticmethod
    def game_over():
        pg.mixer.music.load(f'{Sound._ROOT}/sfx/game_over.{Conf.Sound.FORMAT}')
        pg.mixer.music.set_volume(Sound.get_volume(Sound._VOLUME.BG))
        pg.mixer.music.play()

    """
    SFX
    """
    @staticmethod
    def click():
        return f"{Sound._ROOT}/sfx/click/{Conf.Sound.CLICK}.{Conf.Sound.FORMAT}"

    @staticmethod
    def shoot():
        if Sound._SHOOT is None:
            Sound._SHOOT = pg.mixer.Sound(
                f'{Sound._ROOT}/sfx/shoot/{Conf.Sound.SHOOT}.{Conf.Sound.FORMAT}')
            Sound._SHOOT.set_volume(Sound.get_volume(Sound._VOLUME.SFX))
        Sound._SHOOT.stop()
        Sound._SHOOT.play()

    @staticmethod
    def wound():
        if Sound._WOUND is None:
            Sound._WOUND = pg.mixer.Sound(f'{Sound._ROOT}/sfx/wound.{Conf.Sound.FORMAT}')
            Sound._WOUND.set_volume(Sound.get_volume(Sound._VOLUME.SFX))
        Sound._WOUND.stop()
        Sound._WOUND.play()

    @staticmethod
    def engine():
        if Sound._ENGINE is None:
            Sound._ENGINE = pg.mixer.Sound(f'{Sound._ROOT}/sfx/engine.{Conf.Sound.FORMAT}')
            Sound._ENGINE.set_volume(Sound.get_volume(Sound._VOLUME.SFX))
        Sound._ENGINE.stop()
        Sound._ENGINE.play()

    @staticmethod
    def ex_ship():
        if Sound._EX_SHIP is None:
            Sound._EX_SHIP = pg.mixer.Sound(f'{Sound._ROOT}/sfx/explode/ship.{Conf.Sound.FORMAT}')
            Sound._EX_SHIP.set_volume(Sound.get_volume(Sound._VOLUME.SFX))
        Sound._EX_SHIP.stop()
        Sound._EX_SHIP.play()

    @staticmethod
    def ex_meteor():
        if Sound._EX_METEOR is None:
            Sound._EX_METEOR = pg.mixer.Sound(f'{Sound._ROOT}/sfx/explode/meteor.{Conf.Sound.FORMAT}')
            Sound._EX_METEOR.set_volume(Sound.get_volume(Sound._VOLUME.SFX))
        Sound._EX_METEOR.stop()
        Sound._EX_METEOR.play()

    class Volume:
        @staticmethod
        def set_general(level: int):
            Conf.Sound.Volume.GENERAL = level
            if Sound._SHOOT is not None:
                Sound._SHOOT.set_volume(Sound.get_volume(Conf.Sound.Volume.SFX))
            if Sound._EX_SHIP is not None:
                Sound._EX_SHIP.set_volume(Sound.get_volume(Conf.Sound.Volume.SFX))
            if Sound._EX_METEOR is not None:
                Sound._EX_METEOR.set_volume(Sound.get_volume(Conf.Sound.Volume.SFX))
            pg.mixer.music.set_volume(Sound.get_volume(Conf.Sound.Volume.BG))

        @staticmethod
        def set_sfx(level: int):
            Conf.Sound.Volume.SFX = level
            if Sound._SHOOT is not None:
                Sound._SHOOT.set_volume(Sound.get_volume(level))
            if Sound._EX_SHIP is not None:
                Sound._EX_SHIP.set_volume(Sound.get_volume(level))
            if Sound._EX_METEOR is not None:
                Sound._EX_METEOR.set_volume(Sound.get_volume(level))

        @staticmethod
        def set_bg(level: int):
            Conf.Sound.Volume.BG = level
            pg.mixer.music.set_volume(Sound.get_volume(level))
