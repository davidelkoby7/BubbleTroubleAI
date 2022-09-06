import pygame
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.constants import Settings, PowerupsSettings
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image
from bubble_trouble_ai_competition.utils.types import SpeedTypes

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
        powerup_image_name =  "player_speed_slower_powerup.png" if not random else "random_powerup.png"
        self.powerup_image = load_and_scale_image(Settings.ASSETS_DIR + "/" +  powerup_image_name, self.width, self.height)

        self.mud_slower_image =  load_and_scale_image(Settings.ASSETS_DIR + "/" +  "mud.png", PowerupsSettings.MUG_WIDTH, PowerupsSettings.MUG_HEIGHT)
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the power up.
        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        if self.active:
            screen.blit(self.mud_slower_image, (self.player.get_player_left_hand_coordinates()[0], self.player.get_player_top_left_corner()[1] + self.player.height - PowerupsSettings.MUG_SPACING))
        else:
            screen.blit(self.powerup_image, pygame.Rect(self.x, self.y, self.width, self.height))
    
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
        Change the player's speed back to normal.

    Args:
            player (Player): The player to deactivate.
        """
        self.player.speed = SpeedTypes.NORMAL
        super().deactivate()
    

    def copy_object(self):
        return type("PlayerSpeedSlowerPowerupData", (PlayerSpeedSlowerPowerup, ), self.get_powerup_data())
