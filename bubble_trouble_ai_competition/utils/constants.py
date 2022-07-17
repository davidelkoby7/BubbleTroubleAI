
class BallColors:
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    PURPLE = "purple"
    ORANGE = "orange"

ALL_BALL_COLORS = [getattr(BallColors, x) for x in dir(BallColors) if "__" not in x]    


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
    SCREEN_SIZE = (1600, 900)
    SCREEN_WIDTH = SCREEN_SIZE[0]
    SCREEN_HEIGHT = SCREEN_SIZE[1]

    GAME_AREA_SIZE = (1400, 550)
    GAME_AREA_POSITION = (50, 50)
    FLOOR_Y_VALUE = GAME_AREA_POSITION[1] + GAME_AREA_SIZE[1]
    CIELING_Y_VALUE = GAME_AREA_POSITION[1]
    LEFT_BORDER_X_VALUE = GAME_AREA_POSITION[0]
    RIGHT_BORDER_X_VALUE = GAME_AREA_POSITION[0] + GAME_AREA_SIZE[0]

    SCOREBOARD_HEIGHT_SHIFT = 30
    SCOREBOARD_START_POSITION = (LEFT_BORDER_X_VALUE, FLOOR_Y_VALUE + SCOREBOARD_HEIGHT_SHIFT)
    SCOREBOARD_SPACING = 30
    
    FPS = 60
    FRAME_TIME = 1 / FPS
    TITLE = "Bubble Trouble AI Competition"
    BG_COLOR = (0, 0, 0)

    PLAYER_DIMENSIONS = (30, 50)
    PLAYER_WIDTH = PLAYER_DIMENSIONS[0]
    PLAYER_HEIGHT = PLAYER_DIMENSIONS[1]
    HEAD_RADIUS = PLAYER_DIMENSIONS[0] / 2

    BALL_SPEED = 150
    DEFAULT_GRAVITY = 450
    BALL_SIZE_TO_RADIUS_RATIO = 10
    BALL_POPPED_DOWN_SPEED = -300
    BALL_POPPED_UP_SPEED_DEC = 25

    SHOTS_PER_SECOND = 4
    SHOOTING_DELAY = FPS / SHOTS_PER_SECOND # In units of frames
    ARROW_WIDTH = 10
    ARROW_SPEED = 500

    BASE_MODULE_DIR = __file__ [:-18] # The minus 18 - to remove the part of the path until the base of our module. TODO: FIX THIS SHIT
    ASSETS_DIR = BASE_MODULE_DIR + "assets"
    BACKGROUND_IMAGE_PATH = ASSETS_DIR + "/background.jpg"


class PowerupsSettings:
    SHIELD_WIDTH = Settings.PLAYER_WIDTH + 20
    SHIELD_HEIGHT = Settings.PLAYER_HEIGHT + Settings.HEAD_RADIUS*2 + 20
    

class Events:
    """
    All events that can be triggered in the game.
    """
    BALL_POPPED = "ball_popped"
    PLAYER_SHOT = "player_shot"
    POWERUP_PICKED = "powerup_picked"
    ARROW_OUT_OF_BOUNDS = "arrow_out_of_bounds"

ALL_EVENTS_LIST = [getattr(Events, x) for x in dir(Events) if "__" not in x]


class ScoreboardConstants:
    SCOREBOARD_SIZE = (200, 150)
    SCOREBOARD_WIDTH = SCOREBOARD_SIZE[0]
    SCOREBOARD_HEIGHT = SCOREBOARD_SIZE[1]

    PLAYER_IMAGE_SIZE = (50, 50)
    PLAYER_IMAGE_WIDTH = PLAYER_IMAGE_SIZE[0]
    PLAYER_IMAGE_HEIGHT = PLAYER_IMAGE_SIZE[1]

    HORIZONTAL_TEXT_MARGINS = 10
    VERTICAL_TEXT_MARGINS = 5

    BACKGROUND_COLOR = (70, 70, 70)


class DesignConstants:
    BASE_FONT_NAME = "Arial"
    BASE_FONT_SIZE = 20
    BASE_FONT = None # Will be initialized in the graphics part. Must happen after initializing pygame.

