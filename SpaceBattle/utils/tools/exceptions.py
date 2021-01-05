class GameException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NewGameException(GameException):
    def __init__(self, *args):
        super().__init__(*args)


class GameOverException(GameException):
    def __init__(self, *args):
        super().__init__(*args)
