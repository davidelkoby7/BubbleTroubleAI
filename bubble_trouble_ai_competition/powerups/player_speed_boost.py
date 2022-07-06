from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.types import SpeedTypes

class PlayerSpeedBoostPowerup(Powerup):
    """
    Power up that increases the player's speed.
    """
    def __init__(self, x: int, y: int, width: int, height: int, powerup_value: int = 5):
        """
        Initializes the power up.
        
        Args:
            x (int): The x coordinate of the power up.
            y (int): The y coordinate of the power up.
            width (int): The width of the power up.
            height (int): The height of the power up.
            powerup_value (int): The value of the power up.
        """
        super().__init__(x, y, width, height)
        self.speed_boost = powerup_value
        self.speed_boost_timer = 0
        self.speed_boost_duration = 5 * 50
        self.speed_boost_active = False
        self.player = None
        
    def update(self) -> None:
        """
        Updates the power up state.
        Checks if the power up is active and if so, updates the timer.
        If the timer reaches the duration, the power up is deactivated.
        """
        if self.speed_boost_active:
            self.speed_boost_timer += 1
            if self.speed_boost_timer >= self.speed_boost_duration:
                self.speed_boost_active = False
                self.speed_boost_timer = 0
        else:
            self.speed_boost_timer = 0
        
        if self.player and not self.speed_boost_active:
            self.deactivate()
        
        super().update()
            
    def activate(self, player: BasePlayer) -> None:
        """
        Activates the power up.
        Change the player's speed to the power up's value.
        
    Args:
            player (Player): The player to activate.
        """
        self.speed_boost_active = True
        player.speed = SpeedTypes.FAST
        self.player = player  

    def deactivate(self) -> None:
        """
        Deactivates the power up.
        Change the player's speed back to normal.

    Args:
            player (Player): The player to deactivate.
        """
        self.speed_boost_active = False
        self.player.speed = SpeedTypes.NORMAL
