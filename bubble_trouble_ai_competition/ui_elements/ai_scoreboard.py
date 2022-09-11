import pygame
from bubble_trouble_ai_competition.utils.constants import DesignConstants, DisplayConstants, PowerupsSettings, ScoreboardConstants, Settings
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.load_display import Images, get_arrow_image
from bubble_trouble_ai_competition.utils.types import SpeedTypes

class AIScoreboard:
    """
    This class represents an ai's scoreboard.
    """

    def __init__(self, ai: BasePlayer, x: int, y: int):
        """
        Initialize the player's score board.
        """
        self.ai = ai
        self.x = x
        self.y = y
        self.text_color = DesignConstants.BASIC_FONT_COLOR

    def keep_powerup_in_border(self, powerup_x, powerup_y, powerup_width,powerups_initial_x):
        if (powerup_x + powerup_width) > (ScoreboardConstants.SCOREBOARD_WIDTH + self.x):
            ScoreboardConstants.SHIFT_DOWN_AMOUNT += 1
            return (powerups_initial_x, self.y + DisplayConstants.SCOREBOARD_SCREEN_HEIGHT/(2.3 - (ScoreboardConstants.SHIFT_DOWN_AMOUNT * 0.8)))
        else:
            return (powerup_x, powerup_y)


    def get_text_surface(self, text):
        return DesignConstants.MID_FONT.render(text, True, self.text_color)


    def draw(self, screen: pygame.Surface):
        """
        Draw the player's score board.
        """
        ScoreboardConstants.SHIFT_DOWN_AMOUNT = 0

        # Drawing the background of the scoreboard.
        scoreboard_image = load_and_scale_image(ScoreboardConstants.SCOREBOARD_IMAGE_PATH, ScoreboardConstants.SCOREBOARD_WIDTH, DisplayConstants.SCOREBOARD_SCREEN_HEIGHT)
        screen.blit(scoreboard_image, (self.x, self.y))

        # Drawing the ai's name.
        ai_name_surface = self.get_text_surface(self.ai.name)
        ai_name_rect = ai_name_surface.get_rect()
        ai_name_rect.center = (self.x + ScoreboardConstants.SCOREBOARD_AI_NAME_WIDTH_SHIFT, self.y + ScoreboardConstants.VERTICAL_TEXT_MARGINS)
        screen.blit(ai_name_surface, ai_name_rect)

        # Drawing the ai's arrow.
        arrow_image = load_and_scale_image(Settings.ASSETS_DIR + "\\" + self.ai.arrow_color + "_scoreboard_arrow.png", Settings.ARROW_WIDTH, ai_name_rect.h)
        screen.blit(arrow_image, (ai_name_rect.x + ai_name_rect.w , ai_name_rect.y, ai_name_rect.w, ai_name_rect.h))
        
        # Drawing the ai's score.
        ai_score_surface = self.get_text_surface(f'score: {self.ai.score}')
        screen.blit(ai_score_surface, (self.x + ScoreboardConstants.SCOREBOARD_SHIFT_RIGHT, self.y + DisplayConstants.SCOREBOARD_SCREEN_HEIGHT/4))

        # Drawing the ai's active powerups images.
        active_powerups_surface = self.get_text_surface('powerups:')
        screen.blit(active_powerups_surface, (self.x + ScoreboardConstants.SCOREBOARD_SHIFT_RIGHT, self.y + DisplayConstants.SCOREBOARD_SCREEN_HEIGHT/3))
        initial_x_powerups = self.x + ScoreboardConstants.POWERUPS_IMAGES_SHIFT_X 
        initial_y_powerups = self.y + DisplayConstants.SCOREBOARD_SCREEN_HEIGHT/2.3
        curr_x : int = initial_x_powerups
        curr_y : int = initial_y_powerups
        for active_powerup in set(self.ai.active_powerups):
            active_powerup_image = Images.powerups_images[active_powerup]
            curr_x, curr_y = self.keep_powerup_in_border(curr_x, curr_y, active_powerup_image.get_width() ,initial_x_powerups)
            screen.blit(active_powerup_image, (curr_x, curr_y))
            curr_x = curr_x + active_powerup_image.get_width() 
