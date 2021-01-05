from ctypes import windll

import pygame as pg

from components.game import Game
from components.interfaces.resetable import Resetable
from components.menu import Menu
from config import Configuration as Conf
from utils.resources.image import Image as Img
from utils.resources.sound import Sound as Snd
from utils.tools.exceptions import GameOverException, NewGameException
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
        self.new_game = False
        self.started = False
        self.paused = False
        self.ready = False

    def reset(self):
        self.comp_game.reset()
        self.comp_menu.reset()
        self.started = False
        self.paused = False

    def toggle_menu(self):
        if self.started and self.escape_timer.is_ready():
            if not self.paused and self.comp_game.game_over:
                self.reset()
            self.paused = not self.paused
            self.toggle_mouse(self.paused)
            self.escape_timer.start()
            Snd.bg_menu() if self.paused else Snd.bg_game()
            self.comp_menu.open() if self.paused else self.comp_menu.close()
            self.toggle_mouse(self.paused)

    def start(self):
        if self.ready:
            self.comp_menu.close()
            if self.started:
                raise NewGameException()
            else:
                self.toggle_mouse(False)
                Snd.bg_game()
                self.started = True
                try:
                    self.comp_game.start()
                except GameOverException:
                    pass
                except NewGameException:
                    self.new_game = True

    def show(self):
        def finish():
            self.ready = True
        Img.preload(finish)
        while True:
            if self.new_game:
                self.new_game = False
                self.start()
            else:
                Snd.bg_menu()
                self.toggle_mouse(True)
                self.comp_menu.open()
            self.reset()

    def exit(self):
        if self.ready:
            exit()

    @staticmethod
    def toggle_mouse(value: bool):
        pg.mouse.set_visible(value)
        pg.event.set_grab(not value)
