import pygame_menu

from components.game import Game
from components.interfaces.resetable import Resetable
from components.overlay import Overlay
from config import Configuration as Conf
from sprites.player.rocket import Rocket
from sprites.player.ship import Ship
from utils.listener.events import Event, Device as Dvc, Keyboard as Kb, Gamepad as Gp
from utils.listener.listener import EventListener
from utils.mechanics.spawner import Spawner
from utils.resources.image import Image as Img
from utils.resources.sound import Sound as Snd


class Menu(Resetable):
    def __init__(self, window):
        # Environment
        self.window = window
        self.engine = pygame_menu.sound.Sound()
        self.title_font = "./resources/fonts/opensans.ttf"
        self.widget_font = "./resources/fonts/opensans-light.ttf"
        self.menu_settings = self.create_settings()
        self.menu_about = self.create_about()
        self.menu_main = self.create_menu(self.menu_settings, self.menu_about)

    def reset(self):
        self.menu_about = self.create_about()
        self.menu_settings = self.create_settings()
        self.menu_main = self.create_menu(self.menu_settings, self.menu_about)

    def create_about(self):
        """
        Create menus: About
        This function contains an about list that displays text on the screen.
        A separate about theme is created by copying the standard one,
        the theme is customized - the font of the title is changed.
        """
        ABOUT = [
            'INFO',
            '',
            'Game about violent fighting of the',
            'alone ship and hundreds of asteroids',
            '',
            '',
            f'Authors: {Conf.Menu.AUTHORS[0]}, {Conf.Menu.AUTHORS[1]}, {Conf.Menu.AUTHORS[2]}',
            f'Game version: {Conf.Menu.GAME_VERSION}',
        ]

        # Theme
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title_font = self.title_font
        theme.widget_font = self.widget_font
        theme.title_font_size = 56

        # Initialisation
        menu = pygame_menu.Menu(
            height=Conf.Window.HEIGHT,
            width=Conf.Window.WIDTH,
            onclose=pygame_menu.events.DISABLE_CLOSE,  # Action on closing
            theme=theme,  # Setting theme
            title='About'
        )

        # Layout
        for item in ABOUT:
            menu.add_label(item, font_size=40)

        return menu

    def create_settings(self):
        """
        Create menus: Settings
        This function contains an about list that displays text on the screen.
        A separate about theme is created by copying the standard one,
        the theme is customized - the font of the title is changed.
        """

        # Theme
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title_font = self.title_font
        theme.widget_font = self.widget_font
        theme.title_font_size = 56

        # Initialisation
        menu = pygame_menu.Menu(
            height=Conf.Window.HEIGHT,
            width=Conf.Window.WIDTH,
            onclose=pygame_menu.events.DISABLE_CLOSE,  # Action on closing
            theme=theme,  # Setting theme
            title='Settings'
        )

        # Layout
        menu.add_label("FPS")
        menu.add_selector(
            f'Limit:  ', items=[
                ("30", 30),
                ("60", 60),
                ("90", 90),
                ("120", 120)
            ], font_color=Conf.Menu.FONT_COLOR,
            default=Conf.System.FPS // 30 - 1,
            onchange=lambda _, value: Conf.change_fps(value)
        )
        menu.add_selector(
            f'Show:  ', items=[
                ("No", False),
                ("Yes", True)
            ], font_color=Conf.Menu.FONT_COLOR,
            default=1 if Conf.Overlay.Framerate.VISIBLE else 0,
            onchange=lambda _, value: Overlay.Framerate.toggle(value)
        )
        menu.add_label("Game settings")
        menu.add_selector(
            f'Meteor spawn:  ', items=[
                ("static", False),
                ("dynamic", True)
            ], font_color=Conf.Menu.FONT_COLOR,
            default=1 if Conf.Meteor.BY_TIME else 0,
            onchange=lambda _, value: Spawner.change_meteor_spawn_mode(value)
        )
        menu.add_selector(
            f'Difficulty:  ',
            items=Conf.Game.DIFFICULTY,
            default=2, font_color=Conf.Menu.FONT_COLOR,
            onchange=lambda _, value: Spawner.change_difficulty(value)
        )
        menu.add_label("Textures")
        menu.add_selector(
            f'Ship:  ',
            items=[(str(i), i) for i in range(Img.SHIPS_AMOUNT)],
            default=Ship.texture_num, font_color=Conf.Menu.FONT_COLOR,
            onchange=lambda _, value: Ship.set_texture_num(value)
        )
        menu.add_selector(
            f'Rocket:  ',
            items=[(str(i), i) for i in range(Img.ROCKETS_AMOUNT)],
            default=Rocket.texture_num, font_color=Conf.Menu.FONT_COLOR,
            onchange=lambda _, value: Rocket.set_texture_num(value)
        )
        menu.add_label("Volume")
        menu.add_selector(
            f'General:  ',
            items=[(str(i), i) for i in range(0, 11)],
            default=Conf.Sound.Volume.GENERAL, font_color=Conf.Menu.FONT_COLOR,
            onchange=lambda _, value: Snd.Volume.set_general(value)
        )
        menu.add_selector(
            f'Background:  ',
            items=[(str(i), i) for i in range(0, 11)],
            default=Conf.Sound.Volume.BG, font_color=Conf.Menu.FONT_COLOR,
            onchange=lambda _, value: Snd.Volume.set_bg(value)
        )
        menu.add_selector(
            f'SFX:  ',
            items=[(str(i), i) for i in range(0, 11)],
            default=Conf.Sound.Volume.SFX, font_color=Conf.Menu.FONT_COLOR,
            onchange=lambda _, value: Snd.Volume.set_sfx(value)
        )
        return menu

    def create_menu(self, settings, about):
        """
        Create menus: Main. Responsible for setting up the main menu.
        A picture is selected for the background. Customizable theme, colors, font size, etc.
        A name entry line is added, a play button that redirects to the start function of the game,
        similarly with the about and exit buttons.
        """
        # Theme
        theme = pygame_menu.themes.Theme(
            selection_color=Conf.Menu.THEME_COLOR,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,  # Separating header and body
            title_offset=(Conf.Menu.Title.X_OFFSET, Conf.Menu.Title.Y_OFFSET - 20),
            title_font=self.title_font,
            title_font_color=(255, 255, 255),
            title_font_size=Conf.Menu.Title.SIZE,
            background_color=Img.get_menu(),
            widget_font=self.widget_font,
            widget_font_color=(255, 255, 255),
            widget_font_size=40,
            widget_margin=(0, 40),
            menubar_close_button=False
        )
        # Initialisation
        menu = pygame_menu.Menu(
            Conf.Window.HEIGHT,
            Conf.Window.WIDTH,
            title='SPACE BATTLE',
            theme=theme,
            onclose=lambda: pygame_menu.events.DISABLE_CLOSE,
            mouse_motion_selection=True
        )
        # Layout
        menu.add_button('     Play     ', self.window.start, font_size=60, margin=(0, 50))
        menu.add_button('   Settings   ', settings)
        menu.add_button('     Info     ', about)
        menu.add_button('     Exit     ', self.window.exit)
        # Sound
        self.engine.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, Snd.click(),
                              volume=Snd.get_volume(Conf.Sound.Volume.SFX))
        menu.set_sound(self.engine, recursive=True)
        return menu

    def event_handler(self, events: dict[str, set[Event]]):
        for event in events[Dvc.KEYBOARD] | events[Dvc.GAMEPAD]:
            if (event.get_data() == Kb.Keys.ESC
                    or (event.get_type() == Gp.Events.KEY
                        and event.get_data() == Gp.Keys.START)):
                self.window.toggle_menu()

    def open(self):
        self.menu_main = self.create_menu(self.menu_settings, self.menu_about)
        self.menu_main.mainloop(self.window.screen, bgfun=lambda: self.event_handler(EventListener.get_events()))

    def close(self):
        self.menu_main.disable()
