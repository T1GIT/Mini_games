import pygame as pg


class Event:
    """
    Class of the event's object.
    Object contains:
        Event's type.
        Event's data.
    """
    def __init__(self, eventType: int, data):
        self._type: int = eventType
        self._data = data

    def get_type(self) -> int:
        """
        Returns event's type.
        Gets from Mouse.Events, Keyboard.Events, Gamepad.Events.
        Can be checked so: if (<Event.Object>.get_type() == Mouse.Events.KEY):
        :return: event's type
        """
        return self._type

    def get_data(self):
        """
        Returns event's data, specific for different event's type:
            Tuple - ( 0 <= x_axis <= 1, 0 <= y_axis <= 1) for:
                Mouse.Events.MOVE
                Gamepad.Events.LS
                Gamepad.Events.RS
            Int for:
                Mouse.Keys.<Name>
                Keyboard.Keys.<Name>
                Gamepad.Keys.<Name>
        :return: int or tuple - (0 <= x_axis <= 1, 0 <= y_axis <= 1)
        """
        return self._data


class System:
    class Events:
        QUIT = pg.QUIT


class Mouse:
    class Events:
        KEY = 100
        MOVE = 101

    class Keys:
        LEFT = 0


class Keyboard:
    class Events:
        KEY = 102

    class Keys:
        UP = pg.K_UP
        DOWN = pg.K_DOWN
        LEFT = pg.K_LEFT
        RIGHT = pg.K_RIGHT
        W = pg.K_w
        A = pg.K_a
        S = pg.K_s
        D = pg.K_d
        SPACE = pg.K_SPACE
        ENTER = pg.K_RETURN
        ESC = pg.K_ESCAPE


class Gamepad:
    class Events:
        LS = 103
        RS = 104
        KEY = 105

    class Keys:
        A = 0
        B = 1
        RT = 2
        BACK = 6
        START = 7


class Device:
    SYSTEM = 10000
    MOUSE = 10001
    KEYBOARD = 10002
    GAMEPAD = 10003
