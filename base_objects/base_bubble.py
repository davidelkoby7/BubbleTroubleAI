
from utils.constants import Directions
from utils.types import SpeedTypes

class BaseBubble:
    """
    Base class to create a bubble.
    """
    def __init__(self, name: str, direction: Directions, speed: SpeedTypes) -> None:
        """
        Constructs a base bubble.
        
        :param name: str: abc
        """
        self.name = name
        self.direction = direction
        self.speed = speed
    
    def move(self) -> None:
        """
        Moves the bubble in the current direction he's facing.
        """
        pass
