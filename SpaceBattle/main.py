from components.window import Window
from utils.tools.debugger import format_exception
import datetime

if __name__ == "__main__":
    try:
        window = Window()
        window.show()
    except Exception as e:
        with open("log.txt", "a") as file:
            file.write(str(datetime.datetime.now()) + " | ERROR | " + format_exception(e) + "\n")
