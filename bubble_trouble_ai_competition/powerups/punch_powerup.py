from turtle import right
import pygame
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.utils.constants import PowerupsSettings, Settings
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image, load_image_and_keep_aspect_ratio


class PunchPowerup(Powerup):
    """
    Powerup that get the player the best smashing punch.
    """
    def __init__(self, x: int, y: int, speed_y: float, gravity: float = ...) -> None:
        """
        Initializes the power up.
        Args:
            x (int): The x coordinate of the power up.
            y (int): The y coordinate of the power up.
            speed_y (float): The vertical speed of the power up.
            gravity (float): The gravity which will affect the power up.
        """
        super().__init__(x, y, speed_y, gravity)
        self.punch_action = False
        self.collides = False
        self.powerup_image = pygame.transform.rotate(load_and_scale_image(Settings.ASSETS_DIR + "/" +  "punch_collision_powerup.png", self.width, self.height), 270)
        self.left_punch_collision_image = load_and_scale_image(Settings.ASSETS_DIR + "/" +  "punch_collision_powerup.png", PowerupsSettings.PUNCH_ACTION_WIDTH, PowerupsSettings.PUNCH_ACTION_HEIGHT)
        self.right_punch_collision_image = pygame.transform.flip(self.left_punch_collision_image, flip_x=True, flip_y=False)
        self.up_punch_collision_image = pygame.transform.rotate(self.left_punch_collision_image, 270)

        self.left_action_punch_image = load_and_scale_image(Settings.ASSETS_DIR + "/" +  "punch_powerup.png", PowerupsSettings.PUNCH_ACTION_WIDTH, PowerupsSettings.PUNCH_ACTION_HEIGHT)
        self.right_action_punch_image = pygame.transform.flip(self.left_action_punch_image, flip_x=True, flip_y=False)
        self.up_action_punch_image = pygame.transform.rotate(self.left_action_punch_image, 270)

        self.left_punch_image = load_and_scale_image(Settings.ASSETS_DIR + "/" +  "punch_powerup.png", PowerupsSettings.PUNCH_WIDTH, PowerupsSettings.PUNCH_HEIGHT*5)
        self.right_punch_image = pygame.transform.flip(self.left_punch_image, flip_x=True, flip_y=False)
        
        self.punch_image = self.powerup_image
        self.action_punch_coordinates = (0,0) # Initialize value
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the power up.
        Args:
            screen (pygame.Surface): The screen to draw on.
        
        #TODO: more record to code.
        """
        if self.collides:
            screen.blit(self.punch_image, self.action_punch_coordinates)
            self.collides = False

        elif self.punch_action and self.active:
            screen.blit(self.punch_image, self.action_punch_coordinates)
            self.punch_action = False

        elif self.active:
            

            screen.blit(self.left_punch_image, (self.player.get_player_left_hand_coordinates()[0], self.player.get_player_left_hand_coordinates()[1]))
            screen.blit(self.right_punch_image, (self.player.get_player_right_hand_coordinates()[0], self.player.get_player_right_hand_coordinates()[1]))
        else:
            screen.blit(self.powerup_image, pygame.Rect(self.x, self.y, self.width, self.height))

    def collides_left_punch(self):
        """
        """
        self.punch_image = self.left_punch_collision_image
        self.action_punch_coordinates = (self.player.get_player_left_hand_coordinates()[0] - self.player.width, self.player.get_player_left_hand_coordinates()[1])

    def collides_right_punch(self):
        """
        """
        self.punch_image = self.right_punch_collision_image
        self.action_punch_coordinates = (self.player.get_player_right_hand_coordinates()[0] - Settings.PLAYER_HANDS_SPACING*2, self.player.get_player_right_hand_coordinates()[1])

    def action_left_punch(self):
        """
        """
        self.punch_image = self.left_action_punch_image
        self.action_punch_coordinates = (self.player.get_player_left_hand_coordinates()[0] - self.player.width, self.player.get_player_left_hand_coordinates()[1])
        ...
    
    def action_right_punch(self):
        """
        """
        self.punch_image = self.right_action_punch_image
        self.action_punch_coordinates = (self.player.get_player_right_hand_coordinates()[0] - Settings.PLAYER_HANDS_SPACING*2, self.player.get_player_right_hand_coordinates()[1])
        ...
    def action_up_punch(self):
        """
        """
        self.punch_image = self.up_action_punch_image
        self.action_punch_coordinates = (0,0) #todo

    def activate(self, player) -> None:
        """
        Activates the power up.
        Change the player's shield to the power up's value.
        Args:
            player (Player): The player to activate.
        """
        player.punch = True
        super().activate(player)
    
    def deactivate(self) -> None:
        """
        Deactivates the power up.
        Change the player's shield to False.
        """
        self.player.punch = False
        super().deactivate()
    
    
