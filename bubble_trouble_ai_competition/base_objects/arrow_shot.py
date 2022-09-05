
import pygame
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.utils.constants import DisplayConstants, Events, Settings
from bubble_trouble_ai_competition.utils.general_utils import load_image_and_keep_aspect_ratio


class ArrowShot:
    """
    This class represents an arrow shot of a player.
    """
    def __init__(self, speed_y: int, shooting_player: BasePlayer, events_observable: EventsObservable) -> None:
        """
        Initializes the arrow shot.
        
        Args:
            speed_y (int): The speed of the arrow in the y direction.
            shooting_player (BasePlayer): The player that shot the arrow.
            events_observable (EventsObservable): The events observable.
        """
        self.x = shooting_player.x
        self.y = shooting_player.y
        self.width = Settings.ARROW_WIDTH
        self.height = 0
        self.speed_y = speed_y
        self.shooting_player = shooting_player
        self.events_observable = events_observable

        # Get the arrow image type (basic arrow or double points arrow).
        arrow_type = "/arrow.png" if not shooting_player.double_points else "/double_points_arrow.png" 
        self.arrow_image = load_image_and_keep_aspect_ratio(Settings.ASSETS_DIR + arrow_type, self.width)


    def update(self) -> None:
        """
        Updates the arrow's position, and checks if it has reached the ceiling.
        """
        self.y -= self.speed_y * Settings.FRAME_TIME
        if (self.y < DisplayConstants.CIELING_Y_VALUE):
            self.events_observable.notify_observers(Events.ARROW_OUT_OF_BOUNDS, self)


    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the arrow on the screen.
        """
        self.height = DisplayConstants.FLOOR_Y_VALUE - self.y
        screen.blit(self.arrow_image, (self.x, self.y), area=pygame.Rect(0, 0, self.width, self.height))

