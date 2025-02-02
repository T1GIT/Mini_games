import pygame as pg

from config import Configuration as Conf


class Sound:
    """
    Class playing sounds of the game
    """
    _ROOT = "./resources/sounds"
    _VOLUME = Conf.Sound.Volume
    SFX_DICT: dict[str: pg.mixer.Sound] = dict()

    """
    BACKGROUND
    """
    @staticmethod
    def _play_bg(path: str, pos: int = 0):
        pg.mixer.stop()
        pg.mixer.music.load(
            f'{Sound._ROOT}/background/{path}.{Conf.Sound.FORMAT}')
        pg.mixer.music.set_volume(Sound.get_volume(Sound._VOLUME.BG))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_pos(pos)

    @staticmethod
    def bg_menu(): Sound._play_bg(f"menu/{Conf.Sound.BG_MENU}", 10)

    @staticmethod
    def bg_game(): Sound._play_bg(f"game/{Conf.Sound.BG_GAME}")

    @staticmethod
    def game_over(): Sound._play_bg("game_over")

    """
    SFX
    """
    @staticmethod
    def _play_sfx(path: str, volume: float = 1):
        if path not in Sound.SFX_DICT:
            Sound.SFX_DICT[path] = pg.mixer.Sound(
                f'{Sound._ROOT}/sfx/{path}.{Conf.Sound.FORMAT}')
            Sound.SFX_DICT[path].set_volume(Sound.get_volume(Sound._VOLUME.SFX) * volume)
        Sound.SFX_DICT[path].stop()
        Sound.SFX_DICT[path].play()

    @staticmethod
    def click(): Sound._play_sfx(f"click/{Conf.Sound.CLICK}")  # TODO: add sound to the menu

    @staticmethod
    def shoot(): Sound._play_sfx(f"shoot/{Conf.Sound.SHOOT}", 0.7)

    @staticmethod
    def heal(): Sound._play_sfx(f"heal", 1.4)

    @staticmethod
    def wound(): Sound._play_sfx("wound")

    @staticmethod
    def engine(): Sound._play_sfx("engine")

    @staticmethod
    def ex_ship(): Sound._play_sfx("explode/ship")

    @staticmethod
    def ex_meteor(): Sound._play_sfx("explode/meteor", 2)

    @staticmethod
    def get_volume(volume: float) -> float:
        return volume * Conf.Sound.Volume.GENERAL / 100
