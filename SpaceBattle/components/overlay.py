import pygame as pg
from collections import deque
from time import time_ns

from components.abstractComponent import AbstractComponent
from config import Configuration as Conf
from utils.tools.group import Group
from utils.resources.image import Image as Img


class Overlay(AbstractComponent):
    def __init__(self, game):
        self.game = game
        # Components
        self.score = self.Score()
        self.health = self.Health()
        self.framerate = self.Framerate()
        Group.ALL.add(self.score)
        Group.ALL.add(self.health)
        Group.ALL.add(self.framerate)

    def reset(self):
        """
        Zero out all variables
        """
        self.score.reset()
        self.health.reset()
        self.Framerate.reset()
        self.__init__(self.game)

    def show(self):
        self.score.show()
        self.health.show()
        if Conf.Overlay.Framerate.VISIBLE:
            self.framerate.show()

    class Score(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.font = pg.font.Font("resources/fonts/opensans.ttf", Conf.Overlay.Score.SIZE)
            self.need_update = False
            self.score = 0
            self.image = self.font.render(str(self.score), True, Conf.Overlay.Score.COLOR)
            self.image.set_alpha(Conf.Overlay.OPACITY)

        def reset(self) -> None:
            self.__init__()

        def get_score(self) -> int:
            return self.score

        def show(self) -> None:
            self.rect = self.image.get_rect(topright=(
                Conf.Window.WIDTH - Conf.Overlay.Score.X_OFFSET, Conf.Overlay.Score.Y_OFFSET))

        def update(self) -> None:
            if self.need_update:
                self.image = self.font.render(str(self.score), True, Conf.Overlay.Score.COLOR)
                self.image.set_alpha(Conf.Overlay.OPACITY)
                self.show()
                self.need_update = False

        def up(self, points: int) -> None:
            self.need_update = True
            self.score += Conf.Overlay.Score.DELTA * points

    class Health(pg.sprite.Sprite, AbstractComponent):
        def __init__(self):
            super().__init__()
            self.points: deque[pg.sprite.Sprite] = deque()
            self.image = pg.surface.Surface((0, 0))
            self.rect = pg.rect.Rect(0, 0, 0, 0)
            raw_image = Img.get_life()
            self.texture = pg.transform.scale(raw_image, [Conf.Overlay.Health.SIZE] * 2)
            for i in range(Conf.Rules.LIFES):
                point = pg.sprite.Sprite()
                point.image = self.texture
                point.image.set_alpha(Conf.Overlay.OPACITY)
                self.points.append(point)
                Group.ALL.add(point)

        def get_lifes(self) -> int:
            return len(self.points)

        def show(self) -> None:
            cnf = Conf.Overlay.Health
            for i, point in enumerate(self.points):
                point.rect = point.image.get_rect(
                    topleft=(cnf.X_OFFSET + (i * cnf.SIZE) + (i * cnf.MARGIN), cnf.Y_OFFSET))

        def down(self) -> None:
            self.points.pop().kill()

        def is_dead(self) -> bool:
            return len(self.points) == 0

    @staticmethod
    def fps_toggle(value):
        Conf.Overlay.Framerate.VISIBLE = value

    class Framerate(pg.sprite.Sprite, AbstractComponent):
        def __init__(self):
            super().__init__()
            self.font = pg.font.Font("resources/fonts/opensans.ttf", Conf.Overlay.Framerate.SIZE)
            self.needs_update: bool = False
            self.visible: bool = Conf.Overlay.Framerate.VISIBLE
            self.amount_frames: int = 0
            self.value: int = 0
            self.last_time: int = 0
            self.image = self.font.render("", True, Conf.Overlay.Framerate.COLOR)
            self.image.set_alpha(Conf.Overlay.OPACITY)

        def get(self) -> int:
            return self.value

        def show(self) -> None:
            self.rect = self.image.get_rect(bottomright=(Conf.Window.WIDTH - Conf.Overlay.Framerate.X_OFFSET,
                                                         Conf.Window.HEIGHT - Conf.Overlay.Framerate.Y_OFFSET))

        def update(self) -> None:
            if self.visible:
                if not Conf.Overlay.Framerate.VISIBLE:
                    self.image.set_alpha(0)
                elif self.needs_update:
                    self.image = self.font.render(str(self.value), True, Conf.Overlay.Framerate.COLOR)
                    self.image.set_alpha(Conf.Overlay.OPACITY)
                    self.show()
                    self.needs_update = False
            elif Conf.Overlay.Framerate.VISIBLE:
                self.visible = True

        def add_frame(self):
            self.amount_frames += 1

        def refresh(self):
            self.value = round(self.amount_frames * (1000 / ((time_ns() - self.last_time) / 1e6)))
            self.last_time = time_ns()
            self.amount_frames = 0
            self.needs_update = True
