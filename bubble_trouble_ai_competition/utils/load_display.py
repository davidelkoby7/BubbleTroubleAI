import os
import pygame
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image, load_image_and_keep_aspect_ratio
from bubble_trouble_ai_competition.utils.constants import Settings, PowerupsSettings, DisplayConstants, CountdownBarConstants, AlertConstants

class DisplayObjects:
    """Loads all game generals objects. """
    screen: pygame.Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_size = screen.get_size()
    rect_countdown_image = None       
    countdown_rect = None
    alerts: dict = {}

def load_alerts_surfaces():
    return {AlertConstants.ALERT_GAME_TIMEOUT: AlertConstants.ALERT_FONT.render(AlertConstants.GAME_TIMEOUT_TEXT, False, AlertConstants.ALERT_COLOR),
            AlertConstants.ALERT_GAME_OVER:  AlertConstants.ALERT_FONT.render(AlertConstants.GAME_OVER_TEXT, False, AlertConstants.ALERT_COLOR)}


def load_display_objects():

    DisplayObjects.rect_countdown_image = pygame.Surface((CountdownBarConstants.BAR_WIDTH,
                        CountdownBarConstants.BAR_HEIGHT))
    DisplayObjects.rect_countdown_image.fill(CountdownBarConstants.LOADING_COLOR)
    DisplayObjects.countdown_rect = DisplayObjects.rect_countdown_image.get_rect(topleft=(CountdownBarConstants.BAR_POSITION))
    DisplayObjects.alerts = load_alerts_surfaces()

class Images:
    players_images: dict = {}
    powerups_images: dict = {}
    balls_images: dict = {}
    arrows_images: dict = {}
    general_images: dict = {}

       
def load_game_images():
    """Called once from game manager, load all game images."""

    Images.powerups_images = load_all_powerups_images()
    Images.powerups_images[PowerupsSettings.ICE_CUBE].set_alpha(128)
    Images.players_images = load_all_players_images()
    Images.general_images = load_general_images()


def load_and_scale_powerup_image(powerup_image_path) -> pygame.Surface:
    return load_and_scale_image(powerup_image_path, Settings.POWERUP_WIDTH, Settings.POWERUP_HEIGHT) 


def load_general_images():
    """ Load games general images (like background and main menu images) """
    return {Settings.BACKGROUND_IMAGE_KEY: load_and_scale_image(Settings.BACKGROUND_IMAGE_PATH, *DisplayConstants.GAME_AREA_SIZE),
            Settings.MENU_BACKGROUND_IMAGE_KEY: load_and_scale_image(Settings.MENU_BACKGROUND_IMAGE_PATH, *DisplayObjects.screen_size)}


def load_ball_image(color, size):
    ball_image_path = Settings.ASSETS_DIR + "\\" + color + "_ball.png"
    ball_radius = size * Settings.BALL_SIZE_TO_RADIUS_RATIO
    Images.balls_images[color + "_ball"].update({size: load_and_scale_image(ball_image_path, ball_radius * 2, ball_radius * 2)})


def load_arrow_image(color) -> dict[str, pygame.Surface]:
    """ Load the arrow image by color."""
    Images.arrows_images.update({color + "_arrow": load_image_and_keep_aspect_ratio(Settings.ASSETS_DIR + "\\" + color + "_arrow.png", Settings.ARROW_WIDTH)})


def load_all_powerups_images() -> dict[str, pygame.Surface]:
    """ Load all powerups icons and actions."""
    
    return {
            PowerupsSettings.DEFAULT_POWERUP: load_and_scale_powerup_image(PowerupsSettings.DEFAULT_POWERUP_IMAGE_PATH),
            PowerupsSettings.RANDOM_POWERUP: load_and_scale_powerup_image(PowerupsSettings.RANDOM_POWERUP_IMAGE_PATH),
            PowerupsSettings.FREEZE_POWERUP: load_and_scale_powerup_image(PowerupsSettings.ICE_CROWN_IMAGE_PATH),
            PowerupsSettings.ICE_CROWN: load_and_scale_image(PowerupsSettings.ICE_CROWN_IMAGE_PATH, PowerupsSettings.ICE_CROWN_WIDTH, PowerupsSettings.ICE_CROWN_HEIGHT),
            PowerupsSettings.ICE_CUBE: load_and_scale_image(PowerupsSettings.ICE_CUBE_IMAGE_PATH, PowerupsSettings.ICE_CUBE_WIDTH, PowerupsSettings.ICE_CUBE_HEIGHT),
            PowerupsSettings.ICE_FREEZE: load_and_scale_image(PowerupsSettings.ICE_FREEZE_IMAGE_PATH, PowerupsSettings.ICE_FREEZE_WIDTH, PowerupsSettings.ICE_FREEZE_HEIGHT),
            PowerupsSettings.SPEED_SLOWER_POWERUP: load_and_scale_powerup_image(PowerupsSettings.SPEED_SLOWER_POWERUP_IMAGE_PATH),
            PowerupsSettings.MUD: load_and_scale_image(PowerupsSettings.MUD_IMAGE_PATH, PowerupsSettings.MUD_WIDTH, PowerupsSettings.MUD_HEIGHT),
            PowerupsSettings.SPEED_BOOSTER_POWERUP: load_and_scale_powerup_image(PowerupsSettings.SPEED_BOOSTER_POWERUP_IMAGE_PATH),
            PowerupsSettings.STAND_FLASH_SUIT: load_and_scale_image(PowerupsSettings.FLASH_SUIT_IMAGE_PATH, PowerupsSettings.FLASH_SUIT_WIDTH, PowerupsSettings.FLASH_SUIT_HEIGHT),
            PowerupsSettings.DUCK_FLASH_SUIT: load_and_scale_image(PowerupsSettings.FLASH_SUIT_IMAGE_PATH, PowerupsSettings.FLASH_SUIT_WIDTH, PowerupsSettings.DUCK_FLASH_SUIT_HEIGHT),
            PowerupsSettings.PUNCH_POWERUP: pygame.transform.rotate(load_and_scale_powerup_image(PowerupsSettings.PUNCH_POWERUP_IMAGE_PATH), 270),
            PowerupsSettings.ACTIVE_LEFT_PUNCH: load_and_scale_image(PowerupsSettings.PUNCH_ACTION_IMAGE_PATH, PowerupsSettings.PUNCH_WIDTH, PowerupsSettings.PUNCH_HEIGHT),
            PowerupsSettings.LEFT_ACTION_PUNCH: load_and_scale_image(PowerupsSettings.PUNCH_ACTION_IMAGE_PATH, PowerupsSettings.PUNCH_ACTION_WIDTH, PowerupsSettings.PUNCH_ACTION_HEIGHT),
            PowerupsSettings.LEFT_COLLISION_PUNCH: load_and_scale_image(PowerupsSettings.PUNCH_POWERUP_IMAGE_PATH, PowerupsSettings.PUNCH_ACTION_WIDTH, PowerupsSettings.PUNCH_ACTION_HEIGHT),
            PowerupsSettings.SHIELD_POWERUP: load_and_scale_powerup_image(PowerupsSettings.SHIELD_POWERUP_IMAGE_PATH),
            PowerupsSettings.SHIELD: load_and_scale_image(PowerupsSettings.SHIELD_IMAGE_PATH, PowerupsSettings.SHIELD_WIDTH, PowerupsSettings.SHIELD_HEIGHT),
            PowerupsSettings.DUCK_SHIELD: load_and_scale_image(PowerupsSettings.SHIELD_IMAGE_PATH, PowerupsSettings.SHIELD_WIDTH, PowerupsSettings.SHIELD_DUCKING_HEIGHT),
            PowerupsSettings.DOUBLE_POINTS_POWERUP: load_and_scale_powerup_image(PowerupsSettings.DOUBLE_POINTS_POWERUP_IMAGE_PATH),
            PowerupsSettings.DOUBLE_POINTS_ARROW: load_image_and_keep_aspect_ratio(PowerupsSettings.DOUBLE_POINTS_ARROW_IMAGE_PATH, Settings.ARROW_WIDTH)
            }


def load_all_players_images() -> None:
    # Player constant images
    players_images = {}
    
    for file_name in os.listdir(Settings.BASE_AI_DIR):
        # Skipping irrelevant files
        if (not file_name.endswith(".py") or file_name == "__init__.py"):
            continue

        ai_name = file_name[:-3] # The minus 3 => Removing the .py ending
        ai_folder_name = ai_name + "_images"
        player_head_image = load_and_scale_image(Settings.BASE_AI_DIR + "\\" + ai_folder_name + "\\" + Settings.PLAYER_HEAD_IMAGE_NAME, Settings.HEAD_RADIUS * 2, Settings.HEAD_RADIUS * 2)
        player_right_head_image = load_and_scale_image(Settings.BASE_AI_DIR + "\\" + ai_folder_name + "\\" + Settings.PLAYER_HEAD_RIGHT_IMAGE_NAME, Settings.HEAD_RADIUS * 2, Settings.HEAD_RADIUS * 2)
        player_left_head_image = load_and_scale_image(Settings.BASE_AI_DIR + "\\" + ai_folder_name + "\\" + Settings.PLAYER_HEAD_LEFT_IMAGE_NAME, Settings.HEAD_RADIUS * 2, Settings.HEAD_RADIUS * 2)
        player_duck_body_image = load_and_scale_image(Settings.BASE_AI_DIR + "\\" + ai_folder_name + "\\" + Settings.PLAYER_BODY_IMAGE_NAME, Settings.PLAYER_WIDTH, Settings.PLAYER_DUCK_HEIGHT)
        player_stand_body_image = load_and_scale_image(Settings.BASE_AI_DIR + "\\" + ai_folder_name + "\\" + Settings.PLAYER_BODY_IMAGE_NAME, Settings.PLAYER_WIDTH, Settings.PLAYER_HEIGHT)
        players_images[ai_name] = {
                                    Settings.PLAYER_HEAD: player_head_image,
                                    Settings.PLAYER_RIGHT_HEAD: player_right_head_image,
                                    Settings.PLAYER_LEFT_HEAD: player_left_head_image,
                                    Settings.PLAYER_DUCK_BODY: player_duck_body_image,
                                    Settings.PLAYER_STAND_BODY: player_stand_body_image}
    return players_images


def get_ball_image(ball_color: str, ball_size: int):
    """ Returns the ball image by color and size.
        If ball image not created yet, load it."""
    
    if ball_color + "_ball" not in Images.balls_images.keys():
        # Create the initial record of the ball color image at ball's dictionary.
        Images.balls_images[ball_color + "_ball"] = {}
    
    # Check if image of the colored ball size already loaded.
    if ball_size not in Images.balls_images[ball_color + "_ball"].keys():
        # Load the ball image by color and size.
        load_ball_image(ball_color, ball_size)

    return Images.balls_images[ball_color + "_ball"][ball_size]


def get_arrow_image(arrow_color):
    """Returns the arrow image by color.
       If arrow image not created yet, load it."""

    if arrow_color + "_arrow" not in Images.arrows_images.keys():
        # Load the arrow image by color.
        load_arrow_image(arrow_color)
    return Images.arrows_images[arrow_color + "_arrow"]


def get_ai_images(ai_name):
    """Returns the ai's images."""
    return Images.players_images[ai_name]
