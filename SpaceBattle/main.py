from components.window import Window


class SpaceBattle:
    def __init__(self):
        self.window = Window()

    def start(self):
        self.window.show()


if __name__ == "__main__":
    game = SpaceBattle()
    game.start()
