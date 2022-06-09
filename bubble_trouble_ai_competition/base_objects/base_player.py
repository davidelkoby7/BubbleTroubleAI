
from utils.constants import Directions
from utils.types import SpeedTypes


class BasePlayer:
    """
    Base class to create an AI playing the game.
    """
    def __init__(self, name: str, direction: Directions) -> None:
        """
        Args:
            name (str): The name of the player.
            direction (Directions): The direction the player is facing.
        """
        self.name = name
        self.direction = direction
        self.speed = SpeedTypes.NORMAL
    
    def move(self) -> None:
        """
        Moves the player in the current direction he's facing.
        """
        pass

    def talk(self) -> None:
        """
        Player will talk.
        """
        print (self.name)
