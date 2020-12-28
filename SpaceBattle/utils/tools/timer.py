class Timer:
    def __init__(self):
        self.ticks: int = 0

    def set(self, ticks: int):
        self.ticks = ticks

    def tick(self) -> bool:
        self.ticks -= 1
        return self.ticks <= 0
