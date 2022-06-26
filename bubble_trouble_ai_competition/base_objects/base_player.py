import random
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable

from bubble_trouble_ai_competition.utils.constants import Directions, Settings
from bubble_trouble_ai_competition.utils.types import SpeedTypes

class BasePlayer:
    """
    Base class to create an AI playing the game.
    """

    def __init__(self, name: str, direction: Directions, events_observable: EventsObservable, position: tuple = (20, 0), dimensions: tuple = Settings.PLAYER_DIMENSIONS, head_radius = Settings.HEAD_RADIUS, screen_size: tuple = Settings.SCREEN_SIZE) -> None:
        """
        Args:
            name (str): The name of the player.
            direction (Directions): The direction the player is facing.
        """
        self.name = name
        self.direction = direction
        self.position = position
        self.screen_size = screen_size
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.x = position[0]
        self.y = self.screen_size[1] - position[1] - self.height
        self.dimensions = dimensions
        self.head_radius = head_radius
        self.update_head_center()
        self.color = (255, 0, 0)
        self.speed = SpeedTypes.NORMAL
        self.events_observable = events_observable


    def update(self) -> None:
        """
        Updates the player's attributes.
        """

        self.update_head_center()
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
    

    def update_head_center(self) -> None:
        """
        Updates the head center of the player.
        """
        self.head_center = ((self.x + (self.x + self.width)) / 2, self.y - self.head_radius)

