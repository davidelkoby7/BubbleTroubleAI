import pygame
from bubble_trouble_ai_competition.base_objects.base_ball import Ball

from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
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
    
    
    def draw(self, ais: list[BasePlayer], balls: list[Ball]):
        """
        Draw the game objects.

        Args:
            ais (list[BasePlayer]): The players to draw.
            balls (list[Ball]): The balls to draw.
        """
        # Clear the screen.
        self.screen.fill(self.background_color)

        # Draw the ais.
        for ai in ais:
            self.draw_ai(ai)

        # Draw the balls.
        for ball in balls:
            self.draw_ball(ball)

        # Updating the screen.
        pygame.display.flip()


    def draw_ai(self, ai: BasePlayer):
        """
        Draws an ai.

        Args:
            ai (BasePlayer): The ai to draw.
        """
        # Drawing body
        pygame.draw.rect(self.screen, ai.color, pygame.Rect(ai.x, ai.y, ai.width, ai.height))

        # Drawing head
        pygame.draw.circle(self.screen, ai.color, (int(ai.head_center[0]), int(ai.head_center[1])), ai.head_radius)


    def draw_ball(self, ball: Ball):
        """
        Draws a ball.

        Args:
            ball (Ball): The ball to draw.
        """
        pygame.draw.circle(self.screen, ball.color, (int(ball.x), int(ball.y)), ball.radius)
