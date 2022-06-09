import pygame

from bubble_trouble_ai_competition.utils.constants import Directions
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer

class manualAI(BasePlayer):
    def __init__(self) -> None:
        """
        Constructs the manual AI.
        """
        super().__init__("manual", Directions.RIGHT)
    
    def pick_direction(self) -> Directions:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            return Directions.LEFT
        
        if keys[pygame.K_RIGHT]:
            return Directions.RIGHT
        
        return self.direction
