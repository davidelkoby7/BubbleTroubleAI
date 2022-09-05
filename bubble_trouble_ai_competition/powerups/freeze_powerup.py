from tkinter import N
import pygame
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.utils.constants import DisplayConstants, PowerupsSettings, Settings
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image


class FreezePowerup(Powerup):
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
        super().__init__(x, y, speed_y, gravity)
        powerup_image_name =  "freeze_powerup.png" if not random else "random_powerup.png"
        self.powerup_image = load_and_scale_image(Settings.ASSETS_DIR + "/" +  powerup_image_name, self.width, self.height) 
        self.active_player_powerup = load_and_scale_image(Settings.ASSETS_DIR + "/" + "freeze_powerup.png", PowerupsSettings.ICE_CROWN_WIDTH, PowerupsSettings.ICE_CROWN_HEIGHT)
        self.freeze_image = load_and_scale_image(Settings.ASSETS_DIR + "/" +  "ice_freeze_player.png", PowerupsSettings.ICE_FREEZE_WIDTH, PowerupsSettings.ICE_FREEZE_HEIGHT)
        self._freeze_player = None
        self.ice_cube_image = load_and_scale_image(Settings.ASSETS_DIR + "/" + "ice_cube.png", PowerupsSettings.ICE_CUBE_WIDTH, PowerupsSettings.ICE_CUBE_HEIGHT)
        self.ice_cube_image.set_alpha(128)


    @property
    def freeze_player(self):
        return self._freeze_player
    

    @freeze_player.setter
    def freeze_player(self, ai):
        self._freeze_player = ai
        if ai != None:
            ai.freeze = True
    

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the power up.
        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        if self.active:
            # Draw the freeze power up on the owning player of this power up.
            screen.blit(self.active_player_powerup, (self.player.x - Settings.HEAD_RADIUS/2, PowerupsSettings.ICE_CROWN_Y))
            
            if self.freeze_player and self.freeze_player.freeze:
                # Draw the frozing player.
                screen.blit(self.freeze_image, (self.freeze_player.x - Settings.HEAD_RADIUS ,PowerupsSettings.ICE_FREEZE_Y))
                screen.blit(self.ice_cube_image, (self.freeze_player.x - Settings.HEAD_RADIUS , PowerupsSettings.ICE_CUBE_Y))
        else:
            # Draw the unpicked freeze powerup.
            screen.blit(self.powerup_image, pygame.Rect(self.x, self.y, self.width, self.height))


    def activate(self, player) -> None:
        """
        Activates the power up and set on the ability of user to freeze.
        Args:
            player (Player): The player to activate.
        """
        player.can_freeze = True
        super().activate(player)
    

    def deactivate(self) -> None:
        """
        Deactivates the power up and release the freezed player.
        """
        self.player.can_freeze = False
        if self.freeze_player != None:
            self.freeze_player.freeze = False
            self.freeze_player = None
        super().deactivate()

         
        
