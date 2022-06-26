import pygame
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable

from bubble_trouble_ai_competition.utils.constants import Directions, Events
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer

class manualAI(BasePlayer):
    def __init__(self, events_observable: EventsObservable, screen_size: tuple) -> None:
        """
        Constructs the manual AI.
        """
        super().__init__("manual", Directions.RIGHT, events_observable, screen_size=screen_size)

        # self.events_observable.add_observer(Events.BALL_POPPED,
        #     lambda ball_id, ball_name:
        #         print (f"On Ball Popped! {ball_id=}, {ball_name=}")
        # )

    
    def pick_direction(self) -> Directions:
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            self.shoot()

        if keys[pygame.K_LEFT]:
            return Directions.LEFT
        
        if keys[pygame.K_RIGHT]:
            return Directions.RIGHT
        
        return Directions.STAND

    
    def on_ball_popped(self, ball_id: int, ball_name: str = "None") -> None:
        print (f"On Ball Popped! {ball_id=}, {ball_name=}")

