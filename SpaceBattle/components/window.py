from ctypes import windll

import pygame as pg

from components.game import Game
from components.menu import Menu
from components.resetable import Resetable
from config import Configuration as Conf
from utils.resources.image import Image as Img
from utils.tools.exceptions import GameOverException
from utils.tools.group import Group
from utils.tools.timer import Timer


class Window(Resetable):
    """
    Class for show the main window.
    Initials the Game.
    Start listener
    """

    def __init__(self):
        # Initialisation
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(Conf.Window.TITLE)
        if Conf.Window.FULLSCREEN:
            user32 = windll.user32
            Conf.Window.WIDTH = user32.GetSystemMetrics(0)
            Conf.Window.HEIGHT = user32.GetSystemMetrics(1)
        self.screen = pg.display.set_mode((Conf.Window.WIDTH, Conf.Window.HEIGHT))
        # Components
        self.comp_game = Game(self)
        self.comp_menu = Menu(self)
        # Variables
        self.escape_timer: Timer = Timer(Conf.Control.ESC_PERIOD)
        # Flags
        self.started = False
        self.paused = False

    def reset(self):
        map(lambda sprite: sprite.kill(), Group.ALL)
        self.comp_game.reset()
        self.comp_menu.reset()
        self.started = False
        self.paused = False

    def toggle_menu(self):
        if self.started and self.escape_timer.is_ready():
            if self.paused:
                pg.mouse.set_visible(False)
                pg.event.set_grab(True)
                self.comp_menu.close()
                self.paused = False
            else:
                pg.mouse.set_visible(True)
                pg.event.set_grab(False)
                self.comp_menu.open()
            self.paused = not self.paused
            self.escape_timer.start()

    def start(self):
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        self.started = True
        self.comp_game.start()

    def show(self):
        Img.preload()
        self.comp_menu.open()
