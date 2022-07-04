import random
import pygame

from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable

from bubble_trouble_ai_competition.utils.constants import Directions, Events, Settings
from bubble_trouble_ai_competition.utils.general_utils import circles_collide, circle_rect_collide, rect_collide
from bubble_trouble_ai_competition.utils.types import SpeedTypes

class BasePlayer:
    """
    Base class to create an AI playing the game.
    """

    def __init__(self, name: str, direction: Directions, events_observable: EventsObservable, position: tuple = (20, 0), dimensions: tuple = Settings.PLAYER_DIMENSIONS, head_radius: int = Settings.HEAD_RADIUS, screen_size: tuple = Settings.SCREEN_SIZE) -> None:
        """
        Args:
            name (str): The name of the player.
            direction (Directions): The direction the player is facing.
        """
        self.name = name
        self.direction = direction
        self.position = position
        self.screen_size = screen_size
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.x = position[0]
        self.y = self.screen_size[1] - position[1] - self.height
        self.dimensions = dimensions
        self.head_radius = head_radius
        self.update_head_center()
        self.color = (255, 0, 0)
        self.speed = SpeedTypes.NORMAL
        self.events_observable = events_observable
        self.is_shooting = False


    def update(self) -> None:
        """
        Updates the player's attributes.
        """

        self.update_head_center()
        self.direction = self.pick_direction()
        self.move()

    
    def pick_direction(self) -> Directions:
        """
        Function to be implemented by the inheriting class of each ai.
        """
        return random.choice([Directions.LEFT, Directions.RIGHT])


    def shoot(self):
        """
        Player will shoot.
        """
        if (self.is_shooting == False):
            self.is_shooting = True
            self.events_observable.notify_observers(Events.PLAYER_SHOT, self)
            self.shooting_delay = Settings.SHOOTING_DELAY
    

    def move(self) -> None:
        """
        Moves the player.
        """

        self.x += self.direction * Settings.FRAME_TIME * Settings.PLAYER_SPEED

        # Making sure the AI is not going out of bounds.
        if (self.x < 0):
            self.x = 0
        if (self.x > Settings.SCREEN_WIDTH - self.width):
            self.x = Settings.SCREEN_WIDTH - self.width
    
    
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
        # Check if the player's head collides with the ball
        if (circles_collide(self.head_center, self.head_radius, (ball.x, ball.y), ball.radius)):
            return True
        
        # Check if the player's body collides with the ball
        if (circle_rect_collide(self.x, self.y, self.width, self.height, ball.x, ball.y, ball.radius)):
            return True
        
        # No collision - return False
        return False


    def collides_with_powerup(self, powerup: Powerup) -> bool:
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
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

        # Drawing head
        pygame.draw.circle(screen, self.color, (int(self.head_center[0]), int(self.head_center[1])), self.head_radius)


    def can_shoot(self) -> bool:
        """
        Checks if the player can shoot.

        Returns:
            bool: True if the player can shoot, False otherwise.
        """
        return self.is_shooting == False

