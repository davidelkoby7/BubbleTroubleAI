
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
    DUCK = 2 # initialize random number only for the DUCK identifier


class Settings:
    """
    All settings for the game (FPS / Title \ ratios etc).
    """
    
    FPS = 60 
    FRAME_TIME = 1 / FPS
    TOTAL_GIME_FRAMES = 20 # Game during in seconds.
    FREEZE_ALERT_TIME = 10 # Freeze time in milliseconds .
    FRAMES_TIMEOUT = TOTAL_GIME_FRAMES * FPS # In units of frames.
    FRAMES_FREEZE = FREEZE_ALERT_TIME * FPS # In units of frames.
    TITLE = "Bubble Trouble AI Competition"
    BG_COLOR = (0, 0, 0)

    PLAYER_DIMENSIONS = (1.5, 3) # In units of screen bits.
    PLAYER_WIDTH = PLAYER_DIMENSIONS[0] # In units of screen bits.
    PLAYER_HEIGHT = PLAYER_DIMENSIONS[1] # In units of screen bits.
    PLAYER_DUCK_HEIGHT = PLAYER_HEIGHT * 0.3 # In units of screen bits.
    HEAD_RADIUS = PLAYER_DIMENSIONS[0] / 2 # In units of screen bits.
    PLAYER_SPEED = 20 # In units of screen bits per second.

    BALL_SPEED = 10 # In units of screen bits per second.
    DEFAULT_GRAVITY = 25 # In units of screen bits per second^2.
    BALL_SIZE_TO_RADIUS_RATIO = 0.6
    BALL_POPPED_DOWN_SPEED = -20 # In units of screen bits per second.
    BALL_POPPED_UP_SPEED_DEC = 2 # In units of screen bits per second.

    ARROW_WIDTH = 0.7 # In units of screen bits.
    ARROW_SPEED = 25 # In units of screen bits per second.

    BASE_MODULE_DIR = __file__ [:-18] # The minus 18 - to remove the part of the path until the base of our module. TODO: FIX THIS SHIT
    ASSETS_DIR = BASE_MODULE_DIR + "assets"
    BACKGROUND_IMAGE_PATH = ASSETS_DIR + "/background.jpg"

settings_properties_to_scale = [
    'PLAYER_DIMENSIONS', 'PLAYER_WIDTH', 'PLAYER_HEIGHT', 'PLAYER_DUCK_HEIGHT', 'HEAD_RADIUS', 'ARROW_WIDTH',
    'ARROW_SPEED', 'PLAYER_SPEED', 'BALL_SPEED', 'BALL_POPPED_UP_SPEED_DEC',
    'BALL_POPPED_DOWN_SPEED', 'DEFAULT_GRAVITY', 'BALL_SIZE_TO_RADIUS_RATIO'
    ]

class DisplayConstants:
    # Will be initialized in the graphics part. Must happen after initializing pygame.
    SCREEN_SIZE = None
    SCREEN_WIDTH = None
    SCREEN_HEIGHT = None

    SCREEN_BIT = 1 / 100 # In units of screen width.

    # All are in units of screen bits.
    GAME_AREA_SIZE = (90, 40)
    GAME_AREA_POSITION = (2, 2)
    FLOOR_Y_VALUE = GAME_AREA_POSITION[1] + GAME_AREA_SIZE[1]
    CIELING_Y_VALUE = GAME_AREA_POSITION[1]
    LEFT_BORDER_X_VALUE = GAME_AREA_POSITION[0]
    RIGHT_BORDER_X_VALUE = GAME_AREA_POSITION[0] + GAME_AREA_SIZE[0]


class PowerupsSettings:
    SHIELD_SIZE_INCREASE = 1.5 # In units of screen bits.
    SHIELD_WIDTH = Settings.PLAYER_WIDTH + SHIELD_SIZE_INCREASE
    SHIELD_HEIGHT = Settings.PLAYER_HEIGHT + Settings.HEAD_RADIUS*2 + SHIELD_SIZE_INCREASE

    PUNCH_SPACING = 0.2 # In units of screen bits.
    PUNCH_WIDTH = Settings.PLAYER_WIDTH * 0.6
    PUNCH_HEIGHT = Settings.PLAYER_HEIGHT * 0.16
    
    PUNCH_ACTION_WIDTH = Settings.PLAYER_WIDTH * 1.5
    PUNCH_ACTION_HEIGHT =  Settings.PLAYER_HEIGHT * 0.16

powerup_constants_to_update = [x for x in dir(PowerupsSettings) if ("__" not in x)]

class Events:
    """
    All events that can be triggered in the game.
    """
    BALL_POPPED = "ball_popped"
    PLAYER_SHOT = "player_shot"
    POWERUP_PICKED = "powerup_picked"
    ARROW_OUT_OF_BOUNDS = "arrow_out_of_bounds"
    GAME_TIMEOUT = "game_timeout"
    SHOWED_ALERT = "showed_alert"
    PLAYER_LPUNCH = "player_left_punch"
    PLAYER_RPUNCH = "player_right_punch"
    PLAYER_UPUNCH = "player_up_punch"


ALL_EVENTS_LIST = [getattr(Events, x) for x in dir(Events) if "__" not in x]


# Currently - everything here (besides bg color) is in units of screen bits. Maybe change this later, but it seems to be better like this now.
class ScoreboardConstants:
    SCOREBOARD_SIZE = (10, 4) # In units of screen bits.
    SCOREBOARD_WIDTH = SCOREBOARD_SIZE[0]
    SCOREBOARD_HEIGHT = SCOREBOARD_SIZE[1]

    PLAYER_IMAGE_SIZE = (2, 2) # In units of screen bits.
    PLAYER_IMAGE_WIDTH = PLAYER_IMAGE_SIZE[0]
    PLAYER_IMAGE_HEIGHT = PLAYER_IMAGE_SIZE[1]

    HORIZONTAL_TEXT_MARGINS = 1 # In units of screen bits.
    VERTICAL_TEXT_MARGINS = 0.5 # In units of screen bits.

    BACKGROUND_COLOR = (70, 70, 70)
    SCOREBOARD_HEIGHT_SHIFT = 2 # In units of screen bits.
    SCOREBOARD_START_POSITION = (2, DisplayConstants.FLOOR_Y_VALUE + SCOREBOARD_HEIGHT_SHIFT) # In units of screen bits.
    SCOREBOARD_SPACING = 1 # In units of screen bits.


class DesignConstants:
    BASE_FONT_NAME = "Arial"
    BASE_FONT_SIZE = 1
    BASE_FONT = None # Will be initialized in the graphics part. Must happen after initializing pygame.

design_constants_properties_to_scale = [
    'BASE_FONT_SIZE'
]

class CountdownBarConstants:
   
    BAR_POSITION = (DisplayConstants.GAME_AREA_POSITION[0], DisplayConstants.FLOOR_Y_VALUE + 1)
    BAR_WIDTH = DisplayConstants.RIGHT_BORDER_X_VALUE - DisplayConstants.GAME_AREA_POSITION[0]
    BAR_HEIGHT = 1.2 # In units of screen bits
    COUNTDOWN_SCREEN_MARGIN = 0.1 # In units of screen bits

    BAR_COLOR = (70, 70, 70)
    LOADING_COLOR = (118,238,198)

countdown_bar_constants_to_update = [
    'BAR_HEIGHT', 'COUNTDOWN_SCREEN_MARGIN'
]

class AlertConstants:
    ALERT_FONT_NAME = "freesansbold.ttf"
    ALERT_FONT_SIZE = 5 # In units of screen bits
    ALERT_FONT = None # Will be initialized in the graphics part. Must happen after initializing pygame.


    AlERT_POSITION = ((DisplayConstants.LEFT_BORDER_X_VALUE + DisplayConstants.RIGHT_BORDER_X_VALUE)/DisplayConstants.SCREEN_BIT*2,
                    (DisplayConstants.CIELING_Y_VALUE + DisplayConstants.FLOOR_Y_VALUE)/DisplayConstants.SCREEN_BIT*2)

    ALERT_COLOR = (255,48,48)

alert_constants_to_update = [
    'ALERT_FONT_SIZE'
]

