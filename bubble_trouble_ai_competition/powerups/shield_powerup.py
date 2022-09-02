import pygame
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.utils.constants import PowerupsSettings, Settings
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image, load_image_and_keep_aspect_ratio


class ShieldPowerup(Powerup):
    """
    Powerup that protects the player from bubble collisions.
    """
    def __init__(self, x: int, y: int, speed_y: float, gravity: float = ..., random = False) -> None:
        """
        Initializes the power up.
        Args:
            x (int): The x coordinate of the power up.
            y (int): The y coordinate of the power up.
            speed_y (float): The vertical speed of the power up.
            gravity (float): The gravity which will affect the power up.
            random (boolean): True if powerup picked by random, decided which powerup image to set (random or the original powerup image).
        """
        super().__init__(x, y, speed_y, gravity)
        powerup_image_name =  "shield_powerup.png" if not random else "random_powerup.png"
        self.powerup_image = load_and_scale_image(Settings.ASSETS_DIR + "/" +  powerup_image_name, self.width, self.height) 
        self.shield_image = load_and_scale_image(Settings.ASSETS_DIR + "/" +  "shield.png", PowerupsSettings.SHIELD_WIDTH, PowerupsSettings.SHIELD_HEIGHT)


    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the power up.
        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        if self.active:
            screen.blit(self.shield_image, (self.player.get_player_top_left_corner()[0] - PowerupsSettings.SHIELD_SIZE_INCREASE / 2, self.player.get_player_top_left_corner()[1] - PowerupsSettings.SHIELD_SIZE_INCREASE / 2))
        else:
            screen.blit(self.powerup_image, pygame.Rect(self.x, self.y, self.width, self.height))


    def activate(self, player) -> None:
        """
        Activates the power up.
        Change the player's shield to the power up's value.
        Args:
            player (Player): The player to activate.
        """
        player.shield = True
        super().activate(player)
    
    def deactivate(self) -> None:
        """
        Deactivates the power up.
        Change the player's shield to False.
        """
        self.player.shield = False
        super().deactivate()
    
    
