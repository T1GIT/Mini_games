from components.window import Window


class CrosserAndZeros:
    def __init__(self):
        self.root = Window()

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = CrosserAndZeros()
    game.start()
