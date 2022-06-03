
from utils.constants import Directions
from utils.types import SpeedTypes

class BaseBubble:
    """
    Base class to create a bubble.
    """
    def __init__(self, id: int) -> None:
        """
        Args:
            id (int): The id of the bubble.
        """
        self.id = id
    
    def move(self) -> None:
        """
        Moves the bubble in the current direction it's facing.
        """
        pass
