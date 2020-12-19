import pygame as pg

from components.overlay import Overlay
from config import Configuration as Conf
from sprites.animation import Animation
from sprites.ship import Ship
from utils.mechanics.collider import Collider
from utils.listener.events import Keyboard as Kb, Gamepad as Gp, Mouse as Ms, Device as Dvc, System as Sys, Event
from utils.tools.group import Group
from utils.resources.image import Image as Img
from utils.listener.listener import EventListener
from utils.resources.sound import Sound as Snd
from utils.mechanics.spawner import Spawner


class Game:
    """
    Class which initials the game.
    Spawns meteors.
    Catches events and redirect to the ship
    """

    def __init__(self, window):
        # Environment
        self.window = window
        self.running = False
        self.game_over = False
        self.clock = pg.time.Clock()
        # Components
        self.comp_overlay = Overlay(self)
        # Sprites
        self.ship = None
        # Timers
        self.meteor_timer = 0
        self.rocket_timer = 0
        self.losing_timer = 0
        # Background
        bg = Img.get_background()
        w0, h0 = bg.get_size()
        scale = max((Conf.Window.WIDTH / w0, Conf.Window.HEIGHT / h0))
        w1, h1 = map(lambda x: round(x * scale), [w0, h0])
        self.image = pg.transform.scale(bg, (w1, h1))

    def reset(self):
        """
        Erases all mobs and objects
        """
        self.__init__(self.window)

    def start(self):
        """
        Starts the game
        """
        self.game_over = False
        self.running = True
        self.comp_overlay.show()
        self.ship = Ship()
        self.ship.locate(Conf.Window.WIDTH // 2, Conf.Window.HEIGHT // 2)
        Group.ALL.add(self.ship)
        if not Conf.Meteor.BY_TIME:
            Spawner.all_meteors()
        Spawner.all_pieces(True)
        self.mainloop()

    def lose(self):
        if not self.game_over:
            self.ship.kill()
            Snd.ex_ship()
            Animation.on_sprite("ship", self.ship, max(self.ship.rect.size) * Conf.Ship.ANIM_SCALE)
            self.losing_timer = Conf.System.FPS * Conf.Game.LOSE_DELAY
            self.game_over = True
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
                self.running = False
        for event in events.get(Dvc.MOUSE, ()):
            if event.get_type() == Ms.Events.MOVE:
                self.ship.rotate(*event.get_data(), True)
            if event.get_type() == Ms.Events.KEY and event.get_data() == Ms.Keys.LEFT:
                shoot = True
        for event in events.get(Dvc.KEYBOARD, ()):
            if event.get_data() in (Kb.Keys.W, Kb.Keys.UP):       y += 1
            if event.get_data() in (Kb.Keys.A, Kb.Keys.LEFT):     x -= 1
            if event.get_data() in (Kb.Keys.S, Kb.Keys.DOWN):     y -= 1
            if event.get_data() in (Kb.Keys.D, Kb.Keys.RIGHT):    x += 1
            if event.get_data() == Kb.Keys.ESC: self.window.pause()
            if event.get_data() == Kb.Keys.SPACE: kb_self_distract[0] = True
            if event.get_data() == Kb.Keys.ENTER: kb_self_distract[1] = True
        for event in events.get(Dvc.GAMEPAD, ()):
            if event.get_type() == Gp.Events.LS:    x, y = event.get_data()
            if event.get_type() == Gp.Events.RS:    self.ship.rotate(*event.get_data(), False)
            if event.get_type() == Gp.Events.KEY and event.get_data() == Gp.Keys.RT: shoot = True
            if event.get_type() == Gp.Events.KEY and event.get_data() == Gp.Keys.START: self.window.pause()
            if event.get_type() == Gp.Events.KEY and event.get_data() == Gp.Keys.LS: gp_self_distract[0] = True
            if event.get_type() == Gp.Events.KEY and event.get_data() == Gp.Keys.RS: gp_self_distract[1] = True
        if not self.game_over:
            # Checking self-destruction
            if kb_self_distract == [True, True] or gp_self_distract == [True, True]:
                self.lose()
            # Shooting
            if shoot and not self.game_over and self.rocket_timer == 0:
                self.rocket_timer = (Conf.System.FPS * Conf.Rocket.PERIOD) // 1000
                self.ship.shoot()
            # Moving
            if (x, y) == (0, 0):    self.ship.brake()
            else:                   self.ship.accelerate(x, y)

    def mainloop(self):
        while self.running:
            self.window.screen.blit(self.image, self.image.get_rect())
            events = EventListener.get_events()
            if self.game_over: events = {Dvc.SYSTEM: events[Dvc.SYSTEM]}
            self.event_handler(events)
            Group.ALL.update()
            Group.ALL.draw(self.window.screen)
            pg.display.update(Group.ALL.sprites())
            if self.game_over:
                if self.losing_timer == 0:
                    self.window.reset()
                    self.window.open_menu()
                else:
                    self.losing_timer -= 1
            else:
                self.preparation()
            self.clock.tick(Conf.System.FPS)

    def preparation(self):
        """
        Do all actions per one frame
        """
        # Colliding
        points = Collider.rockets_meteors()
        wounds = Collider.ship_meteors(self.ship)
        self.comp_overlay.score.up(points)
        if wounds: self.comp_overlay.health.down()
        if self.comp_overlay.health.is_dead():
            self.lose()
        # Spawning
        if Conf.Meteor.BY_TIME:
            if self.meteor_timer == 0:
                self.meteor_timer = (Conf.System.FPS * Conf.Meteor.PERIOD) // 1000
                Spawner.meteor()
        else: Spawner.all_meteors()
        Spawner.all_pieces(False)
        # Decrementing timers
        self.meteor_timer = max(0, self.meteor_timer - 1)
        self.rocket_timer = max(0, self.rocket_timer - 1)

