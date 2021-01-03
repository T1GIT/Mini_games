import pygame as pg

from components.interfaces.resetable import Resetable
from components.overlay import Overlay
from config import Configuration as Conf
from sprites.animation import Animation
from sprites.ship import Ship
from utils.listener.events import Keyboard as Kb, Gamepad as Gp, Mouse as Ms, Device as Dvc, System as Sys, Event
from utils.listener.listener import EventListener
from utils.mechanics.collider import Collider
from utils.mechanics.spawner import Spawner
from utils.resources.image import Image as Img
from utils.resources.sound import Sound as Snd
from utils.tools.groups import Groups
from utils.tools.timer import Timer


class Game(Resetable):
    """
    Class which initials the game.
    Spawns meteors.
    Catches events and redirect to the ship
    """

    def __init__(self, window):
        # Environment
        self.window = window
        self.game_over_flag: bool = False
        self.clock: pg.time.Clock = pg.time.Clock()
        self.running: bool = False
        # Components
        self.comp_overlay: Overlay = Overlay(self)
        # Sprites
        self.ship: Ship = Ship()
        # Timers
        self.meteor_timer = Timer(Conf.Meteor.PERIOD)
        self.rocket_timer = Timer(Conf.Rocket.PERIOD)
        self.losing_timer = Timer(Conf.Game.LOSE_DELAY)
        self.frames_timer = Timer(Conf.Overlay.Framerate.PERIOD)
        # Background
        w0, h0 = Img.get_background().get_size()
        tar_size = max(w0, h0) * max((Conf.Window.WIDTH / w0, Conf.Window.HEIGHT / h0))
        self.background = Img.scale(Img.get_background(), tar_size)

    def reset(self):
        """
        Erases all mobs and objects
        """
        self.comp_overlay.reset()
        Groups.METEORS.kill()
        Groups.ROCKETS.kill()
        Groups.PIECES.kill()
        self.ship.kill()
        self.ship = Ship()
        self.game_over_flag = False
        self.running = False

    def start(self):
        """
        Starts the game
        """
        self.game_over_flag = False
        self.comp_overlay.show()
        self.ship.add(Groups.ALL)
        self.ship.locate(Conf.Window.WIDTH // 2, Conf.Window.HEIGHT // 2)
        Groups.ALL.add(self.ship)
        if not Conf.Meteor.BY_TIME:
            Spawner.all_meteors()
        Spawner.all_pieces(True)
        self.running = True
        self.mainloop()

    def lose(self):
        if not self.game_over_flag:
            Snd.ex_ship()
            Animation.on_sprite("ship", self.ship, max(self.ship.rect.size) * Conf.Ship.ANIM_SCALE)
            self.ship.kill()
            self.losing_timer.start()
            self.game_over_flag = True
            Snd.game_over()

    def event_handler(self, events: [Event]):
        """
        Does action from event name
        :param events
        """
        x, y = 0, 0
        shoot = False
        kb_self_distract = [False, False]
        gp_self_distract = [False, False]
        for event in events.get(Dvc.SYSTEM, ()):
            if event.get_type() == Sys.Events.QUIT:
                self.window.exit()
        for event in events.get(Dvc.MOUSE, ()):
            if event.get_type() == Ms.Events.MOVE:
                self.ship.vector_rotate(*event.get_data(), True)
            if event.get_type() == Ms.Events.KEY and event.get_data() == Ms.Keys.LEFT:
                shoot = True
        for event in events.get(Dvc.KEYBOARD, ()):
            if event.get_data() in (Kb.Keys.W, Kb.Keys.UP):       y += 1
            if event.get_data() in (Kb.Keys.A, Kb.Keys.LEFT):     x -= 1
            if event.get_data() in (Kb.Keys.S, Kb.Keys.DOWN):     y -= 1
            if event.get_data() in (Kb.Keys.D, Kb.Keys.RIGHT):    x += 1
            if event.get_data() == Kb.Keys.ESC: self.window.toggle_menu()
            if event.get_data() == Kb.Keys.SPACE: kb_self_distract[0] = True
            if event.get_data() == Kb.Keys.ENTER: kb_self_distract[1] = True
        for event in events.get(Dvc.GAMEPAD, ()):
            if event.get_type() == Gp.Events.LS:    x, y = event.get_data()
            if event.get_type() == Gp.Events.RS:    self.ship.vector_rotate(*event.get_data(), False)
            if event.get_type() == Gp.Events.KEY:
                if event.get_data() == Gp.Keys.RT: shoot = True
                if event.get_data() == Gp.Keys.START: self.window.toggle_menu()
                if event.get_data() == Gp.Keys.LS: gp_self_distract[0] = True
                if event.get_data() == Gp.Keys.RS: gp_self_distract[1] = True
        if not self.game_over_flag:
            # Checking self-destruction
            if kb_self_distract == [True, True] or gp_self_distract == [True, True]:
                self.lose()
            # Shooting
            if self.rocket_timer.is_ready() and shoot:
                self.rocket_timer.start()
                self.ship.shoot()
            # Moving
            self.ship.vector_accelerate(x, y)

    def mainloop(self):
        while self.running:
            events = EventListener.get_events()
            if self.game_over_flag: events = {Dvc.SYSTEM: events[Dvc.SYSTEM]}
            self.event_handler(events)
            pg.event.get()
            Groups.ALL.update()
            self.window.screen.blit(self.background, self.background.get_rect())
            Groups.ALL.draw(self.window.screen)
            pg.display.flip()
            self.preparation()
            self.clock.tick(Conf.System.FPS)

    def preparation(self):
        """
        Do all actions per one frame
        """
        # Colliding
        if not self.game_over_flag:
            if self.comp_overlay.health.is_dead():
                self.lose()
            else:
                hits = Collider.rockets_meteors()
                wounds = Collider.ship_meteors(self.ship)
                self.comp_overlay.score.up(hits)
                self.comp_overlay.health.down(wounds)
        # Spawning
        if Conf.Meteor.BY_TIME:
            if self.meteor_timer.is_ready():
                self.meteor_timer.start()
                Spawner.meteor()
        else: Spawner.all_meteors()
        Spawner.all_pieces(False)
        # Refreshing framerate
        self.comp_overlay.framerate.add_frame()
        if self.frames_timer.is_ready() and Conf.Overlay.Framerate.VISIBLE:
            self.frames_timer.start()
            self.comp_overlay.framerate.refresh()
        # Checking death
        if self.game_over_flag:
            if self.losing_timer.is_ready():
                self.running = False

    @staticmethod
    def change_fps(value: int):
        Conf.System.FPS = value
        Conf.System.SCALE = Conf.System.GAME_SPEED / value
