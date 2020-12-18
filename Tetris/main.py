from components.window import Window


class Tetris:
    def __init__(self):
        self.root = Window()

    def start(self):
        self.root.mainloop()
        self.root.exit()


if __name__ == "__main__":
    tetris = Tetris()
    tetris.start()
