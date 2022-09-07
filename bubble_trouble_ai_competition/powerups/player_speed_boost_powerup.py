import pygame
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.types import SpeedTypes
from bubble_trouble_ai_competition.utils.load_display import Images


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
    
    def draw(self, screen: pygame.Surface):
        if self.active:
            # draw flash suit
            pass

        super().draw(screen, Images.powerups_images["speed_booster_powerup"])

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
    
    def copy_object(self):
        return type("PlayerSpeedBoostPowerupData", (PlayerSpeedBoostPowerup, ), self.get_powerup_data())
