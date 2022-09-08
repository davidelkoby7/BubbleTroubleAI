
import pygame
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.utils.constants import Events, AlertConstants, Settings
from bubble_trouble_ai_competition.utils.load_display import DisplayObjects


class Alert:
    """
    This class represents an Alert message the appears to screen.
    """
    def __init__(self, alert_type: str, end_game: bool, events_observable: EventsObservable, frames_freeze = Settings.FRAMES_FREEZE) -> None:
        """
        Initializes the Alert message.
        
        Args:
            alert_type (str): the alert message that will appear to screen as alert, must be alert_<alert_type>_key from AlertConstants.
            events_observable (EventsObservable): The events observable.
            showed (bool): indicates if the alert already showed to the screen one
            frames_freeze (int): the number of frames to freeze when alert is shown.
        """
        self.alert_type: str = alert_type
        self.end_game: bool = end_game
        self.events_observable: EventsObservable = events_observable
        self.frames_freeze: int = frames_freeze
        self.showed: bool = False

        # initialize coordiantis according to text height and width
        self.x = AlertConstants.AlERT_POSITION[0] + DisplayObjects.alerts[self.alert_type].get_width()
        self.y = AlertConstants.AlERT_POSITION[1] + DisplayObjects.alerts[self.alert_type].get_height()

    def update(self) -> None:
        """
        Update the game if the alert already drawed to screen.
        notify observers that alert is showed.
        """
        if self.showed:
     
            self.events_observable.notify_observers(Events.SHOWED_ALERT, self)
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the bar loading on the screen.
        """

        # Writing the alert message
        screen.blit(DisplayObjects.alerts[self.alert_type], (self.x, self.y))
        self.showed = True
        