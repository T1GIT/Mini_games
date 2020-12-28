from math import pow, hypot

import pygame as pg

from config import Configuration as Conf
from utils.listener.events import Event, Mouse as Ms, Keyboard as Kb, Gamepad as Gp, System as Sys, Device as Dvc


class EventListener:
    """
    Collects events in the separated thread.
    Events can be gotten by pop_events(), and
    they will be erasing in the same time.
    """
    _ms_keys = {0}
    _kb_keys = {Kb.Keys.W, Kb.Keys.A, Kb.Keys.S, Kb.Keys.D, Kb.Keys.UP, Kb.Keys.DOWN,
                Kb.Keys.LEFT, Kb.Keys.RIGHT, Kb.Keys.ENTER, Kb.Keys.SPACE, Kb.Keys.ESC}
    _gp_keys = {Gp.Keys.RT, Gp.Keys.START, Gp.Keys.LS, Gp.Keys.RS}
    _system = {Sys.Events.QUIT}
    _gamepad = None
    _stick_sens = (11 - Conf.Control.Stick.SENSITIVITY) * 2 / 10

    @staticmethod
    def get_events():
        """
        Main thread's cycle.
        Checks devices state, writes events if it has them
        Can be safely closed by calling <EventListener.object>.interrupt()
        """
        events = dict()
        # Checking devices
        events[Dvc.SYSTEM] = EventListener._check_system()
        events[Dvc.MOUSE] = EventListener._check_mouse()
        events[Dvc.KEYBOARD] = EventListener._check_keyboard()
        events[Dvc.GAMEPAD] = EventListener._check_gamepad()
        return events

    @staticmethod
    def _check_system():
        events = set()
        for event_type in EventListener._system:
            if pg.event.peek(event_type):
                event = Event(pg.QUIT, None)
                events.add(event)
        return events

    @staticmethod
    def _check_mouse():
        """
        Checks mouse buttons' state, mouse motion
        and collects it.
        """
        events = set()
        for key in EventListener._ms_keys:
            if pg.mouse.get_pressed(num_buttons=Conf.Control.Mouse.BUTTONS)[key]:
                events.add(Event(Ms.Events.KEY, key))
        rel = pg.mouse.get_rel()
        if rel != (0, 0):
            events.add(Event(Ms.Events.MOVE, (rel[0], -rel[1])))
        return events

    @staticmethod
    def _check_keyboard():
        """
        Checks keyboard buttons' state
        and collects pressed keys.
        """
        events = set()
        pressed = pg.key.get_pressed()
        for key in EventListener._kb_keys:
            if pressed[key]:
                events.add(Event(Kb.Events.KEY, key))
        return events

    @staticmethod
    def _check_gamepad():
        """
        Checks gamepad buttons' and sticks' state
        and collects it.
        """
        events = set()
        if pg.joystick.get_count() == 0:
            EventListener._gamepad = None
        else:
            if EventListener._gamepad is None:
                EventListener._gamepad = pg.joystick.Joystick(0)
            for btn_num in EventListener._gp_keys:
                if EventListener._gamepad.get_button(btn_num):
                    events.add(Event(Gp.Events.KEY, btn_num))
            x, y = EventListener.get_stick_axis(EventListener._gamepad, Conf.Control.Stick.L_DEAD_ZONE, 0, 1)
            if (x, y) != (0, 0):
                events.add(Event(Gp.Events.LS, (x, -y)))
            x, y = EventListener.get_stick_axis(EventListener._gamepad, Conf.Control.Stick.R_DEAD_ZONE, 3, 4)
            if (x, y) != (0, 0):
                events.add(Event(Gp.Events.RS, (x, -y)))
            if (EventListener._gamepad.get_axis(5) + 1) / 2 > Conf.Control.Trigger.DEAD_ZONE:
                events.add(Event(Gp.Events.KEY, Gp.Keys.RT))
        return events

    @staticmethod
    def get_stick_axis(gamepad: pg.joystick.Joystick, dead_zone: float, *axis_list: int) -> list[float]:
        out: list[float] = []
        for axis in axis_list:
            pos = gamepad.get_axis(axis)
            out.append(pow(abs(pos), EventListener._stick_sens) * (-1 if pos < 0 else 1))
        if hypot(*out) < dead_zone:
            out = [0] * len(axis_list)
        return out
