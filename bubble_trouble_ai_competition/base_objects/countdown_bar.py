
import pygame
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.utils.constants import Events, CountdownBarConstans



class CountdownBar:
    """
    This class represents an arrow shot of a player.
    """
    def __init__(self, countdown: int, events_observable: EventsObservable) -> None:
        """
        Initializes the Countdown Bar.
        
        Args:
            countdown (int): The amount of time (in fps units) that the game left.
            events_observable (EventsObservable): The events observable.
        """
        self.countdown = countdown
        self.fps = countdown
        self.x = CountdownBarConstans.BAR_POSITION[0]
        self.y = CountdownBarConstans.BAR_POSITION[1]

        self.events_observable = events_observable

        # Define the rect inside the progress bar
        self.rect_image = pygame.Surface((CountdownBarConstans.BAR_WIDTH,
                        CountdownBarConstans.BAR_HEIGHT)) 
        
        self.rect_image.fill(CountdownBarConstans.LOADING_COLOR)
        self.countdown_rect = self.rect_image.get_rect(topleft=(self.x, self.y)) 
        
       

    def update(self) -> None:
        """
        Update countdown, and checks if it has reached the end.
        notify observers that time is out
        """
        self.countdown -= 1
        if self.countdown == 0:
            self.events_observable.notify_observers(Events.GAME_TIMEOUT)
    


    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the bar loading on the screen.
        """
        # Drawing the background of the countdown bar.
        pygame.draw.rect(screen, CountdownBarConstans.BAR_COLOR, pygame.Rect(*CountdownBarConstans.BAR_POSITION, CountdownBarConstans.BAR_WIDTH,
                        CountdownBarConstans.BAR_HEIGHT))
        
        # Calculate the new width of the countdown bar (rect)
        update_countdown_rect_width = self.countdown_rect.w * (self.countdown / self.fps)
       
        # Update countdown bar
        screen.blit(
            self.rect_image,
            self.countdown_rect,
            (0, 0, update_countdown_rect_width, self.countdown_rect.h)
            )
        
     

        
        