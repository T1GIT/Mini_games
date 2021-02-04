import pygame_menu

from components.settings import Settings
from components.interfaces.resetable import Resetable
from config import Configuration as Conf
from utils.listener.events import Event, Device as Dvc, Keyboard as Kb, Gamepad as Gp
from utils.listener.listener import EventListener
from utils.resources.image import Image as Img


class Menu(Resetable):
    def __init__(self, window, settings):
        # Environment
        self.window = window
        self.settings = settings
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
        s_items = Settings.Items
        s_def = Settings.Default
        menu.add_label("FPS")
        menu.add_selector(
            f'Limit:  ', items=s_items.Fps.limit, font_color=Conf.Menu.FONT_COLOR,
            default=s_def.Fps.limit, onchange=lambda _, value: self.settings.fps_limit(value)
        )
        menu.add_selector(
            f'Show:  ', items=s_items.Fps.show, font_color=Conf.Menu.FONT_COLOR,
            default=s_def.Fps.show, onchange=lambda _, value: self.settings.fps_show(value)
        )
        menu.add_label("GAME")
        menu.add_selector(
            f'Spawn:  ', items=s_items.Game.spawn, font_color=Conf.Menu.FONT_COLOR,
            default=s_def.Game.spawn, onchange=lambda _, value: self.settings.game_spawn(value)
        )
        menu.add_selector(
            f'Difficulty:  ', items=s_items.Game.difficulty, font_color=Conf.Menu.FONT_COLOR,
            default=s_def.Game.difficulty, onchange=lambda _, value: self.settings.game_difficulty(value)
        )
        menu.add_label("SKIN")
        menu.add_selector(
            f'Ship:  ', items=s_items.Skin.ship, font_color=Conf.Menu.FONT_COLOR,
            default=s_def.Skin.ship, onchange=lambda _, value: self.settings.skin_ship(value)
        )
        menu.add_selector(
            f'Rocket:  ', items=s_items.Skin.rocket, font_color=Conf.Menu.FONT_COLOR,
            default=s_def.Skin.rocket,  onchange=lambda _, value: self.settings.skin_rocket(value)
        )
        menu.add_label("VOLUME")
        menu.add_selector(
            f'General:  ', items=s_items.Volume.general, font_color=Conf.Menu.FONT_COLOR,
            default=s_def.Volume.general, onchange=lambda _, value: self.settings.volume_general(value)
        )
        menu.add_selector(
            f'Background:  ', items=s_items.Volume.background, font_color=Conf.Menu.FONT_COLOR,
            default=s_def.Volume.background, onchange=lambda _, value: self.settings.volume_background(value)
        )
        menu.add_selector(
            f'Effects:  ', items=s_items.Volume.effects, font_color=Conf.Menu.FONT_COLOR,
            default=s_def.Volume.effects, onchange=lambda _, value: self.settings.volume_effects(value)
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
