class Configuration:
    """
    Class containing settings of the components
    Don't require creating object
    """
    class System:
        FPS = 60
        GAME_SPEED = 60
        SCALE = GAME_SPEED / FPS

    class Window:
        TITLE = "Space Battle"
        FULLSCREEN = True
        WIDTH = 1000
        HEIGHT = 1000

    class Game:
        LOSE_DELAY = 900  # ms
        DIFFICULTY = [
                    ("novice", (1100, 10)),
                    ("easy", (900, 20)),
                    ("normal", (700, 30)),
                    ("hard", (650, 40)),
                    ("DEATH", (500, 50)),
                ]

    class Overlay:
        OPACITY = 90

        class Framerate:
            VISIBLE = True
            SIZE = 60
            COLOR = (255, 30, 30)
            X_OFFSET = 10
            Y_OFFSET = -5
            PERIOD = 200
            DELTA = 20

        class Score:
            SIZE = 64
            COLOR = (100, 255, 100)
            X_OFFSET = 10
            Y_OFFSET = -15
            DELTA = 100

        class Health:
            SIZE = 50
            MARGIN = 5
            X_OFFSET = 10
            Y_OFFSET = 5

    class Menu:
        GAME_VERSION = "1.0"
        AUTHORS = "Damir", "Artem", "Dmitriy"
        CONTACTS = ""
        THEME_COLOR = (0, 250, 0)
        FONT_COLOR = (0, 0, 0)

        class Title:
            X_OFFSET = 40
            Y_OFFSET = 40
            SIZE = 60

    class Piece:
        MIN_OPACITY = 60  # [0, 100]
        MAX_OPACITY = 90  # [0, 100]
        MIN_SIZE = 200  # px
        MAX_SIZE = 500  # px
        MAX_SPEED = 1
        QUANTITY = 5

    class Ship:
        SIZE = 150
        WEIGHT = 5
        POWER = 5
        RESIST = 0.05  # >= 0
        DEAD_SPEED = 0.2  # [0, 1)
        ANIM_SCALE = 2

    class Meteor:
        MAX_SIZE = 200
        MIN_SIZE = 70
        SIZES = 3
        MAX_LIFES = 3  # (Needs Rocket.DESTROYABLE = True)
        MAX_SPEED = 3
        TELEPORT = True
        ROTATING = True
        MAX_ROTATE_SPEED = 4
        QUANTITY = 0
        BY_TIME = True  # (Needs Meteor.TELEPORT = True for value True)
        PERIOD = 700
        ON_FIELD = False
        DECREASE_SIZE = False

    class Rocket:
        SIZE = 40  # px
        SPEED = 20  # > 0
        PERIOD = 200  # ms
        DESTROYABLE = True
        MAX_DISTANCE = 300  # px  (needs Rocket.UNLIMITED = False)
        UNLIMITED = True

    class Animation:
        DEFAULT_SIZE = 200
        FPS = 40

    class Image:
        SHIP = 0
        LIFE = 0
        ROCKET = 0
        MENU_BG = 0
        STATIC_BG = 0

        class Format:
            ANIM = "gif"
            SPRITE = "png"
            BASIC = "jpg"

    class Sound:
        SHOOT = 0
        CLICK = 0
        BG_MENU = 0
        BG_GAME = 0
        FORMAT = "mp3"

        class Volume:
            GENERAL = 2  # [0; 10]
            BG = 7  # [0; 10]
            SFX = 3  # [0; 10]

    class Control:
        ESC_PERIOD = 500  # ms

        class Mouse:
            BUTTONS = 3
            ACCURACY = 10  # [1; 10]
            SMOOTH = 10  # >= 1

        class Stick:
            SENSITIVITY = 5  # [1; 10]
            L_DEAD_ZONE = 0.2  # [0; 1)
            R_DEAD_ZONE = 0.2  # [0; 1)

        class Trigger:
            DEAD_ZONE = 0.5  # [0; 1)

    class Rules:
        LIFES = 3

    # Checking parameters
    assert Game.LOSE_DELAY > 0
    assert 0 <= Ship.RESIST
    assert 0 < Ship.DEAD_SPEED < 1
    assert Control.Mouse.SMOOTH >= 1
    assert 1 <= Control.Mouse.ACCURACY <= 10
    assert Meteor.MAX_SIZE >= Meteor.MIN_SIZE
    assert Rocket.SPEED > 0
    assert 0 <= Control.Stick.SENSITIVITY <= 10
    assert 0 <= Control.Stick.L_DEAD_ZONE < 1
    assert 0 <= Control.Stick.R_DEAD_ZONE < 1
    assert 0 <= Control.Trigger.DEAD_ZONE < 1
    assert 0 <= Piece.MIN_OPACITY <= 100
    assert 0 <= Piece.MAX_OPACITY <= 100
    assert 1 <= Sound.Volume.GENERAL <= 10
    assert 1 <= Sound.Volume.SFX <= 10
    assert 1 <= Sound.Volume.BG <= 10
    assert Animation.FPS <= System.FPS
