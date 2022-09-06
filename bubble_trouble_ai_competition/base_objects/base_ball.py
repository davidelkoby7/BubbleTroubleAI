
import pygame
from bubble_trouble_ai_competition.utils.constants import BallColors, DisplayConstants, Settings
from bubble_trouble_ai_competition.utils.general_utils import circle_rect_collide, load_and_scale_image
from bubble_trouble_ai_competition.utils.load_images import get_ball_image 

class Ball:
    def __init__(self, x: int, y: int, speed_x: float, speed_y: float, size: int, color: BallColors, last_shot_by = None) -> None:
        """
        Initializes a ball object

        Args:
            x (int): The x coordinate of the ball.
            y (int): The y coordinate of the ball.
            speed_x (float): The horizontal speed of the ball.
            speed_y (float): The vertical speed of the ball.
            size (int): The size of the ball, in terms of how many times can this ball be split until it's completely popped.
            radius (int): The radius of the ball.
            color (BallColors): The color of the ball.
            gravity (float): The gravity which will affect the ball.
        """
        self.x = x + DisplayConstants.LEFT_BORDER_X_VALUE
        self.y = y + DisplayConstants.CIELING_Y_VALUE
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.size = size
        self.radius = self.size * Settings.BALL_SIZE_TO_RADIUS_RATIO
        self.color = color
        self.gravity = Settings.DEFAULT_GRAVITY
        self.last_shot_by = last_shot_by
    

    def get_raw_x(self) -> int:
        """
        Returns the raw x coordinate of the ball.

        Returns:
            int: The raw x coordinate of the ball.
        """
        return self.x - DisplayConstants.LEFT_BORDER_X_VALUE
    

    def get_raw_y(self) -> int:
        """
        Returns the raw y coordinate of the ball.

        Returns:
            int: The raw y coordinate of the ball.
        """
        return self.y - DisplayConstants.CIELING_Y_VALUE


    def update(self) -> None:
        """
        Updates the ball's position, speed, handles size etc.
        """
        self.move()
        self.handle_borders_collision()


    def move(self) -> None:
        """
        Moves the ball.
        """
        # Updating the vertical speed of the ball due to gravity
        self.speed_y += self.gravity * Settings.FRAME_TIME

        # Moving the ball
        self.x += self.speed_x * Settings.FRAME_TIME
        self.y += self.speed_y * Settings.FRAME_TIME


    def handle_borders_collision(self) -> None:
        """
        Handles the collision with the screen borders.
        If the ball has collided with the screen borders, it will reverse the speed.
        """
        if self.y - self.radius < DisplayConstants.CIELING_Y_VALUE: # Doesn't matter - if it touches the cieling the ball will be destroyed anyway
            pass
        elif self.y + self.radius > DisplayConstants.FLOOR_Y_VALUE:
            self.y = DisplayConstants.FLOOR_Y_VALUE - self.radius
            self.speed_y *= -1
        
        if self.x - self.radius < DisplayConstants.LEFT_BORDER_X_VALUE:
            self.x = DisplayConstants.LEFT_BORDER_X_VALUE + self.radius
            self.speed_x *= -1
        elif self.x + self.radius > DisplayConstants.RIGHT_BORDER_X_VALUE:
            self.x = DisplayConstants.RIGHT_BORDER_X_VALUE - self.radius
            self.speed_x *= -1


    def collides_with_shot(self, shot) -> bool:
        """
        Checks if the ball collides with a shot.

        Args:
            shot (ArrowShot): The shot to check if the ball collides with.

        Returns:
            bool: True if the ball collides with the shot, False otherwise.
        """
        # Check if the ball's center collides with the shot's center
        if (circle_rect_collide(shot.x, shot.y, shot.width, shot.height, self.x, self.y, self.radius)):
            return True

        # No collision - return False
        return False

    
    def collides_with_ceiling(self) -> bool:
        """
        Checks if the ball collides with the cieling.

        Returns:
            bool: True if the ball collides with the cieling, False otherwise.
        """
        if self.y - self.radius <= DisplayConstants.CIELING_Y_VALUE:
            return True
            
        return False
    

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(get_ball_image(self.color, self.size), (self.x - self.radius, self.y - self.radius))

    def copy_object(self):
        attr_dict = dict(filter(lambda attr: not isinstance(attr[1], pygame.Surface), self.__dict__.items()))
        return type("BallData", (Ball, ), attr_dict)