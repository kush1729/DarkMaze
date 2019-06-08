WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (34, 139, 34)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
GOLDENROD = (218, 165, 32)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 191, 255)
DARKBLUE = (0, 0, 175)
SKYBLUE = (135, 206, 235)
LIGHTGREY = (218, 218, 218)
GREY = (126, 126, 126)
DARKGREY = (80, 80, 80)
TOMATO = (255, 99, 71)
SIENNA = (160, 82, 45)
DARKORANGE = (255, 120, 0)
PURPLE = (160, 32, 240)
ORANGE = (255, 165, 0)
PEACH = (255, 218, 185)
GREENYELLOW = (173, 255, 47)
PINK = (255, 181, 197)
CYAN = (0, 255, 255)
BROWN = (165, 42, 42)

darkColours = (BLACK, DARKGREEN, DARKBLUE, DARKGREY)

def getFontColour(c):
    """Gets the font colour that looks best on a background of colour c.
Will return only black/white colours."""
    if c in darkColours:
        return WHITE
    return BLACK
