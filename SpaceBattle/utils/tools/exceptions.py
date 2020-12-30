class NewGameException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class GameOverException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
