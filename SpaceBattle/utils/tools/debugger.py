import sys
import traceback
from time import time_ns


def format_exception(e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]

    return exception_str


class Debugger:
    t, s, a = 0, 0, 0

    @staticmethod
    def start():
        Debugger.t = time_ns()

    @staticmethod
    def print(comment: str):
        print(f"{comment:20}" + ":", round((time_ns() - Debugger.t) / 1e6, 4), "ms")
        Debugger.t = time_ns()
