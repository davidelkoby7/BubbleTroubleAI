import pygame
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.utils.constants import Settings, PowerupsSettings
from bubble_trouble_ai_competition.utils.general_utils import flip_x_image
from bubble_trouble_ai_competition.utils.load_display import Images

class PunchPowerup(Powerup):
    """
    Powerup that get the player the best smashing punch.
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
        self.action_left_punch = False 
        self.action_right_punch = False
        self.collides_right_punch = False
        self.collides_left_punch = False 

    def get_right_punch_action_coordinates(self):
        return (self.player.get_player_right_hand_coordinates()[0] - Settings.PLAYER_HANDS_SPACING, self.player.get_player_right_hand_coordinates()[1])

    def get_left_punch_action_coordinates(self):
        return (self.player.get_player_left_hand_coordinates()[0] - self.player.width, self.player.get_player_left_hand_coordinates()[1])

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the punch power up.
        Args:
            screen (pygame.Surface): The screen to draw on.
        
        """

        if self.collides_right_punch == True:
            # Draw the right punch collision.
            screen.blit(flip_x_image(Images.powerups_images[PowerupsSettings.LEFT_COLLISION_PUNCH]), self.get_right_punch_action_coordinates())
            self.collides_right_punch = False
            self.action_right_punch = False
            self.player.punch_right = False

        elif self.collides_left_punch == True:
            # Draw the left punch collision.
            screen.blit(Images.powerups_images[PowerupsSettings.LEFT_COLLISION_PUNCH], self.get_left_punch_action_coordinates())
            self.collides_left_punch = False
            self.action_left_punch = False
            self.player.punch_left = False

        elif self.action_left_punch == True and self.active == True:
            # Draw the left punch action (without a collision).
            screen.blit(Images.powerups_images[PowerupsSettings.LEFT_ACTION_PUNCH], self.get_left_punch_action_coordinates())
            self.action_left_punch = False
            self.player.punch_left = False
        
        elif self.action_right_punch == True and self.active == True:
            # Draw the right punch action (without a collision).
            screen.blit(flip_x_image(Images.powerups_images[PowerupsSettings.LEFT_ACTION_PUNCH]), self.get_right_punch_action_coordinates())
            self.action_right_punch = False
            self.player.punch_right = False

        elif self.active:
            # Draw the punch powerup abillity of player (without punch action).
            screen.blit(Images.powerups_images[PowerupsSettings.ACTIVE_LEFT_PUNCH], self.player.get_player_left_hand_coordinates())
            screen.blit(flip_x_image(Images.powerups_images[PowerupsSettings.ACTIVE_LEFT_PUNCH]), self.player.get_player_right_hand_coordinates())

        super().draw(screen, Images.powerups_images[PowerupsSettings.PUNCH_POWERUP])


    def activate(self, player) -> None:
        """
        Activates the power up.
        Change the player's shield to the power up's value.
        Args:
            player (Player): The player to activate.
        """
        player.punch_powerup = True
        player.punch = True
        super().activate(player)
    
    def deactivate(self) -> None:
        """
        Deactivates the power up.
        Change the player's shield to False.
        """
        self.player.punch = False
        super().deactivate()
        