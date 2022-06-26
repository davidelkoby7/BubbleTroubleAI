
import pygame
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.utils.constants import Events, Settings


class ArrowShot:
    """
    This class represents an arrow shot of a player.
    """
    def __init__(self, x: int, y: int, speed_y: int, shooting_player: BasePlayer, events_observable: EventsObservable ,width: int = Settings.ARROW_WIDTH) -> None:
        """
        Initializes the arrow shot.
        
        Args:
            x (int): The x coordinate of the arrow.
            y (int): The y coordinate of the arrow.
            speed_y (int): The speed of the arrow in the y direction.
            shooting_player (BasePlayer): The player that shot the arrow.
            events_observable (EventsObservable): The events observable.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = 0
        self.speed_y = speed_y
        self.shooting_player = shooting_player
        self.events_observable = events_observable


    def update(self) -> None:
        self.y -= self.speed_y * Settings.FRAME_TIME
        if (self.y < 0):
            self.events_observable.notify_observers(Events.ARROW_OUT_OF_BOUNDS, self)


    def draw(self, screen) -> None:
        self.height = screen.get_height() - self.y
        pygame.draw.rect(screen, (30, 60, 90), pygame.Rect(self.x, self.y, self.width, self.height))

