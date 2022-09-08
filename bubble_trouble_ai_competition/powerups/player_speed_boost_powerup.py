import pygame
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.types import SpeedTypes
from bubble_trouble_ai_competition.utils.load_display import Images
from bubble_trouble_ai_competition.utils.constants import PowerupsSettings


class PlayerSpeedBoostPowerup(Powerup):
    """
    Power up that increases the player's speed.
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
        self.powerup_image_key = PowerupsSettings.SPEED_BOOSTER_POWERUP


    def draw(self, screen: pygame.Surface):

        super().draw(screen)


    def activate(self, player: BasePlayer) -> None:
        """
        Activates the power up.
        Change the player's speed to the power up's value.
        
    Args:
            player (Player): The player to activate.
        """
        player.speed = SpeedTypes.FAST
        super().activate(player)

    def deactivate(self) -> None:
        """
        Deactivates the power up.
        Change the player's speed back to normal.

    Args:
            player (Player): The player to deactivate.
        """
        self.player.speed = SpeedTypes.NORMAL
        super().deactivate()
    