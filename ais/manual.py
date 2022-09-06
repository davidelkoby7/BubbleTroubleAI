import pygame
import random
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.powerups.freeze_powerup import FreezePowerup

from bubble_trouble_ai_competition.utils.constants import Directions, Events
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer

class manualAI(BasePlayer):
    def __init__(self, events_observable: EventsObservable, ais_dir_path: str) -> None:
        """
        Constructs the manual AI.
        """
        super().__init__("manual", Directions.RIGHT, events_observable, ais_dir_path=ais_dir_path)

        # self.events_observable.add_observer(Events.BALL_POPPED,
        #     lambda ball_id, ball_name:
        #         print (f"On Ball Popped! {ball_id=}, {ball_name=}")
        # )

    def pick_player_to_freeze(self) -> BasePlayer:
       
        other_ais = [ai for ai in self.game_state['ais'] if ai.name != self.name]
        # Check that there are still others ais in game.
        if other_ais != []:
            ai = random.choice(other_ais) 
            return ai.name
        else:
            return None

    def pick_direction(self) -> Directions:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            self.do_freeze()

        if keys[pygame.K_DOWN]:
            return Directions.DUCK
        
        if keys[pygame.K_LCTRL]:
            self.do_left_punch()
        
        if keys[pygame.K_RCTRL]:
            self.do_right_punch()
            
        if keys[pygame.K_SPACE]:
            self.shoot()

        if keys[pygame.K_LEFT]:
            return Directions.LEFT
        
        if keys[pygame.K_RIGHT]:
            return Directions.RIGHT
        
        return Directions.STAND

    
    def on_ball_popped(self, ball_id: int, ball_name: str = "None") -> None:
        print (f"On Ball Popped! {ball_id=}, {ball_name=}")

