class Configuration:
    """
    Class containing settings of the components
    Don't require creating object
    """
    class Window:
        TITLE = "Space Battle"
        FULLSCREEN = True
        WIDTH = 1000
        HEIGHT = 1000

    class Game:
        LOSE_DELAY = 9
        DIFFICULTY = [
                    ("novice", (1100, 10)),
                    ("easy", (900, 20)),
                    ("normal", (700, 30)),
                    ("hard", (650, 40)),
                    ("DEATH", (500, 50)),
                ]

    class Overlay:
        OPACITY = 90

        class Score:
            SIZE = 64
            COLOR = (100, 255, 100)
            X_OFFSET = 10
            Y_OFFSET = 5
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

        class Title:
            X_OFFSET = 40
            Y_OFFSET = 40
            SIZE = 60

    class Piece:
        MIN_OPACITY = 60  # [0, 100]
        MAX_OPACITY = 90  # [0, 100]
        MIN_SIZE = 100  # px
        MAX_SIZE = 300  # px
        MAX_SPEED = 1
        QUANTITY = 0

    class Ship:
        SIZE = 100
        WEIGHT = 5
        POWER = 5
        RESIST = 0.05  # >= 0
        SMOOTH = 10  # >= 1
        ACCURACY = 10  # [1; 10]
        DEAD_SPEED = 0.2  # [0, 1)
        ANIM_SCALE = 2

    class Meteor:
        MAX_SIZE = 200
        MIN_SIZE = 70
        SIZES = 3
        MAX_LIFES = 3  # (Need Rocket.DESTROYABLE = True)
        MAX_SPEED = 3
        TELEPORT = True
        ROTATING = True
        MAX_ROTATE_SPEED = 4
        QUANTITY = 25
        BY_TIME = True
        PERIOD = 700
        ON_FIELD = False

    class Rocket:
        SIZE = 10  # px
        SPEED = 20  # > 0
        PERIOD = 200  # ms
        DESTROYABLE = True
        MAX_DISTANCE = 300  # px  (needs Rocket.UNLIMITED = False)
        UNLIMITED = True

    class Animation:
        DEFAULT_SIZE = 200
        FPS = 30

    class Image:
        SHIP = 0
        LIFE = 0
        ROCKET = 0
        MENU_BG = 0
        STATIC_BG = 0
        ANIM_FORMAT = "gif"
        SPRITE_FORMAT = "png"
        BASIC_FORMAT = "jpg"

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
        MOUSE_BUTTONS = 3
        STICK_SENSITIVITY = 2  # [1; 10]
        STICK_DEAD_ZONE = 0.2  # [0; 1)
        TRIGGER_DEAD_ZONE = 0.5  # [0; 1)
        ESC_PERIOD = 500  # ms

    class Rules:
        LIFES = 3

    class System:
        FPS = 60
        GAME_SPEED = 60
        SCALE = GAME_SPEED / FPS

    # Checking parameters
    assert 0 <= Ship.RESIST
    assert 0 < Ship.DEAD_SPEED < 1
    assert Ship.SMOOTH >= 1
    assert 1 <= Ship.ACCURACY <= 10
    assert Meteor.MAX_SIZE >= Meteor.MIN_SIZE
    assert Rocket.SPEED > 0
    assert 0 <= Control.STICK_SENSITIVITY <= 10
    assert 0 <= Control.STICK_DEAD_ZONE < 1
    assert 0 <= Control.TRIGGER_DEAD_ZONE < 1
    assert 0 <= Piece.MIN_OPACITY <= 100
    assert 0 <= Piece.MAX_OPACITY <= 100
    assert 1 <= Sound.Volume.GENERAL <= 10
    assert 1 <= Sound.Volume.SFX <= 10
    assert 1 <= Sound.Volume.BG <= 10
