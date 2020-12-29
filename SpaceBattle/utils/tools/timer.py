from config import Configuration as Conf


class Timer:
    def __init__(self, time: float):
        self.time: float = Conf.System.GAME_SPEED / (1000 / time)
        self.ticks: int = 0

    def start(self) -> None:
        self.ticks = round(self.time / Conf.System.SCALE)

    def tick(self) -> bool:
        self.ticks -= 1
        return self.ticks <= 0
