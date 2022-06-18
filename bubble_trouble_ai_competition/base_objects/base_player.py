import random
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable

from bubble_trouble_ai_competition.utils.constants import Directions, Settings
from bubble_trouble_ai_competition.utils.types import SpeedTypes

class BasePlayer:
    """
    Base class to create an AI playing the game.
    """

    def __init__(self, name: str, direction: Directions, events_observable: EventsObservable, position: tuple = (20, 0), dimensions: tuple = Settings.PLAYER_DIMENSIONS) -> None:
        """
        Args:
            name (str): The name of the player.
            direction (Directions): The direction the player is facing.
        """
        self.name = name
        self.direction = direction
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.dimensions = dimensions
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.color = (255, 0, 0)
        self.speed = SpeedTypes.NORMAL
        self.events_observable = events_observable


    def update(self) -> None:
        """
        Updates the player's attributes.
        """

        self.direction = self.pick_direction()

    
    def pick_direction(self) -> Directions:
        """
        Function to be implemented by the inheriting class of each ai.
        """
        return random.choice([Directions.LEFT, Directions.RIGHT])

    
    def talk(self) -> None:
        """
        Player will talk.
        """
        print (self.name)
    