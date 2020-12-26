from ctypes import windll
from threading import Thread
from time import time_ns

import pygame as pg

from components.abstractComponent import AbstractComponent
from components.game import Game
from components.menu import Menu
from config import Configuration as Conf
from utils.tools.group import Group
from utils.resources.sound import Sound as Snd
from utils.resources.image import Image as Img


class Window(AbstractComponent):
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
        self.esc_timer = time_ns()
        # Flags
        self.started = False

    def reset(self):
        for sprite in Group.ALL:
            sprite.kill()
        self.started = False
        self.comp_game.reset()

    def pause(self):
        if time_ns() - self.esc_timer > Conf.Control.ESC_PERIOD * 1e6:
            self.esc_timer = time_ns()
            self.open_menu()

    def play(self):
        if time_ns() - self.esc_timer > Conf.Control.ESC_PERIOD * 1e6 and self.started:
            self.esc_timer = time_ns()
            self.close_menu()

    def open_menu(self):
        pg.mixer.stop()
        Snd.bg_menu()
        pg.event.set_grab(False)
        self.comp_menu.open()
        pg.mouse.set_visible(False)

    def close_menu(self):
        pg.mixer.stop()
        Snd.bg_game()
        self.comp_menu.close()
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)

    def start(self):
        if self.started:
            self.reset()
        self.started = True
        self.close_menu()
        self.comp_game.start()

    def show(self):
        Img.cache()
        Snd.bg_menu()
        self.comp_menu.open()
