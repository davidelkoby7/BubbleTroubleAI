
from bubble_trouble_ai_competition.utils.constants import Settings


class Ball:
    def __init__(self, x: int, y: int, speed_x: float, speed_y: float, radius: int, color: tuple, gravity: float = Settings.DEFAULT_GRAVITY) -> None:
        """
        Initializes a ball object

        Args:
            x (int): The x coordinate of the ball.
            y (int): The y coordinate of the ball.
            speed_x (float): The horizontal speed of the ball.
            speed_y (float): The vertical speed of the ball.
            radius (int): The radius of the ball.
            color (tuple): The color of the ball.
            gravity (float): The gravity which will affect the ball.
        """
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius
        self.color = color
        self.gravity = gravity
    

    def update(self) -> None:
        """
        Updates the ball's position.
        """
        # Updating the vertical speed of the ball due to gravity
        self.speed_y += self.gravity * Settings.FRAME_TIME

        # Moving the ball
        self.x += self.speed_x * Settings.FRAME_TIME
        self.y += self.speed_y * Settings.FRAME_TIME

        # Check for collision with the screen
        if self.y < 0:
            self.y = 0
            self.speed_y *= -1
        elif self.y > Settings.SCREEN_HEIGHT:
            self.y = Settings.SCREEN_HEIGHT
            self.speed_y *= -1
        
        if self.x < 0:
            self.x = 0
            self.speed_x *= -1
        elif self.x > Settings.SCREEN_WIDTH:
            self.x = Settings.SCREEN_WIDTH
            self.speed_x *= -1

