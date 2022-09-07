import os
import pygame
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image, load_image_and_keep_aspect_ratio
from bubble_trouble_ai_competition.utils.constants import Settings, PowerupsSettings, DisplayConstants, CountdownBarConstants

class DisplayObjects:

    screen: pygame.Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_size = screen.get_size()
    rect_countdown_image = None       
    countdown_rect = None

def load_display_objects():

    DisplayObjects.rect_countdown_image = pygame.Surface((CountdownBarConstants.BAR_WIDTH,
                        CountdownBarConstants.BAR_HEIGHT))
    DisplayObjects.rect_countdown_image.fill(CountdownBarConstants.LOADING_COLOR)
    DisplayObjects.countdown_rect = DisplayObjects.rect_countdown_image.get_rect(topleft=(CountdownBarConstants.BAR_POSITION))
    
class Images:
    players_images: dict = {}
    powerups_images: dict = {}
    balls_images: dict = {}
    arrows_images: dict = {}
    general_images: dict = {}

       
def load_game_images():
    """Called once from game manager, load all game images."""

    Images.powerups_images = load_all_powerups_images()
    Images.balls_images = load_balls_images()
    Images.arrows_images = load_arrows_images()
    Images.players_images = load_all_players_images()
    Images.general_images = load_general_images()


def load_and_scale_powerup_image(powerup_image_path) -> pygame.Surface:
    return load_and_scale_image(powerup_image_path, Settings.POWERUP_WIDTH, Settings.POWERUP_HEIGHT) 


def load_and_scale_all_ball_sizes(ball_image_path) -> list[pygame.Surface]:
    """Return list of ball images from the biggest ball image to the smallest ball image."""
    radius_sizes = [size* Settings.BALL_SIZE_TO_RADIUS_RATIO for size in Settings.BALL_SIZES]
    return [load_and_scale_image(ball_image_path, radius * 2, radius * 2) for radius in radius_sizes] 


def load_general_images():
    """ Load games general images (like background and main menu images) """

    return {"background_image": load_and_scale_image(Settings.BACKGROUND_IMAGE_PATH, *DisplayConstants.GAME_AREA_SIZE),
            "menu_background_image": load_and_scale_image(Settings.MENU_BACKGROUND_IMAGE_PATH, *DisplayObjects.screen_size)}


def load_balls_images() -> dict[str, list[pygame.Surface]]:
    """ Load all balls images."""
    
    return {
        "blue_ball": load_and_scale_all_ball_sizes(Settings.BLUE_BALL_IMAGE_PATH),
        "green_ball": load_and_scale_all_ball_sizes(Settings.GREEN_BALL_IMAGE_PATH),
        "yellow_ball": load_and_scale_all_ball_sizes(Settings.YELLOW_BALL_IMAGE_PATH),
        "red_ball": load_and_scale_all_ball_sizes(Settings.RED_BALL_IMAGE_PATH),
        "purple_ball": load_and_scale_all_ball_sizes(Settings.PURPLE_BALL_IMAGE_PATH)
        }


def load_arrows_images() -> dict[str, pygame.Surface]:
    """ Load all arrows images."""
    return {"grey_arrow" : load_image_and_keep_aspect_ratio(Settings.GREY_ARROW_IMAGE_PATH, Settings.ARROW_WIDTH)}


def load_all_powerups_images() -> dict[str, pygame.Surface]:
    """ Load all powerups icons and actions."""

    return {"random_powerup": load_and_scale_powerup_image(PowerupsSettings.RANDOM_POWERUP_IMAGE_PATH),
            "freeze_powerup": load_and_scale_powerup_image(PowerupsSettings.ICE_CROWN_IMAGE_PATH),
            "ice_crown": load_and_scale_image(PowerupsSettings.ICE_CROWN_IMAGE_PATH, PowerupsSettings.ICE_CROWN_WIDTH, PowerupsSettings.ICE_CROWN_HEIGHT),
            "ice_cube": load_and_scale_image(PowerupsSettings.ICE_CUBE_IMAGE_PATH, PowerupsSettings.ICE_CUBE_WIDTH, PowerupsSettings.ICE_CUBE_HEIGHT).set_alpha(128),
            "ice_freeze": load_and_scale_image(PowerupsSettings.ICE_FREEZE_IMAGE_PATH, PowerupsSettings.ICE_FREEZE_WIDTH, PowerupsSettings.ICE_FREEZE_HEIGHT),
            "speed_slower_powerup": load_and_scale_powerup_image(PowerupsSettings.SPEED_SLOWER_POWERUP_IMAGE_PATH),
            "mud": load_and_scale_image(PowerupsSettings.MUD_IMAGE_PATH, PowerupsSettings.MUD_WIDTH, PowerupsSettings.MUD_HEIGHT),
            "speed_booster_powerup": load_and_scale_powerup_image(PowerupsSettings.SPEED_BOOSTER_POWERUP_IMAGE_PATH),
            "flash_suit": load_and_scale_image(PowerupsSettings.FLASH_SUIT_IMAGE_PATH, Settings.PLAYER_WIDTH, Settings.PLAYER_HEIGHT),
            "punch_powerup": pygame.transform.rotate(load_and_scale_powerup_image(PowerupsSettings.PUNCH_POWERUP_IMAGE_PATH), 270),
            "active_left_punch": load_and_scale_image(PowerupsSettings.PUNCH_ACTION_IMAGE_PATH, PowerupsSettings.PUNCH_WIDTH, PowerupsSettings.PUNCH_HEIGHT),
            "left_action_punch": load_and_scale_image(PowerupsSettings.PUNCH_ACTION_IMAGE_PATH, PowerupsSettings.PUNCH_ACTION_WIDTH, PowerupsSettings.PUNCH_ACTION_HEIGHT),
            "left_collision_punch": load_and_scale_image(PowerupsSettings.PUNCH_POWERUP_IMAGE_PATH, PowerupsSettings.PUNCH_ACTION_WIDTH, PowerupsSettings.PUNCH_ACTION_HEIGHT),
            "shield_powerup": load_and_scale_powerup_image(PowerupsSettings.SHIELD_POWERUP_IMAGE_PATH),
            "shield": load_and_scale_image(PowerupsSettings.SHIELD_IMAGE_PATH, PowerupsSettings.SHIELD_WIDTH, PowerupsSettings.SHIELD_HEIGHT),
            "double_points_powerup": load_and_scale_powerup_image(PowerupsSettings.DOUBLE_POINTS_POWERUP_IMAGE_PATH),
            "double_points_arrow": load_image_and_keep_aspect_ratio(PowerupsSettings.DOUBLE_POINTS_ARROW_IMAGE_PATH, Settings.ARROW_WIDTH)
            }


def load_all_players_images() -> None:
    # Player constant images
    players_images = {}
    for ai_dir in [ai_dir for ai_dir in next(os.walk(Settings.BASE_AI_DIR))[1] if "__" not in ai_dir]:
        player_head_image = load_and_scale_image(Settings.BASE_AI_DIR + "\\" + ai_dir + "\\" + Settings.PLAYER_HEAD_IMAGE_NAME, Settings.HEAD_RADIUS * 2, Settings.HEAD_RADIUS * 2)
        player_right_head_image = load_and_scale_image(Settings.BASE_AI_DIR + "\\" + ai_dir + "\\" + Settings.PLAYER_HEAD_RIGHT_IMAGE_NAME, Settings.HEAD_RADIUS * 2, Settings.HEAD_RADIUS * 2)
        player_left_head_image = load_and_scale_image(Settings.BASE_AI_DIR + "\\" + ai_dir + "\\" + Settings.PLAYER_HEAD_LEFT_IMAGE_NAME, Settings.HEAD_RADIUS * 2, Settings.HEAD_RADIUS * 2)
        player_duck_body_image = load_and_scale_image(Settings.BASE_AI_DIR + "\\" + ai_dir + "\\" + Settings.PLAYER_BODY_IMAGE_NAME, Settings.PLAYER_WIDTH, Settings.PLAYER_DUCK_HEIGHT)
        player_stand_body_image = load_and_scale_image(Settings.BASE_AI_DIR + "\\" + ai_dir + "\\" + Settings.PLAYER_BODY_IMAGE_NAME, Settings.PLAYER_WIDTH, Settings.PLAYER_HEIGHT)
        ai_name = ai_dir.replace("_images", "")
        players_images[ai_name] = {"head": player_head_image,
                                        "right_head": player_right_head_image,
                                        "left_head": player_left_head_image,
                                        "duck_body": player_duck_body_image,
                                        "stand_body": player_stand_body_image}
    return players_images


def get_ball_image(ball_color, ball_size):
    return Images.balls_images[ball_color + "_ball"][ball_size-1]

def get_arrow_image(arrow_color):
    return Images.arrows_images[arrow_color + "_arrow"]

def get_ai_images(ai_name):
    return Images.players_images[ai_name]
