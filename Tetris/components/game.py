import time
import tkinter as tk

from config import Configuration as Conf


class Game(tk.Frame):
    def __init__(self, window):
        super().__init__(master=window,
                         width=Conf.WIN_WIDTH - Conf.OVERLAY_WIDTH + Conf.FIELD_BRD_WIDTH,
                         height=Conf.WIN_HEIGHT + Conf.FIELD_BRD_WIDTH * 2,
                         bg=Conf.BG_CLR,
                         highlightthickness=0)
        self.pack_propagate(False)
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.field = Field(self)

    def reset(self):
        self.field.reset()


class Field(tk.Canvas):
    def __init__(self, game):
        super().__init__(master=game,
                         width=Conf.WIN_WIDTH - Conf.OVERLAY_WIDTH,
                         height=Conf.WIN_HEIGHT,
                         bg=Conf.FG_CLR,
                         highlightthickness=0)
        self.pack(side=tk.RIGHT)
        self.fallen = [[None] * Conf.X_BLOCKS for _ in range(Conf.Y_BLOCKS)]
        self.moving = [[]]
        self.tag = ""

    def reset(self):
        self.delete("all")
        self.fallen = [[None] * Conf.X_BLOCKS for _ in range(Conf.Y_BLOCKS)]
        self.moving = [[]]
        self.tag = ""

    def spawn(self, template: list, dtl_type: int):
        """
        Draws and remembers new moving element.
        :param template: bin array storing figure's shape
        :param dtl_type: number of color
        """
        _rev_tmpl = list(reversed(template))
        width = len(template[0])
        height = len(template)
        x_offset = (Conf.X_BLOCKS - width) // 2
        y_offset = -len(template) + _rev_tmpl.index(next((row for row in _rev_tmpl if row != [0] * len(row))))
        self.moving = [[None] * width for _ in range(height)]
        self.tag = f"F{time.time()}"
        for row_ind, row in enumerate(template):
            for col_ind, col in enumerate(row):
                if col:
                    self.moving[row_ind][col_ind] = self.draw_block(
                        x=col_ind + x_offset,
                        y=row_ind + y_offset,
                        dtl_type=dtl_type
                    )

    def clear_full(self):
        """
        Erase full lines from the canvas and removes its objects from the memory.
        :return amount of full lines
        """
        counter = 0
        for row in reversed(self.fallen):
            if None in row:
                if counter > 0:
                    for block in row:
                        if block is not None:
                            self.move(block, 0, Conf.DTL_SIZE * counter)
            else:
                for block in row:
                    if block is not None:
                        self.delete(block)
                self.fallen.remove(row)
                counter += 1
        for _ in range(counter):
            self.fallen.insert(0, [None] * Conf.X_BLOCKS)
        return counter

    def is_lose(self) -> bool:
        """
        Checks if game is finished.
        :return: True if the top stroke has part of a detail, else - False.
        """
        top_line = self.fallen[0]
        return not (top_line == [None] * len(top_line))

    def left(self):
        self.move(self.tag, -Conf.DTL_SIZE, 0)

    def right(self):
        self.move(self.tag, Conf.DTL_SIZE, 0)

    def rotate(self):
        for row_i, row in enumerate(self.moving):
            for col_i, col in enumerate(row):
                if col is not None:
                    delta_x = len(self.moving) - row_i - col_i - 1
                    delta_y = col_i - row_i
                    self.move(col, delta_x * Conf.DTL_SIZE, delta_y * Conf.DTL_SIZE)
        self.moving = [list(t) for t in zip(*reversed(self.moving))]

    def can_rotate(self):
        for row_i, row in enumerate(self.moving):
            for col_i, col in enumerate(row):
                if col is not None:
                    x, y = self.block_coords(col)
                    tar_x = x + len(self.moving) - row_i - col_i - 1
                    tar_y = y + col_i - row_i
                    if not 0 <= tar_x < Conf.X_BLOCKS:
                        return False
                    elif tar_y < 0:
                        continue
                    elif tar_y >= Conf.Y_BLOCKS:
                        return False
                    elif self.fallen[tar_y][tar_x] is not None:
                        return False
        return True

    def fall(self):
        """
        Clears moving element and places its blocks into the fallen
        """
        for row in self.moving:
            for col in row:
                if col is not None:
                    x, y = self.block_coords(col)
                    self.fallen[y][x] = col

    def step(self):
        """
        Moves falling element down on one step
        """
        self.move(self.tag,
                  0, Conf.DTL_SIZE
                  )

    def can_move(self, x_offset=0, y_offset=1):
        for row in self.moving:
            for col in row:
                if col is not None:
                    x, y = self.block_coords(col)
                    check_x, check_y = x + x_offset, y + y_offset
                    if not (0 <= check_x < Conf.X_BLOCKS):
                        return False
                    elif check_y < 0:
                        continue
                    elif check_y >= Conf.Y_BLOCKS:
                        return False
                    elif self.fallen[check_y][check_x] is not None:
                        return False
        return True

    def draw_block(self, x: int, y: int, dtl_type: int):
        raw_x0 = x * Conf.DTL_SIZE + Conf.DTL_OFFSET
        raw_y0 = y * Conf.DTL_SIZE + Conf.DTL_OFFSET
        raw_x1 = raw_x0 + Conf.DTL_SIZE - Conf.DTL_BORDER_WIDTH
        raw_y1 = raw_y0 + Conf.DTL_SIZE - Conf.DTL_BORDER_WIDTH
        return self.create_rectangle(raw_x0, raw_y0, raw_x1, raw_y1,
                                     fill=Conf.DTL_CLR[dtl_type],
                                     outline=Conf.DTL_BRD_CLR[dtl_type],
                                     width=Conf.DTL_BORDER_WIDTH,
                                     tag=self.tag)

    def block_coords(self, tk_id):
        return list(map(lambda v: int(v // Conf.DTL_SIZE), self.coords(tk_id)[0:2]))
