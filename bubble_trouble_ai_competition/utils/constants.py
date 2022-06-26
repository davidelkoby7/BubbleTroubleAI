
class Directions:
    """
    All available directions for the player to move in.
    """
    LEFT = -1
    RIGHT = 1
    STAND = 0


class Settings:
    """
    All settings for the game (FPS / Title \ ratios etc).
    """
    SCREEN_SIZE = (800, 600)
    SCREEN_WIDTH = SCREEN_SIZE[0]
    SCREEN_HEIGHT = SCREEN_SIZE[1]
    
    FPS = 60
    FRAME_TIME = 1 / FPS
    TITLE = "Bubble Trouble AI Competition"
    PLAYER_DIMENSIONS = (30, 70)
    PLAYER_WIDTH = PLAYER_DIMENSIONS[0]
    PLAYER_HEIGHT = PLAYER_DIMENSIONS[1]
    HEAD_RADIUS = PLAYER_DIMENSIONS[0] / 2
    PLAYER_SPEED = 180
    BALL_SPEED = 150
    BG_COLOR = (0, 0, 0)

    DEFAULT_GRAVITY = 450
    BALL_SIZE_TO_RADIUS_RATIO = 10

    SHOOTING_DELAY = FPS / 2 # In units of frames
    

class Events:
    """
    All events that can be triggered in the game.
    """
    BALL_POPPED = "ball_popped"
    PLAYER_SHOT = "player_shot"
    POWERUP_PICKED = "powerup_picked"

ALL_EVENTS_LIST = [getattr(Events, x) for x in dir(Events) if "__" not in x]
