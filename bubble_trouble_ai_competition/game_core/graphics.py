import pygame
from bubble_trouble_ai_competition.base_objects.arrow_shot import ArrowShot
from bubble_trouble_ai_competition.base_objects.base_ball import Ball

from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.utils.constants import Settings

class Graphics:
    """
    Will handle the graphics.
    """
    
    def __init__(self, screen_size: tuple = (800, 600), background_color: tuple = Settings.BG_COLOR):
        """
        Initialize the graphics.

        Args:
            screen_size (tuple): The size of the screen.
            background_color (tuple): The background color.
        """

        # Store initial values.
        self.screen_size = screen_size
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.background_color = background_color

        # Initialize the pygame module.
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
    
    
    def draw(self, ais: list[BasePlayer], balls: list[Ball], shots: list[ArrowShot], powerups: list[Powerup]) -> None:
        """
        Draw the game objects.

        Args:
            ais (list[BasePlayer]): The players to draw.
            balls (list[Ball]): The balls to draw.
            shots (list[ArrowShot]): The shots to draw.
        """
        # Clear the screen.
        self.screen.fill(self.background_color)

        all_items = balls + shots + ais + powerups

        # Draw the ais.
        for item in all_items:
            item.draw(self.screen)

        # Updating the screen.
        pygame.display.flip()

