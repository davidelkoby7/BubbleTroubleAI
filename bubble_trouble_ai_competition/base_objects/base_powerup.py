
from turtle import width
import pygame
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.constants import Settings
from bubble_trouble_ai_competition.utils.general_utils import circle_rect_collide
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image



class Powerup:
    def __init__(self, x: int, y: int, speed_y: float, gravity: float = Settings.DEFAULT_GRAVITY) -> None:
        """
        Initializes a powerup object
        Args:
            x (int): The x coordinate of the ball.
            y (int): The y coordinate of the ball.
            speed_y (float): The vertical speed of the ball.
            color (tuple): The color of the ball.
            gravity (float): The gravity which will affect the ball.
        """
        self.x = x
        self.y = y
        self.speed_y = speed_y
        self.width = 50
        self.height = 50
        self.gravity = 0
        self.powerup_image = load_and_scale_image(Settings.ASSETS_DIR + "/" +  "powerup.png", self.width, self.height)
        self.active = False
        self.timer = 0
        self.duration = 5 * 60
        self.player = None


    def update(self) -> None:
        """
        Updates the power up state.
        Checks if the power up is active and if so, updates the timer.
        If the timer reaches the duration, the power up is deactivated.
        """
        if self.active:
            self.timer += 1
            if self.timer >= self.duration:
                self.active = False
                self.timer = 0
        else:
            self.move()
            self.handle_floor_collision()
            self.timer = 0
        
        # If powerup picked up and the timer is over the duration, deactivate the powerup.
        if self.player and not self.active:
            self.deactivate()


    def move(self) -> None:
        """
        Moves the powerup.
        """
        # Updating the vertical speed of the powerup due to gravity
        self.speed_y += self.gravity * Settings.FRAME_TIME

        # Moving the powerup
        self.y += self.speed_y * Settings.FRAME_TIME


    def activate(self, player: BasePlayer) -> None:
        """
        Activates the powerup.
        """
        self.active = True
        self.player = player
    
    def deactivate(self) -> None:
        """
        Deactivates the powerup.
        """
        self.active = False


    def handle_floor_collision(self) -> None:
        """
        Handles the collision with the floor.
        If the powerup has collided with the floor, it will stop.
        """
        if self.y + self.height > Settings.SCREEN_HEIGHT:
            self.y = Settings.SCREEN_HEIGHT - self.height
            self.speed_y = 0


    def draw(self, screen: pygame.Surface) -> None:
        # if powerup is not picked up, draw it.
        if self.player == None:
            screen.blit(self.powerup_image, pygame.Rect(self.x, self.y, self.width, self.height))
