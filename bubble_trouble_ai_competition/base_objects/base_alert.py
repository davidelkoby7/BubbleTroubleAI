
import pygame
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.utils.constants import Events, AlertConstans, Settings



class Alert:
    """
    This class represents an arrow shot of a player.
    """
    def __init__(self, msg: str, end_game: bool, events_observable: EventsObservable, freeze_time = Settings.FREEZE_TIME) -> None:
        """
        Initializes the Alert message.
        
        Args:
            msg (str): the message that will appear to screen as alert.
            events_observable (EventsObservable): The events observable.
            showed (bool): indicates if the alert already showed to the screen one
            freeze_time (int): the number of frames (seconds in fps units) to freeze game when alert is shown.
        """
        self.msg = msg
        self.end_game = end_game
        self.events_observable = events_observable
        self.freeze_time = freeze_time
        self.showed: bool = False
        
        
        # Defiene the text surface that alert will appear in
        self.text_surface = AlertConstans.ALERT_FONT.render(self.msg, False, AlertConstans.ALERT_COLOR)

        # initialize coordiantis according to text height and width
        self.x = AlertConstans.AlERT_POSITION[0] + self.text_surface.get_width()
        self.y = AlertConstans.AlERT_POSITION[1] + self.text_surface.get_height()

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
        screen.blit(self.text_surface, (self.x, self.y))

        self.showed = True
     

        
        