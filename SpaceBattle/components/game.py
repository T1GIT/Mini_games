import sys

import pygame as pg

from components.interfaces.resetable import Resetable
from components.overlay import Overlay
from config import Configuration as Conf
from sprites.effects.animation import Animation
from sprites.effects.piece import Piece
from sprites.loot.bonuses import Heal
from sprites.mobs.meteor import Meteor
from sprites.player.ship import Ship
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
        self.game_over: bool = False
        self.clock: pg.time.Clock = pg.time.Clock()
        self.running: bool = False
        # Components
        self.comp_overlay: Overlay = Overlay(self)
        # Sprites
        self.ship: Ship = Ship()
        # Timers
        self.meteor_timer = Timer(Conf.Meteor.PERIOD)
        self.heal_timer = Timer(Conf.Bonus.Period.HEAL)
        self.losing_timer = Timer(Conf.Game.LOSE_DELAY)
        self.frames_timer = Timer(Conf.Overlay.Framerate.PERIOD)
        # Spawners
        self.meteor_spawner = Spawner(Meteor)
        self.piece_spawner = Spawner(Piece)
        self.heal_spawner = Spawner(Heal)
        # Background
        w0, h0 = Img.get_background().get_size()
        tar_size = max(w0, h0) * max((Conf.Window.WIDTH / w0, Conf.Window.HEIGHT / h0))
        self.background = Img.scale(Img.get_background(), tar_size)

    def reset(self):
        """
        Erases all mobs and objects
        """
        self.comp_overlay.reset()
        self.piece_spawner.get_group().kill_all()
        self.meteor_spawner.get_group().kill_all()
        self.heal_spawner.get_group().kill_all()
        self.comp_overlay.show()
        self.ship.kill()
        self.ship = Ship()
        self.ship.add(Groups.ALL)
        self.ship.locate(Conf.Window.WIDTH // 2, Conf.Window.HEIGHT // 2)
        Groups.ALL.add(self.ship)
        self.game_over = False
        self.running = True

    def lose(self):
        if not self.game_over:
            self.comp_overlay.health.down(self.comp_overlay.health.get_lifes())
            Snd.ex_ship()
            Animation.on_sprite("ship", self.ship, max(self.ship.rect.size) * Conf.Ship.ANIM_SCALE)
            self.ship.kill()
            self.losing_timer.start()
            Snd.game_over()
            self.game_over = True

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
                sys.exit()
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
            if event.get_data() == Kb.Keys.ESC:     self.window.toggle_menu()
            if event.get_data() == Kb.Keys.SPACE:   kb_self_distract[0] = True
            if event.get_data() == Kb.Keys.ENTER:   kb_self_distract[1] = True
        for event in events.get(Dvc.GAMEPAD, ()):
            if event.get_type() == Gp.Events.LS:    x, y = event.get_data()
            if event.get_type() == Gp.Events.RS:    self.ship.vector_rotate(*event.get_data(), False)
            if event.get_type() == Gp.Events.KEY:
                if event.get_data() == Gp.Keys.RT:      shoot = True
                if event.get_data() == Gp.Keys.START:   self.window.toggle_menu()
                if event.get_data() == Gp.Keys.LS:      gp_self_distract[0] = True
                if event.get_data() == Gp.Keys.RS:      gp_self_distract[1] = True
        if not self.game_over:
            # Checking self-destruction
            if kb_self_distract == [True, True] or gp_self_distract == [True, True]:
                self.lose()
            # Shooting
            if shoot and self.ship.can_shoot():
                Groups.ALL.add(*self.ship.shoot())
            # Moving
            self.ship.accelerate(x, -y)

    def mainloop(self):
        while self.running:
            self.event_processing()
            self.updating()
            # Checking losing
            if self.game_over:
                if self.losing_timer.is_ready():
                    self.running = False
            elif self.comp_overlay.health.is_dead():
                self.lose()
            # Actions
            self.colliding()
            self.spawning()
            self.refreshing_framerate()
            self.clock.tick(Conf.System.FPS)

    def event_processing(self):
        events = EventListener.get_events()
        self.event_handler(events)
        pg.event.get()

    def updating(self):
        Groups.ALL.update()
        self.window.screen.blit(self.background, self.background.get_rect())
        Groups.ALL.draw(self.window.screen)
        pg.display.flip()

    def colliding(self):
        hits = Collider.rockets_meteors(self.ship.get_group(), self.meteor_spawner.get_group())
        self.comp_overlay.score.up(hits)
        if not self.game_over:
            wounds = Collider.ship_to_group(self.ship, self.meteor_spawner.get_group(), Snd.ex_meteor, "meteor")
            self.comp_overlay.health.down(wounds)
            heals = Collider.ship_to_group(self.ship, self.heal_spawner.get_group(), Snd.heal, "heal", Conf.Bonus.ANIM_SIZE)
            self.comp_overlay.health.up(heals)

    def spawning(self):
        if Conf.Meteor.BY_TIME:
            if self.meteor_timer.is_ready():
                Groups.ALL.add(*self.meteor_spawner.spawn())
                self.meteor_timer.start()
        else:
            Groups.ALL.add(*self.meteor_spawner.spawn(Conf.Meteor.QUANTITY - len(self.meteor_spawner.get_group())))
            self.meteor_timer.start()
        Groups.ALL.add(*self.piece_spawner.spawn(Conf.Piece.QUANTITY - len(self.piece_spawner.get_group())))
        if self.heal_timer.is_ready():
            Groups.ALL.add(*self.heal_spawner.spawn())
            self.heal_timer.start()

    def refreshing_framerate(self):
        self.comp_overlay.framerate.add_frame()
        if Conf.Overlay.Framerate.VISIBLE and self.frames_timer.is_ready():
            self.frames_timer.start()
            self.comp_overlay.framerate.refresh()
