
class Directions:
    """
    All available directions for the player to move in.
    """
    LEFT = -1
    RIGHT = 1

class Settings:
    """
    All settings for the game (FPS / Title \ ratios etc).
    """
    SCREEN_SIZE = (800, 600)
    SCREEN_WIDTH = SCREEN_SIZE[0]
    SCREEN_HEIGHT = SCREEN_SIZE[1]
    
    FPS = 30
    FRAME_TIME = 1 / FPS
    TITLE = "Bubble Trouble AI Competition"
    PLAYER_DIMENSIONS = (30, 100)
    PLAYER_WIDTH = PLAYER_DIMENSIONS[0]
    PLAYER_HEIGHT = PLAYER_DIMENSIONS[1]
    PLAYER_SPEED = 4
    BG_COLOR = (0, 0, 0)
    
