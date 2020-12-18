import tkinter as tk
from threading import Thread

import pygame

from config import Configuration as Conf
from components.game import Game
from components.overlay import Overlay


class Window(tk.Tk):
    def __init__(self):
        # Initialisation
        super().__init__()
        # Configuring window
        width = Conf.WIN_WIDTH + Conf.FIELD_BRD_WIDTH
        height = Conf.WIN_HEIGHT + Conf.FIELD_BRD_WIDTH * 2
        if Conf.WITH_ICON: self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file=Conf.ICON_PATH))
        self.title(Conf.TITLE)
        self.geometry(f"{width}x{height}")
        self.resizable(width=Conf.RESIZABLE, height=Conf.RESIZABLE)
        self.attributes('-fullscreen', Conf.FULLSCREEN)
        self.overrideredirect(not Conf.BORDERS)
        # Components
        self.overlay = Overlay(self)
        self.game = Game(self)
        self.counter = self.overlay.counter
        self.next = self.overlay.next
        # Variables
        self.interval = self.counter.get_interval()
        self.lines = 0
        self.after_id = ""
        self.bind_id = ""
        self.thread = Thread()
        # Flags
        self.started = False
        self.paused = False
        self.is_over = False
        self.working = True
        # Listeners
        self.keyboard_listener()
        self.gamepad_listener()

    def exit(self):
        self.working = False

    def reset(self):
        self.overlay.reset()
        self.game.reset()
        self.paused = False
        self.interval = self.counter.get_interval()
        self.lines = 0
        self.is_over = False
        self.started = False
        self.after_cancel(self.after_id)

    def event_handler(self, event_name):
        fld = self.game.field
        if event_name == "exit":
            self.destroy()
        elif event_name == "start":
            if not self.started:
                self.start()
        elif self.started:
            if event_name == "pause":
                if self.paused:
                    self.process()
                else:
                    self.after_cancel(self.after_id)
                self.paused = not self.paused
            elif event_name == "reset":
                self.reset()
            if not self.paused:
                if event_name == 'left':
                    if fld.can_move(-1, 0):
                        fld.left()
                elif event_name == 'right':
                    if fld.can_move(1, 0):
                        fld.right()
                elif event_name == 'up':
                    if fld.can_rotate():
                        fld.rotate()
                elif event_name == 'down':
                    if fld.can_move():
                        fld.step()
                    else:
                        self.after_cancel(self.after_id)
                        self.process()

    def keyboard_listener(self, event=None):
        if event is None:
            self.bind('<KeyPress>', self.keyboard_listener)
        else:
            char = event.keysym.lower()
            if char in ['left', 'right', 'up', 'down']: self.event_handler(char)
            elif char in ['p', 'з']: self.event_handler('pause')
            elif char in ['r', 'к']: self.event_handler('reset')
            elif char in ['space', 'return']: self.event_handler('start')
            elif char == "escape": self.event_handler('exit')

    def gamepad_listener(self):
        pygame.init()
        clock = pygame.time.Clock()

        def connect():
            while pygame.joystick.get_count() == 0:
                if not self.working:
                    exit(69)
                pygame.quit()
                pygame.init()
            gamepad = pygame.joystick.Joystick(0)
            print("Gamepad connected:", gamepad.get_name())
            handler(gamepad)

        def disconnect(gamepad):
            print("Gamepad disconnected:", gamepad.get_name())
            if not self.paused: self.event_handler('pause')
            connect()

        def handler(gamepad):
            time = 0
            while True:
                if not self.working:
                    exit(69)
                if pygame.joystick.get_count() == 0: break
                hat = gamepad.get_hat(0)
                if hat != (0, 0):
                    if time == 0 or time > Conf.HOLD_LIMIT:
                        if hat[0] == -1: self.event_handler('left')
                        elif hat[0] == 1: self.event_handler('right')
                        if hat[1] == -1: self.event_handler('down')
                        elif hat[1] == 1: self.event_handler('up')
                    time += 1
                else: time = 0

                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                        btn = event.button
                        if btn == 1: self.event_handler('exit')
                        elif btn == 6: self.event_handler('pause')
                        elif btn == 7:
                            if self.started: self.event_handler('reset')
                            else: self.event_handler('start')

                clock.tick(Conf.REFRESH_RATE)
            disconnect(gamepad)

        self.thread = Thread(target=connect).start()

    def start(self):
        self.started = True
        self.overlay.button.pack_forget()
        self.next.generate()
        self.game.field.spawn(*self.next.get())
        self.process()

    def process(self):
        fld = self.game.field
        if not self.is_over:
            self.after_id = self.after(self.interval, self.process)
            if not self.paused:
                if fld.can_move():
                    fld.step()
                else:
                    fld.fall()
                    new_lines = fld.clear_full()
                    self.counter.raise_score(Conf.POINTS_FOR_LINES[new_lines])
                    self.lines += new_lines
                    if self.lines >= Conf.LEVEL_CONDITION:
                        self.lines -= Conf.LEVEL_CONDITION
                        self.counter.raise_level()
                        self.interval = self.counter.get_interval()
                    self.is_over = fld.is_lose()
                    if not self.is_over:
                        fld.spawn(*self.next.get())
                        self.next.generate()
        else:
            self.reset()
