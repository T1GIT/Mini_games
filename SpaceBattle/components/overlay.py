import pygame as pg
from collections import deque

from config import Configuration as Conf
from utils.tools.group import Group
from utils.resources.image import Image as Img


class Overlay:
    def __init__(self, game):
        self.game = game
        # Components
        self.score = self.Score()
        self.health = self.Health()
        Group.ALL.add(self.score)
        Group.ALL.add(self.health)

    def reset(self):
        """
        Zero out all variables
        """
        self.score.reset()
        self.health.reset()
        self.__init__(self.game)

    def show(self):
        self.score.show()
        self.health.show()

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
                Conf.Window.WIDTH - Conf.Overlay.Score.X_OFFSET, Conf.Overlay.Score.Y_OFFSET - 20))

        def update(self) -> None:
            if self.need_update:
                self.image = self.font.render(str(self.score), True, Conf.Overlay.Score.COLOR)
                self.image.set_alpha(Conf.Overlay.OPACITY)
                self.show()
                self.need_update = False

        def up(self, points: int) -> None:
            self.need_update = True
            self.score += Conf.Overlay.Score.DELTA * points

    class Framerate(pg.sprite.Sprite):
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
                Conf.Window.WIDTH - Conf.Overlay.Score.X_OFFSET, Conf.Overlay.Score.Y_OFFSET - 20))

        def update(self) -> None:
            if self.need_update:
                self.image = self.font.render(str(self.score), True, Conf.Overlay.Score.COLOR)
                self.image.set_alpha(Conf.Overlay.OPACITY)
                self.show()
                self.need_update = False

        def up(self, points: int) -> None:
            self.need_update = True
            self.score += Conf.Overlay.Score.DELTA * points

    class Health(pg.sprite.Sprite):
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

        def reset(self) -> None:
            self.__init__()

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
