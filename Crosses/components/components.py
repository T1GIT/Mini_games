import random
import tkinter as tk
from functools import partial

from config import Settings as Conf


class ComponentWin(tk.Frame):
    def __init__(self, window):
        super().__init__(master=window, highlightthickness=0, bg=Conf.BG_CLR)
        self.lbl_win = tk.Label(master=self, bg=Conf.BG_CLR, fg=Conf.TEXT_CLR,
                                image=self.master.pixel, compound=tk.CENTER,
                                width=Conf.CELL_SIZE, height=Conf.CELL_SIZE,
                                font=("Arial", Conf.SIGN_SIZE))
        self.btn_restart = tk.Button(master=self, text="Restart",
                                     relief=Conf.RELIEF, bg=Conf.MENU_BTN_CLR, fg=Conf.TEXT_CLR,
                                     activebackground=Conf.ACT_MENU_BTN_CLR, activeforeground=Conf.ACT_TEXT_CLR,
                                     height=Conf.BTN_HEIGHT, width=self.master.btn_width,
                                     command=lambda: self.master.reset(),
                                     image=self.master.pixel, compound=tk.CENTER,
                                     font=(Conf.FONT, Conf.SIGN_SIZE // 4))
        self.lbl_win.pack(pady=Conf.PADDING, padx=Conf.PADDING, fill=tk.X)
        self.btn_restart.pack(pady=Conf.PADDING, padx=Conf.PADDING)

    def reset(self):
        self.grid_forget()

    def show(self, win_char=None):
        if win_char is None:
            self.lbl_win["text"] = "DRAW"
        else:
            self.lbl_win["text"] = f"WIN {win_char}!"
        self.grid(row=0, sticky=tk.E + tk.W, pady=Conf.MARGIN, padx=Conf.MARGIN)


class ComponentGame(tk.Frame):
    def __init__(self, window):
        super().__init__(master=window, highlightthickness=0, bg=Conf.BG_CLR)
        self.grid(row=1, pady=Conf.MARGIN, padx=Conf.MARGIN)
        # Components
        self.field = [[None] * Conf.X_CELLS for _ in range(Conf.Y_CELLS)]
        for y, row in enumerate(self.field):
            for x in range(len(row)):
                btn = tk.Button(master=self, text=" ", state="disabled",
                                relief=Conf.RELIEF, bg=Conf.CELL_CLR,
                                activebackground=Conf.ACT_CELL_CLR,
                                image=self.master.pixel, compound=tk.CENTER,
                                width=Conf.CELL_SIZE, height=Conf.CELL_SIZE,
                                font=(Conf.FONT, Conf.SIGN_SIZE))
                btn.grid(row=y, column=x, padx=Conf.PADDING, pady=Conf.PADDING)
                btn["command"] = partial(self.step, x, y)
                row[x] = btn
        # Variables
        self.num_bot = 0
        self.is_bot = False
        self.move = 0

    def reset(self):
        self.move = 0
        for y, row in enumerate(self.field):
            for x, cell in enumerate(row):
                cell["text"] = " "
                cell["state"] = "disabled"

    def disable(self):
        for y, row in enumerate(self.field):
            for x, cell in enumerate(row):
                cell["state"] = "disabled"

    def get_rnd_coord(self):
        while True:
            x = random.randint(0, Conf.X_CELLS - 1)
            y = random.randint(0, Conf.Y_CELLS - 1)
            if self.field[y][x]["text"] == " ":
                return x, y

    def set_sign(self, x, y, sign_type):
        cell = self.field[y][x]
        cell["text"] = Conf.SIGNS[sign_type]
        cell["disabledforeground"] = Conf.SIGN_CLRS[sign_type]
        cell["state"] = "disabled"

    def is_draw(self):
        for row in self.field:
            for cell in row:
                if cell["text"] == " ":
                    return False
        return True

    def is_win(self):
        char = Conf.SIGNS[self.move]
        # Check horizontal
        for x0 in range(Conf.X_CELLS - Conf.REQ_LINE_LENGTH + 1):
            for y in range(0, Conf.Y_CELLS):
                points = 0
                for x in range(x0, x0 + Conf.REQ_LINE_LENGTH):
                    if self.field[y][x]["text"] == char:
                        points += 1
                if points == Conf.REQ_LINE_LENGTH:
                    return True
        # Check vertical
        for y0 in range(Conf.Y_CELLS - Conf.REQ_LINE_LENGTH + 1):
            for x in range(0, Conf.X_CELLS):
                points = 0
                for y in range(y0, y0 + Conf.REQ_LINE_LENGTH):
                    if self.field[y][x]["text"] == char:
                        points += 1
                if points == Conf.REQ_LINE_LENGTH:
                    return True
        # Check primary diagonal
        for y0 in range(Conf.Y_CELLS - Conf.REQ_LINE_LENGTH + 1):
            for x0 in range(Conf.X_CELLS - Conf.REQ_LINE_LENGTH + 1):
                points = 0
                for d in range(0, Conf.REQ_LINE_LENGTH):
                    if self.field[y0 + d][x0 + d]["text"] == char:
                        points += 1
                if points == Conf.REQ_LINE_LENGTH:
                    return True
        # Check secondary diagonal
        for y0 in range(Conf.Y_CELLS - Conf.REQ_LINE_LENGTH + 1):
            for x0 in range(Conf.X_CELLS - Conf.REQ_LINE_LENGTH + 1):
                points = 0
                for d in range(0, Conf.REQ_LINE_LENGTH):
                    if self.field[y0 + d][x0 - d + Conf.REQ_LINE_LENGTH - 1]["text"] == char:
                        points += 1
                if points == Conf.REQ_LINE_LENGTH:
                    return True
        return False

    def next(self):
        self.move = (self.move + 1) % len(Conf.SIGNS)

    def step(self, x, y):
        self.set_sign(x, y, self.move)
        if self.is_win():
            self.master.win(Conf.SIGNS[self.move])
        elif self.is_draw():
            self.master.draw()
        else:
            self.next()
            if self.is_bot and self.num_bot == self.move:
                self.step(*self.get_rnd_coord())

    def start(self, is_bot):
        self.is_bot = is_bot
        for y, row in enumerate(self.field):
            for x, cell in enumerate(row):
                cell["state"] = "normal"
        if self.is_bot:
            self.num_bot = random.randint(0, len(Conf.SIGNS) - 1)
            if self.num_bot == 0:
                self.step(*self.get_rnd_coord())


class ComponentMenu(tk.Frame):
    def __init__(self, window):
        super().__init__(master=window, highlightthickness=0, bg=Conf.BG_CLR)
        self.grid(row=2, pady=Conf.MARGIN, padx=Conf.MARGIN)
        self.lbl_start = tk.Label(master=self, text="Start with:",
                                  bg=Conf.BG_CLR, fg=Conf.TEXT_CLR,
                                  font=(Conf.FONT, Conf.BTN_TEXT_SIZE))
        self.btn_bot = tk.Button(master=self, text="BOT",
                                 relief=Conf.RELIEF, bg=Conf.MENU_BTN_CLR, fg=Conf.TEXT_CLR,
                                 activebackground=Conf.ACT_MENU_BTN_CLR, activeforeground=Conf.ACT_TEXT_CLR,
                                 height=Conf.BTN_HEIGHT, width=self.master.btn_width,
                                 command=lambda: self.master.start(True),
                                 image=self.master.pixel, compound=tk.CENTER,
                                 font=(Conf.FONT, Conf.BTN_TEXT_SIZE))
        self.btn_player = tk.Button(master=self, text="PLAYER",
                                    relief=Conf.RELIEF, bg=Conf.MENU_BTN_CLR, fg=Conf.TEXT_CLR,
                                    activebackground=Conf.ACT_MENU_BTN_CLR, activeforeground=Conf.ACT_TEXT_CLR,
                                    height=Conf.BTN_HEIGHT, width=self.master.btn_width,
                                    command=lambda: self.master.start(False),
                                    image=self.master.pixel, compound=tk.CENTER,
                                    font=(Conf.FONT, Conf.BTN_TEXT_SIZE))
        self.lbl_start.grid(row=0, columnspan=2, pady=Conf.PADDING, padx=Conf.PADDING)
        self.btn_bot.grid(row=1, column=0, pady=Conf.PADDING, padx=Conf.PADDING)
        self.btn_player.grid(row=1, column=1, pady=Conf.PADDING, padx=Conf.PADDING)

    def reset(self):
        self.grid(row=2, pady=Conf.MARGIN, padx=Conf.MARGIN)

    def hide(self):
        self.grid_forget()
