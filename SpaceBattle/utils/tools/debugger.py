from time import time_ns


class Debugger:
    t, s, a = 0, 0, 0

    @staticmethod
    def start():
        Debugger.t = time_ns()

    @staticmethod
    def print(comment: str):
        print(f"{comment:20}" + ":", round((time_ns() - Debugger.t) / 1e6, 4), "ms")
        Debugger.t = time_ns()
