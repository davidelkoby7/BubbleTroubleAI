import pygame
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.constants import Settings, PowerupsSettings
from bubble_trouble_ai_competition.utils.types import SpeedTypes
from bubble_trouble_ai_competition.utils.load_display import Images


class PlayerSpeedSlowerPowerup(Powerup):
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
        self.powerup_image_key = PowerupsSettings.SPEED_SLOWER_POWERUP



    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the power up.
        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        if self.active:
            screen.blit(Images.powerups_images[PowerupsSettings.MUD], (self.player.get_player_left_hand_coordinates()[0], self.player.get_player_top_left_corner()[1] + self.player.height - PowerupsSettings.MUD_SPACING))
        
        super().draw(screen)
    
    def activate(self, player: BasePlayer) -> None:
        """
        Activates the power up.
        Change the player's speed to the power up's value.
        
    Args:
            player (Player): The player to activate.
        """
        player.speed = SpeedTypes.SLOW
        super().activate(player)

    def deactivate(self) -> None:
        """
        Deactivates the power up.
        Change the player's speed back to normal if the player doesn't have other
        active PlayerSpeedSlowerPowerup.

    Args:
            player (Player): The player to deactivate.
        """
        if self.player.active_powerups.count(self.powerup_image_key) == 1:
            self.player.speed = SpeedTypes.NORMAL
        super().deactivate()
    