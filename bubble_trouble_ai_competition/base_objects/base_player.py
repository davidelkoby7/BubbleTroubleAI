import random
import pygame

from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable

from bubble_trouble_ai_competition.utils.constants import Directions, DisplayConstants, Events, Settings
from bubble_trouble_ai_competition.utils.general_utils import circles_collide, circle_rect_collide, rect_collide, load_and_scale_image
from bubble_trouble_ai_competition.utils.types import SpeedTypes

class BasePlayer:
    """
    Base class to create an AI playing the game.
    """

    def __init__(self, name: str, direction: Directions, events_observable: EventsObservable,
                 position: tuple = (1000, 0), ais_dir_path = None) -> None:
        """
        Args:
            name (str): The name of the player.
            direction (Directions): The direction the player is facing.
        """
        self.name = name
        self.direction = direction
        self.position = position
        self.width = Settings.PLAYER_DIMENSIONS[0]
        self._height = Settings.PLAYER_DIMENSIONS[1] # player's height changes during game
        self.x = position[0] + DisplayConstants.LEFT_BORDER_X_VALUE
        self.y = DisplayConstants.FLOOR_Y_VALUE - position[1] - self.height # player's height changes during game 
        self.head_radius = Settings.HEAD_RADIUS
        self.dimensions = Settings.PLAYER_DIMENSIONS
        self.update_head_center()
        self.color = (255, 0, 0)
        self.speed = SpeedTypes.NORMAL
        self.events_observable = events_observable
        self.is_shooting = False
        self.head_image = load_and_scale_image(ais_dir_path + "/" + name + "_images//head.png", self.head_radius * 2, self.head_radius * 2)
        self.head_right_image = load_and_scale_image(ais_dir_path + "/" + name + "_images//head_right.png", self.head_radius * 2, self.head_radius * 2)
        self.head_left_image = load_and_scale_image(ais_dir_path + "/" + name + "_images//head_left.png", self.head_radius * 2, self.head_radius * 2)
        self.duck_body_image = load_and_scale_image(ais_dir_path + "/" + name + "_images//body.png", self.width, Settings.PLAYER_DUCK_HEIGHT)
        self.stand_body_image = load_and_scale_image(ais_dir_path + "/" + name + "_images//body.png", self.width, self.height)
        self.body_image = self.stand_body_image
        self.body_image_rect = self.body_image.get_rect()
        self.shield = False
        self.punch = False
        self.score = 0

    @property
    def height(self):
        """
        Player's height
        """
        return self._height

    @height.setter
    def height(self, new_height):
        """
        Set new height for player and update  player y coordiantes.
        """
        self._height = new_height
        self.y = DisplayConstants.FLOOR_Y_VALUE - self.position[1] - self.height

    def update(self) -> None:
        """
        Updates the player's attributes.
        """

        self.direction = self.pick_direction()

        if self.direction == Directions.DUCK:
            self.duck()
        else:
            self.stand()
            self.move()
        self.update_head_center()

    def duck(self):
        """Player will duck."""

        #  update player's new height and body image
        self.height = Settings.PLAYER_DUCK_HEIGHT
        self.body_image = self.duck_body_image
    
    def stand(self):
        """Player will stand."""

        #  update player's new height and body image
        self.height = Settings.PLAYER_DIMENSIONS[1]
        self.body_image = self.stand_body_image

    def pick_direction(self) -> Directions:
        """
        Function to be implemented by the inheriting class of each ai.
        """
        return random.choice([Directions.LEFT, Directions.RIGHT])

    def right_punch(self):
        """
        Player will punch with his right punch.
        """
        if (self.punch == True):
            
            self.events_observable.notify_observers(Events.PLAYER_RPUNCH, self)
        ...
    def left_punch(self):
        """
        Player will punch with his left punch.
        """
        if (self.punch == True):
            
            self.events_observable.notify_observers(Events.PLAYER_LPUNCH, self)
        ...
    
    def up_punch(self):
        """
        Player will punch with his up punch.
        """
        if (self.punch == True):
            
            self.events_observable.notify_observers(Events.PLAYER_UPUNCH, self)
        ...
    def shoot(self):
        """
        Player will shoot.
        """
        if (self.is_shooting == False):
            self.is_shooting = True
            self.events_observable.notify_observers(Events.PLAYER_SHOT, self)
    

    def move(self) -> None:
        """
        Moves the player.
        """

        self.x += self.direction * Settings.FRAME_TIME * self.speed

        # Making sure the AI is not going out of bounds.
        if (self.x < DisplayConstants.LEFT_BORDER_X_VALUE):
            self.x = DisplayConstants.LEFT_BORDER_X_VALUE
        if (self.x > DisplayConstants.RIGHT_BORDER_X_VALUE - self.width):
            self.x = DisplayConstants.RIGHT_BORDER_X_VALUE - self.width

    
    def talk(self) -> None:
        """
        Player will talk.
        """
        print (self.name)
    

    def update_head_center(self) -> None:
        """
        Updates the head center of the player.
        """
        self.head_center = ((self.x + (self.x + self.width)) / 2, self.y - self.head_radius)


    def collides_with_ball(self, ball: Ball) -> bool:
        """
        Checks if the player collides with a ball.

        Args:
            ball (Ball): The ball to check if the player collides with.
        
        Returns:
            bool: True if the player collides with the ball, False otherwise.
        """
        # Check if the player has shield
        if (self.shield):
            return False

        # Check if the player's head collides with the ball
        if (circles_collide(self.head_center, self.head_radius, (ball.x, ball.y), ball.radius)):
            return True
        
        # Check if the player's body collides with the ball
        if (circle_rect_collide(self.x, self.y, self.width, self.height, ball.x, ball.y, ball.radius)):
            return True
        
        # No collision - return False
        return False


    def collides_with_powerup(self, powerup) -> bool:
        """
        Checks if the player collides with a power up.

        Args:
            powerup (Powerup): The power up to check if the player collides with.
        
        Returns:
            bool: True if the player collides with the power up, False otherwise.
        """
        # Check if the player's head collides with the powerup
        if (circle_rect_collide(powerup.x, powerup.y, powerup.width, powerup.height, self.head_center[0], self.head_center[1], self.head_radius)):
            return True

        # Check if the player's body collides with the powerup
        if rect_collide(self.x, self.y, self.width, self.height, powerup.x, powerup.y, powerup.width, powerup.height):
            return True      
 
        # No collision - return False
        return False
  

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the player on the screen.

        Args:
            screen (pygame.Surface): The screen to draw the player on.
        """

        # Drawing body
        screen.blit(self.body_image, (self.x, self.y))

        # Drawing head
        head_image_draw_position = (self.head_center[0] - self.head_radius, self.head_center[1] - self.head_radius)

        if (self.direction == Directions.STAND or self.direction == Directions.DUCK):
            screen.blit(self.head_image, head_image_draw_position)
        elif (self.direction == Directions.LEFT):
            screen.blit(self.head_left_image, head_image_draw_position)
        elif (self.direction == Directions.RIGHT):
            screen.blit(self.head_right_image, head_image_draw_position)

    def can_shoot(self) -> bool:
        """
        Checks if the player can shoot.

        Returns:
            bool: True if the player can shoot, False otherwise.
        """
        return self.is_shooting == False

    def can_punch(self) -> bool:
        """
        Checks if the player can punch
        """
        return self.punch

    def get_player_top_right_corner(self) -> tuple:
        """
        Returns the top right corner of the player.

        Returns:
            tuple: The top right corner of the player.
        """
        return (self.x + self.width, self.y - self.head_radius*2)


    def get_player_top_left_corner(self) -> tuple:
        """
        Returns the top left corner of the player.

        Returns:
            tuple: The top left corner of the player.
        """
        return (self.x, self.y - self.head_radius*2)


    def get_score(self) -> int:
        """
        Returns the player's score.

        Returns:
            int: The player's score.
        """
        return self.score