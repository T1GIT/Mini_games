import pygame as pg

from components.interfaces.resetable import Resetable
from config import Configuration as Conf
from utils.resources.image import Image as Img
from utils.resources.sound import Sound as Snd
from utils.tools.groups import Groups


class Settings(Resetable):
    class Items:
        class Fps:
            limit = list(map(lambda x: (str(x), x), range(30, 31 + 30 * 3, 30)))
            show = [("no", False), ("yes", True)]

        class Game:
            spawn = [("static", False), ("dynamic", True)]
            difficulty = list(map(
                lambda name, params: (name, params),
                ["novice", "easy", "normal", "hard", "DEATH"],
                zip(range(500, 501 + 150 * 4, 150), range(10, 11 + 10 * 4, 10))
            ))

        class Skin:
            ship = [(str(i), i) for i in range(Img.SHIPS_AMOUNT)]
            rocket = [(str(i), i) for i in range(Img.ROCKETS_AMOUNT)]

        class Volume:
            general = [(str(i), i) for i in range(11)]
            background = [(str(i), i) for i in range(11)]
            effects = [(str(i), i) for i in range(11)]

    class Default:
        class Fps:
            limit = Conf.System.FPS // 30 - 1
            show = 1 if Conf.Overlay.Framerate.VISIBLE else 0

        class Game:
            spawn = 1 if Conf.Meteor.BY_TIME else 0
            difficulty = 2

        class Skin:
            ship = Conf.Image.SHIP
            rocket = Conf.Image.ROCKET

        class Volume:
            general = Conf.Sound.Volume.GENERAL
            background = Conf.Sound.Volume.BG
            effects = Conf.Sound.Volume.SFX

    def __init__(self, window):
        self.window = window

    def fps_limit(self, value: int):
        Conf.System.FPS = value
        Conf.System.SCALE = Conf.System.GAME_SPEED / value

    def fps_show(self, value: bool):
        if value:
            self.window.comp_game.comp_overlay.framerate.set_opacity(Conf.Overlay.OPACITY)
        else:
            self.window.comp_game.comp_overlay.framerate.set_opacity(0)

    def game_spawn(self, value: int):
        Conf.Meteor.BY_TIME = bool(value)

    def game_difficulty(self, value: tuple[int, int]):
        Conf.Meteor.PERIOD = value[0]
        Conf.Meteor.QUANTITY = value[1]
        self.window.comp_game.meteor_timer.set_time(Conf.Meteor.PERIOD)

    def skin_ship(self, value: int):
        Conf.Image.SHIP = value
        self.window.comp_game.ship.set_texture((
            Img.scale(Img.get_ship(value, False), Conf.Ship.SIZE),
            Img.scale(Img.get_ship(value, True), Conf.Ship.SIZE)
        ))

    def skin_rocket(self, value: int):
        Conf.Image.ROCKET = value
        for rocket in Groups.ROCKETS:
            rocket.set_texture(Img.scale(Img.get_rocket(value), Conf.Rocket.SIZE))

    def volume_general(self, value):
        Conf.Sound.Volume.GENERAL = value
        self.volume_background(Conf.Sound.Volume.BG)
        self.volume_effects(Conf.Sound.Volume.SFX)

    def volume_background(self, value):
        Conf.Sound.Volume.BG = value
        pg.mixer.music.set_volume(Snd.get_volume(value))

    def volume_effects(self, value):
        Conf.Sound.Volume.SFX = value
        for sound in Snd.SFX_DICT.values():
            sound.set_volume(Snd.get_volume(value))
