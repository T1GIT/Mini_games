import random as rnd
import tkinter as tk

from config import Configuration as Conf


class Overlay(tk.Frame):
    def __init__(self, window):
        super().__init__(master=window,
                         width=Conf.OVERLAY_WIDTH,
                         height=Conf.WIN_HEIGHT,
                         bg=Conf.BG_CLR,
                         highlightthickness=0)
        self.pack_propagate(False)
        self.pack(side=tk.RIGHT, fill=tk.Y)
        self.next = Next(self)
        self.counter = Counter(self)
        self.button = Button(self)

    def reset(self):
        self.next.reset()
        self.counter.reset()
        self.button.reset()


class Next(tk.Frame):
    def __init__(self, overlay):
        super().__init__(master=overlay,
                         width=Conf.WIN_HEIGHT // 4,
                         bg=Conf.BG_CLR,
                         highlightthickness=0)
        self.pack(fill=tk.BOTH)
        self.next = tk.Label(self,
                             text="NEXT", fg=Conf.TXT_CLR, bg=Conf.BG_CLR,
                             font=("Ariel", Conf.WIN_HEIGHT // 30))
        self.next.pack(pady=Conf.WIN_HEIGHT // 30)
        self.cvs = tk.Canvas(self,
                             width=Conf.WIN_HEIGHT // 6,
                             height=Conf.WIN_HEIGHT // 6,
                             bg=Conf.BG_CLR,
                             highlightbackground=Conf.FG_CLR,
                             highlightthickness=Conf.NEXT_BRD_WIDTH)
        self.cvs.pack()
        self.template = [[]]
        self.dtl_type = -1

    def reset(self):
        self.cvs.delete("all")
        self.template = [[]]
        self.dtl_type = -1

    def generate(self):
        """
        Draws next dropping components in the overlay
        """
        self.cvs.delete("all")
        self.dtl_type = rnd.randint(0, len(Conf.DTL_TYPES) - 1)
        self.template = Conf.DTL_TYPES[self.dtl_type]
        for _ in range(rnd.randint(0, 3)):
            self.template = [list(t) for t in zip(*reversed(self.template))]
        size = self.cvs.winfo_width()
        block_size = size // (max(len(self.template), len(self.template[0])) + Conf.NEXT_PAD * 2)
        border_width = Conf.DTL_BORDER_WIDTH * block_size // Conf.DTL_SIZE
        border_offset = border_width / 2
        draw = list(map(lambda x: list(x), filter(lambda r: r != [0] * len(r), self.template)))
        draw = list(map(lambda x: list(x), zip(*filter(lambda r: list(r) != [0] * len(r), zip(*draw)))))
        x_offset = round((size - len(draw[0]) * block_size) / 2)
        y_offset = round((size - len(draw) * block_size) / 2)
        for row_ind, row in enumerate(draw):
            for col_ind, col in enumerate(row):
                if col:
                    raw_x0 = x_offset + col_ind * block_size + border_offset
                    raw_y0 = y_offset + row_ind * block_size + border_offset
                    raw_x1 = raw_x0 + block_size - border_width
                    raw_y1 = raw_y0 + block_size - border_width
                    self.cvs.create_rectangle(raw_x0, raw_y0, raw_x1, raw_y1,
                                              fill=Conf.DTL_CLR[self.dtl_type],
                                              outline=Conf.DTL_BRD_CLR[self.dtl_type],
                                              width=border_width)

    def get(self):
        return self.template, self.dtl_type


class Counter(tk.Frame):
    def __init__(self, overlay):
        super().__init__(master=overlay,
                         width=Conf.WIN_HEIGHT // 4,
                         bg=Conf.BG_CLR)
        self.pack(fill=tk.BOTH, pady=Conf.WIN_HEIGHT // 20)

        def counter_lbl(text):
            lbl = tk.Label(self,
                           text=text, fg=Conf.TXT_CLR, bg=Conf.BG_CLR,
                           font=("Ariel", Conf.WIN_HEIGHT // 35))
            lbl.pack(pady=Conf.VERTICAL_MARGIN)
            return lbl

        self.score = counter_lbl("SCORE")
        self.score_msr = counter_lbl("0")
        self.level = counter_lbl("LEVEL")
        self.level_msr = counter_lbl(str(Conf.START_LEVEL))
        self.max = counter_lbl("MAX")
        self.max_msr = counter_lbl("0")

    def reset(self):
        if int(self.score_msr["text"]) > int(self.max_msr["text"]):
            self.max_msr["text"] = str(self.score_msr["text"])
        self.score_msr["text"] = "0"
        self.level_msr["text"] = str(Conf.START_LEVEL)

    def raise_score(self, delta):
        self.score_msr["text"] = str(int(self.score_msr["text"]) + delta)

    def raise_level(self):
        self.level_msr["text"] = str(int(self.level_msr["text"]) + 1)

    def get_interval(self) -> int:
        level = int(self.level_msr["text"])
        return int((0.8 - ((level - 1) * 0.007)) ** (level - 1) * 1000)


class Button(tk.Button):
    def __init__(self, overlay):
        super().__init__(master=overlay,
                         text="START", font=("Ariel", Conf.WIN_HEIGHT // 30),
                         width=8,
                         height=1,
                         fg=Conf.BG_CLR, bg=Conf.FG_CLR,
                         relief=tk.FLAT,
                         command=self.click)
        self.pack(side=tk.BOTTOM, pady=Conf.WIN_HEIGHT // 20)

    def reset(self):
        self.pack(side=tk.BOTTOM, pady=Conf.WIN_HEIGHT // 20)

    def click(self):
        self.master.master.set()
