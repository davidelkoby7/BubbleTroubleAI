import pygame
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.utils.constants import PowerupsSettings, Settings
from bubble_trouble_ai_competition.utils.load_display import Images


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
        self.powerup_image_key = PowerupsSettings.SHIELD_POWERUP
        

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the power up.
        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        if self.active:
            if self.player.is_ducking == True:
                screen.blit(Images.powerups_images[PowerupsSettings.DUCK_SHIELD], (self.player.get_player_top_left_corner()[0] - PowerupsSettings.SHIELD_SIZE_INCREASE / 2, self.player.get_player_top_left_corner()[1] - PowerupsSettings.SHIELD_SIZE_INCREASE / 2))

            else:
                screen.blit(Images.powerups_images[PowerupsSettings.SHIELD], (self.player.get_player_top_left_corner()[0] - PowerupsSettings.SHIELD_SIZE_INCREASE / 2, self.player.get_player_top_left_corner()[1] - PowerupsSettings.SHIELD_SIZE_INCREASE / 2))
        
        super().draw(screen)


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
