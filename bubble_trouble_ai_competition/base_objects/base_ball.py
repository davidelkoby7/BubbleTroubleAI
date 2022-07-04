
import pygame
from bubble_trouble_ai_competition.utils.constants import Settings
from bubble_trouble_ai_competition.utils.general_utils import circle_rect_collide


class Ball:
    def __init__(self, x: int, y: int, speed_x: float, speed_y: float, size: int, color: str, gravity: float = Settings.DEFAULT_GRAVITY) -> None:
        """
        Initializes a ball object

        Args:
            x (int): The x coordinate of the ball.
            y (int): The y coordinate of the ball.
            speed_x (float): The horizontal speed of the ball.
            speed_y (float): The vertical speed of the ball.
            size (int): The size of the ball, in terms of how many times can this ball be split until it's completely popped.
            radius (int): The radius of the ball.
            color (tuple): The color of the ball.
            gravity (float): The gravity which will affect the ball.
        """
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.size = size
        self.radius = self.size * Settings.BALL_SIZE_TO_RADIUS_RATIO
        self.color = color
        self.gravity = gravity
        self.last_shot_by = None
    

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
        if self.y - self.radius < 0:
            self.y = self.radius
            self.speed_y *= -1
        elif self.y + self.radius > Settings.SCREEN_HEIGHT:
            self.y = Settings.SCREEN_HEIGHT - self.radius
            self.speed_y *= -1
        
        if self.x - self.radius < 0:
            self.x = self.radius
            self.speed_x *= -1
        elif self.x + self.radius > Settings.SCREEN_WIDTH:
            self.x = Settings.SCREEN_WIDTH - self.radius
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
        if self.y - self.radius <= 0:
            return True
        return False
    

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

