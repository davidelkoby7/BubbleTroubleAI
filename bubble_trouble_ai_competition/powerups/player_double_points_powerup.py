import pygame
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.load_images import Images

class PlayerDoublePointsPowerup(Powerup):
    """
    Power up that double the player's earning points.
    """
    def __init__(self, x: int, y: int, speed_y: float, gravity: float = ..., random = False) -> None:
        """
        Initializes the power up.
        
        Args:
            x (int): The x coordinate of the power up.
            y (int): The y coordinate of the power up.
            random (boolean): True if powerup picked by random, decided which powerup image to set (random or the original powerup image).
        """
        super().__init__(x, y, speed_y, gravity)
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the power up.
        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        super().draw(screen, Images.powerups_images["double_points_powerup"])
    
    def activate(self, player: BasePlayer) -> None:
        """
        Activates the power up.        
    Args:
            player (Player): The player to activate.
        """
        player.double_points = True
        super().activate(player)

    def deactivate(self) -> None:
        """
        Deactivates the power up.

        """
        self.player.double_points = False
        super().deactivate()
    
