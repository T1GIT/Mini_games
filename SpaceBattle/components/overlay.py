from time import time_ns

import pygame as pg

from components.interfaces.resetable import Resetable
from config import Configuration as Conf
from sprites.interfaces.basic import Transparent, Text, Locatable, Group
from utils.resources.image import Image as Img
from utils.tools.groups import Groups


class Overlay(Resetable):
    def __init__(self, game):
        super().__init__()
        self.game = game
        # Components
        self.score: Overlay.Score = Overlay.Score()
        self.health: Overlay.Health = Overlay.Health()
        self.framerate: Overlay.Framerate = Overlay.Framerate()
        Groups.ALL.add(self.score)
        Groups.ALL.add(self.health)
        Groups.ALL.add(self.framerate)
        Groups.OVERLAY.add(self.score, self.health, self.framerate)

    def reset(self):
        """
        Zero out all variables
        """
        self.score.reset()
        self.health.reset()
        self.framerate.reset()

    def show(self):
        self.score.show()
        self.health.show()
        if Conf.Overlay.Framerate.VISIBLE:
            self.framerate.show()

    class Score(Text, Transparent):
        def __init__(self):
            Text.__init__(
                self,
                font=pg.font.Font("resources/fonts/opensans.ttf", Conf.Overlay.Score.SIZE),
                color=Conf.Overlay.Score.COLOR,
                value="0"
            )
            Transparent.__init__(
                self,
                texture=self.texture,
                opacity=Conf.Overlay.OPACITY
            )

        def reset(self) -> None:
            super().set_value(0)

        def get_score(self) -> int:
            return int(super().get_value())

        def show(self) -> None:
            super().locate(topright=(
                Conf.Window.WIDTH - Conf.Overlay.Score.X_OFFSET, Conf.Overlay.Score.Y_OFFSET))

        def up(self, points: int) -> None:
            super().set_value(int(super().get_value()) + Conf.Overlay.Score.DELTA * points)

    class Health(Locatable, Resetable):
        def __init__(self):
            super().__init__(pg.Surface((0, 0)))
            self.texture = pg.transform.scale(Img.get_life(), [Conf.Overlay.Health.SIZE] * 2)
            self.points_group = Group()
            for i in range(Conf.Rules.LIFES):
                point = Overlay.Health.Life(self.texture)
                self.points_group.add(point)
                point.add(Groups.LIFES, Groups.ALL)

        def reset(self):
            self.points_group.kill()
            for i in range(Conf.Rules.LIFES):
                point = Overlay.Health.Life(self.texture)
                self.points_group.add(point)
                point.add(Groups.LIFES, Groups.ALL)

        def update(self, *args, **kwargs) -> None:
            self.points_group.update()

        def get_lifes(self) -> int:
            return len(self.points_group)

        def show(self) -> None:
            cnf = Conf.Overlay.Health
            super().locate()
            for pos, point in enumerate(self.points_group):
                point.locate(topleft=(cnf.X_OFFSET + (pos * cnf.SIZE) + (pos * cnf.MARGIN), cnf.Y_OFFSET))

        def down(self, amount: int) -> None:
            for _ in range(amount):
                self.points_group.sprites()[-1].kill()

        def up(self, amount: int) -> None:
            cnf = Conf.Overlay.Health
            for _ in range(amount):
                point = Overlay.Health.Life(self.texture)
                self.points_group.add(point)
                point.add(Groups.LIFES, Groups.ALL)
                pos = len(self.points_group) - 1
                point.locate(topleft=(cnf.X_OFFSET + (pos * cnf.SIZE) + (pos * cnf.MARGIN), cnf.Y_OFFSET))

        def is_dead(self) -> bool:
            return len(self.points_group) == 0

        class Life(Transparent):
            def __init__(self, texture: pg.Surface):
                super().__init__(
                    texture=texture,
                    opacity=Conf.Overlay.OPACITY
                )

    class Framerate(Text, Transparent, Resetable):
        def __init__(self):
            Text.__init__(
                self,
                font=pg.font.Font("resources/fonts/opensans.ttf", Conf.Overlay.Framerate.SIZE),
                color=Conf.Overlay.Framerate.COLOR,
                value=""
            )
            Transparent.__init__(
                self,
                texture=self.texture,
                opacity=Conf.Overlay.OPACITY
            )
            self.amount_frames: int = 0
            self.last_time: int = 0

        def reset(self):
            super().set_value("")
            self.amount_frames = 0
            self.last_time = 0

        def get(self) -> int:
            return int(super().get_value())

        def show(self) -> None:
            super().locate(bottomright=(Conf.Window.WIDTH - Conf.Overlay.Framerate.X_OFFSET,
                                        Conf.Window.HEIGHT - Conf.Overlay.Framerate.Y_OFFSET))

        def update(self) -> None:
            if Conf.Overlay.Framerate.VISIBLE:
                if super().get_opacity() != Conf.Overlay.OPACITY:
                    super().set_opacity(Conf.Overlay.OPACITY)
            else:
                if super().get_opacity() != 0:
                    super().set_opacity(0)

        def add_frame(self):
            self.amount_frames += 1

        def refresh(self):
            super().set_value(min(
                round(self.amount_frames * (1000 / ((time_ns() - self.last_time) / 1e6))),
                Conf.System.FPS))
            self.last_time = time_ns()
            self.amount_frames = 0

        @staticmethod
        def toggle(value):
            Conf.Overlay.Framerate.VISIBLE = value
