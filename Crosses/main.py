from components.window import Window


class Crosses:
    def __init__(self):
        self.root = Window()

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = Crosses()
    game.start()
