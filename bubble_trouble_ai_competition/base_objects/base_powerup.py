
import pygame
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.constants import DisplayConstants, PowerupsSettings, Settings
from bubble_trouble_ai_competition.utils.load_display import Images



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
        self.width = Settings.POWERUP_WIDTH
        self.height = Settings.POWERUP_HEIGHT
        self.gravity = 0
        self.player = None
        
        self.active = False
        self.has_active_timer = True
        self.active_timer = 0
        self.active_duration = 5 * 60
        
        self.pickable = True
        self.pickable_duration = 10 * 60
        self.pickable_timer = 0
        self.has_pickable_timer = True

        self.powerup_image_key = PowerupsSettings.DEFAULT_POWERUP


    def update(self) -> None:
        """
        Updates the power up state.
        Moves the powerup and handles the collision with the floor.
        Checks if the powerup is not picked up until the timer is up. If so, change its state to not pickable.
        If the powerup picked, check if the power up has an active timer.
        If so, updates the active_timer.
        If the active_timer reaches the active_duration, the power up is deactivated.
        """
        # move the poweup until it hits the floor
        if self.speed_y > 0:
            self.move()
            self.handle_floor_collision()
        
        if self.active and self.has_active_timer:
            self.active_timer += 1
            if self.active_timer >= self.active_duration:
                self.active = False
        
        if self.pickable and self.has_pickable_timer:
                self.pickable_timer += 1
                if self.pickable_timer >= self.pickable_duration:
                    self.pickable = False
        
        # If powerup picked up and the active_timer is over the active_duration, deactivate the powerup.
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
        player.active_powerups.append(self.powerup_image_key)
    

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
        if self.y + self.height > DisplayConstants.FLOOR_Y_VALUE:
            self.y = DisplayConstants.FLOOR_Y_VALUE - self.height
            self.speed_y = 0


    def draw(self, screen: pygame.Surface) -> None:
        # if powerup is not picked up, draw it.
        if self.player == None:
            screen.blit(Images.powerups_images[self.powerup_image_key], pygame.Rect(self.x, self.y, self.width, self.height))
