
import pygame
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.utils.constants import Events, CountdownBarConstants
from bubble_trouble_ai_competition.utils.load_display import DisplayObjects



class CountdownBar:
    """
    This class represent progress bar that count down the game frames remaining.
    """
    def __init__(self, game_frames: int, events_observable: EventsObservable) -> None:
        """
        Initializes the Countdown Bar.
        
        Args:
            game_frames (int): The amount of frames that the game left.
            events_observable (EventsObservable): The events observable.
        """
        self.frames_remaining = game_frames # farmes left to game.
        self.total_game_frames = game_frames # total of game frames during.
        self.x = CountdownBarConstants.BAR_POSITION[0]
        self.y = CountdownBarConstants.BAR_POSITION[1]

        self.events_observable = events_observable
        

    def update(self) -> None:
        """
        Update fram, and checks if it has reached the end.
        notify observers that time is out
        """
        self.frames_remaining -= 1
        if self.frames_remaining == 0:
            self.events_observable.notify_observers(Events.GAME_TIMEOUT)
    

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the bar loading on the screen.
        """

        # Drawing the background of the countdown bar.
        pygame.draw.rect(screen, CountdownBarConstants.BAR_COLOR, pygame.Rect(*CountdownBarConstants.BAR_POSITION, CountdownBarConstants.BAR_WIDTH,
                        CountdownBarConstants.BAR_HEIGHT))
        
        # Calculate the new width of the countdown bar (rect)
        update_countdown_rect_width = DisplayObjects.rect_countdown_image.get_width() * (self.frames_remaining / self.total_game_frames)
       
        # Update countdown bar
        screen.blit(
            DisplayObjects.rect_countdown_image,
            DisplayObjects.countdown_rect,
            (0, 0, update_countdown_rect_width, DisplayObjects.countdown_rect.h)
            )
        
     

        
        