def get_border_clr(clr):
    CONTRAST = 50
    return '#%02x%02x%02x' % tuple(map(
        lambda x: max(0, x - CONTRAST),
        tuple(int(clr[i:i+2], 16) for i in (1, 3, 5))
    ))


class Configuration:
    # Window
    TITLE = "Tetris"
    WIN_HEIGHT = 1000  # px
    RESIZABLE = False
    BORDERS = True
    FULLSCREEN = False
    WITH_ICON = False
    ICON_PATH = "../tetris/icon/icon.gif"
    # Sizes
    X_BLOCKS = 10  # blocks
    Y_BLOCKS = 20  # blocks
    NEXT_PAD = 1  # blocks
    NEXT_BRD_WIDTH = 3  # px
    VERTICAL_MARGIN = 3
    OVERLAY_WIDTH = 300  # px
    FIELD_BRD_WIDTH = 3  # px
    DTL_BORDER_WIDTH = 5  # px
    # Colors
    BG_CLR = "#111"
    FG_CLR = "gray"
    TXT_CLR = "white"
    DTL_CLR = ["#515BD4", "#69E641", "#F3455D", "#F9C946", "#8F46D1", "#3EA23E", "#0FF0A5"]
    # Rules
    START_LEVEL = 1
    LEVEL_CONDITION = 8  # lines
    POINTS_FOR_LINES = [0, 100, 300, 700, 1500]
    DTL_TYPES = [
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ], [
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, 0]
        ], [
            [1, 1],
            [1, 1]
        ], [
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ], [
            [0, 1, 1],
            [0, 1, 0],
            [0, 1, 0]
        ], [
            [0, 0, 0],
            [0, 1, 1],
            [1, 1, 0]
        ], [
            [0, 0, 0],
            [1, 1, 0],
            [0, 1, 1]
        ]
    ]
    # Gamepad
    REFRESH_RATE = 30
    HOLD_LIMIT = 5
    # DON"T TOUCH
    DTL_BRD_CLR = list(map(get_border_clr, DTL_CLR))
    WIN_HEIGHT = WIN_HEIGHT - WIN_HEIGHT % Y_BLOCKS
    WIN_WIDTH = WIN_HEIGHT * X_BLOCKS // Y_BLOCKS + OVERLAY_WIDTH
    DTL_OFFSET = DTL_BORDER_WIDTH // 2
    DTL_SIZE = WIN_HEIGHT // Y_BLOCKS
