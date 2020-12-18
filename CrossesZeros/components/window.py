import tkinter as tk

from config import Settings as Conf
from components.components import ComponentGame, ComponentMenu, ComponentWin


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        # Configuring window
        self.title(Conf.TITLE)
        self.resizable(width=False, height=False)
        self["bg"] = Conf.BG_CLR
        # Variables
        self.btn_width = (Conf.CELL_SIZE + Conf.PADDING * 2) * Conf.X_CELLS // 2 - (Conf.PADDING * 2) + 4 * (
                    Conf.X_CELLS - 2)
        self.pixel = tk.PhotoImage(width=1, height=1)
        # Flags
        self.started = False
        # Components
        self.comp_win = ComponentWin(self)
        self.comp_game = ComponentGame(self)
        self.comp_menu = ComponentMenu(self)
        # Listeners
        self.keyboard_listener()

    def reset(self):
        self.started = False
        self.comp_win.reset()
        self.comp_game.reset()
        self.comp_menu.reset()

    def event_handler(self, event_name):
        if event_name == "exit":
            self.destroy()
        elif event_name == "start":
            if not self.started:
                self.start(True)
        elif event_name == "reset":
            if self.started:
                self.reset()

    def keyboard_listener(self, event=None):
        if event is None:
            self.bind('<KeyPress>', self.keyboard_listener)
        else:
            char = event.keysym.lower()
            if char in ['r', 'к']: self.event_handler('reset')
            elif char in ['space', 'return']: self.event_handler('start')
            elif char == "escape": self.event_handler('exit')

    def win(self, win_char):
        self.comp_win.show(win_char)
        self.comp_game.disable()

    def draw(self):
        self.comp_win.show()
        self.comp_game.disable()

    def start(self, is_bot):
        self.started = True
        self.comp_menu.hide()
        self.comp_game.start(is_bot)
