from time import time_ns


class Timer:
    def __init__(self, time: float):
        self.time: float = time * 1e6
        self.start_time: float = time_ns()

    def set_time(self, time: float):
        self.time: float = time * 1e6

    def start(self) -> None:
        self.start_time = time_ns()

    def is_ready(self) -> bool:
        return time_ns() - self.start_time > self.time
