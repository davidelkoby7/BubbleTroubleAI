import pygame
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.utils.constants import DisplayConstants, PowerupsSettings, Settings
from bubble_trouble_ai_competition.utils.load_display import Images


class TeleportPowerup(Powerup):
    """
    Powerup that give player the abilitiy to freeze other player.
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
        self.action = False
        self.was_teleported = False
        super().__init__(x, y, speed_y, gravity)
    

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the power up.
        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        if self.active and self.action == True:

             # Draw the teleport on player.
            screen.blit(Images.powerups_images[PowerupsSettings.TELEPORT], (self.player.x - self.player.width - self.player.head_radius*2, PowerupsSettings.TELEPORT_Y - self.player.head_radius*2))
            self.was_teleported = True


        elif self.active:
            pass
            # Draw the teleport on player.
            #screen.blit(Images.powerups_images[PowerupsSettings.TELEPORT], (self.player.x - self.player.width - self.player.head_radius*2, PowerupsSettings.TELEPORT_Y - self.player.head_radius*2))
            #screen.blit(Images.powerups_images[PowerupsSettings.TELEPORT], (self.player.x - self.player.width - self.player.head_radius*2, PowerupsSettings.TELEPORT_Y - self.player.head_radius*2))
        
        super().draw(screen, Images.powerups_images[PowerupsSettings.TELEPORT_POWERUP])



    def activate(self, player) -> None:
        """
        Activates the power up and set on the ability of user to freeze.
        Args:
            player (Player): The player to activate.
        """
        player.can_teleport = True
        super().activate(player)
    

    def deactivate(self) -> None:
        """
        Deactivates the power up and release the freezed player.
        """
        self.action = False
        self.player.can_teleport = False
        self.player.is_teleporting = False

        super().deactivate()
    

         
        