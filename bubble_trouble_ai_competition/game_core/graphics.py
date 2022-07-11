import pygame
from bubble_trouble_ai_competition.base_objects.arrow_shot import ArrowShot
from bubble_trouble_ai_competition.base_objects.base_ball import Ball

from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.ui_elements.ai_scoreboard import AIScoreboard
from bubble_trouble_ai_competition.utils.constants import DesignConstants, Settings
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image

class Graphics:
    """
    Will handle the graphics.
    """
    
    def __init__(self):
        """
        Initialize the graphics.

        Args:
            screen_size (tuple): The size of the screen.
            background_color (tuple): The background color.
        """

        # Store initial values.
        self.screen_size = Settings.SCREEN_SIZE
        self.screen_width = self.screen_size[0]
        self.screen_height = self.screen_size[1]

        self.game_area_size = Settings.GAME_AREA_SIZE
        self.game_area_width = self.game_area_size[0]
        self.game_area_height = self.game_area_size[1]

        self.game_area_position = Settings.GAME_AREA_POSITION

        # Initialize the pygame module.
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)

        # Loading the background image. 
        self.background_image = load_and_scale_image(Settings.BACKGROUND_IMAGE_PATH, self.game_area_width, self.game_area_height)

        # Handling constants
        DesignConstants.BASE_FONT = pygame.font.SysFont(DesignConstants.BASE_FONT_NAME, DesignConstants.BASE_FONT_SIZE)
    
    
    def draw(self, ais: list[BasePlayer], balls: list[Ball], shots: list[ArrowShot], scoreboards: list[AIScoreboard]) -> None:
        """
        Draw the game objects.

        Args:
            ais (list[BasePlayer]): The players to draw.
            balls (list[Ball]): The balls to draw.
            shots (list[ArrowShot]): The shots to draw.
        """
        # Clear the screen.
        self.screen.fill((0, 0, 0))

        # Draw background.
        self.screen.blit(self.background_image, Settings.GAME_AREA_POSITION)

        all_items = scoreboards + balls + shots + ais

        # Draw the ais.
        for item in all_items:
            item.draw(self.screen)

        # Updating the screen.
        pygame.display.flip()

