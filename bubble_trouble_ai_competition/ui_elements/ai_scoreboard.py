import pygame
from bubble_trouble_ai_competition.utils.constants import DesignConstants, ScoreboardConstants
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer

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


    def draw(self, screen: pygame.Surface):
        """
        Draw the player's score board.
        """
        # Drawing the background of the scoreboard.
        i = load_and_scale_image(ScoreboardConstants.SCOREBOARD_IMAGE_PATH, ScoreboardConstants.SCOREBOARD_WIDTH, ScoreboardConstants.SCOREBOARD_HEIGHT)
      
        text_surface = DesignConstants.MID_BOTTON_FONT.render(f'{self.ai.name}: {self.ai.score}', True, (255, 255, 255))
        screen.blit(i, (self.x, self.y))
        screen.blit(text_surface, (self.x + ScoreboardConstants.HORIZONTAL_TEXT_MARGINS, self.y + ScoreboardConstants.VERTICAL_TEXT_MARGINS + 1))
