import pygame

from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.constants import Settings

class Graphics:
    """
    Will handle the graphics.
    """
    
    def __init__(self, screen_size: tuple = (800, 600), background_color: tuple = Settings.BG_COLOR):
        """
        Initialize the graphics.
        """

        # Store initial values.
        self.screen_size = screen_size
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.background_color = background_color

        # Initialize the pygame module.
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
    
    
    def draw(self, ais: list[BasePlayer]):
        """
        Draw the game objects.
        """
        # Clear the screen.
        self.screen.fill(self.background_color)

        # Draw the ais.
        for ai in ais:
            self.draw_ai(ai)

        # Updating the screen.
        pygame.display.flip()


    def draw_ai(self, ai: BasePlayer):
        """
        Draws an ai.
        """
        pygame.draw.rect(self.screen, ai.color, pygame.Rect(ai.x, self.screen_height - ai.y - ai.height, ai.width, ai.height))
