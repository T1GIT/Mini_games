import tkinter as tk


class Settings:
    # Window
    TITLE = "Crosses and Zeros"
    # Sizes
    CELL_SIZE = 150  # px
    X_CELLS = 3
    Y_CELLS = 3
    MARGIN = 5  # px
    PADDING = 5  # px
    SIGN_SIZE = 60  # px
    BTN_TEXT_SIZE = 30
    BTN_HEIGHT = 40  # px
    # Rules
    REQ_LINE_LENGTH = 3
    SIGNS = ["❌", "⭕"]
    # Appearance
    RELIEF = tk.GROOVE
    FONT = "Ariel"
    # Colors
    SIGN_CLRS = ["purple", "pink"]
    BG_CLR = "black"
    CELL_CLR = "#333"
    ACT_CELL_CLR = "#444"
    TEXT_CLR = "white"
    ACT_TEXT_CLR = "white"
    MENU_BTN_CLR = "#555"
    ACT_MENU_BTN_CLR = "#666"
    # Don't touch
    assert len(SIGNS) <= len(SIGN_CLRS), "Isn't enough colors"

