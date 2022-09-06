
import pygame
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.utils.constants import DisplayConstants, Events, Settings
from bubble_trouble_ai_competition.utils.load_images import get_arrow_image, Images


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
        self.color = shooting_player.arrow_color
        self.events_observable = events_observable


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
        arrow_image = get_arrow_image(self.color) if not self.shooting_player.double_points else Images.powerups_images["double_points_arrow"]
        screen.blit(arrow_image, (self.x, self.y), area=pygame.Rect(0, 0, self.width, self.height))
    

    def copy_object(self):
        attr_dict = dict(filter(lambda attr: not isinstance(attr[1], pygame.Surface), self.__dict__.items()))
        return type("ArrowShotData", (ArrowShot, ), attr_dict)

