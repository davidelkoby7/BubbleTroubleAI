import pygame
from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.game_core import game_state

from bubble_trouble_ai_competition.utils.constants import Directions, Events, ArrowColors
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.general_utils import get_closest_ball, get_closest_player, player_to_ball_distance

# The name of the class MUST be the name of the AI, with the filename, followed by 'AI'.
class exampleAI(BasePlayer):
    def __init__(self, events_observable: EventsObservable, ais_dir_path: str) -> None:
        """
        Constructs the example AI.
        """
        # The first parameter MUST be the name of the AI, as written in the filename.

        super().__init__("example", Directions.RIGHT, events_observable, ais_dir_path=ais_dir_path)
        self.arrow_color = ArrowColors.BLUE

    def pick_direction(self) -> Directions:
        """
        The main function where you decide what to do.
        In here - you MUST *return* a value of which direction to go.
        This can be one of the following:
        Directions.LEFT, Directions.RIGHT, Directions.STAND, Directions.DUCK
        In addition - you can call self.shoot() to shoot an arrow, and self.do_teleport() to teleport.
        Also - if you have the freeze powerup on you (can be checked with self.can_freeze), you can call self.do_freeze() to freeze an enemy.
        Another powerup is the punch powerup, which can be used with self.do_left_punch() and self.do_right_punch().
        Shooting and powerups can be used *in addition* to your movement - which is the return value.
        """
        # To get info about other things in the game - use the game_state file.
        closest_ball: Ball = get_closest_ball(self)
        if (player_to_ball_distance(self, closest_ball) < 300):
            self.shoot()

        ball_diff: int = closest_ball.x - self.x
        if (0 < ball_diff < 100 and self.shield == False and self.can_teleport == True):
            self.do_teleport()
        
        if (self.can_freeze):
            self.do_freeze()
        
        closest_player: BasePlayer = get_closest_player(self)
        if (closest_player != None):
            ai_diff: int = closest_player.x - self.x
            if (self.can_punch == True):
                if (0 < ai_diff < 100):
                    self.do_right_punch()
                if (0 > ai_diff > -100):
                    self.do_left_punch()
            
        if (ball_diff > 100 or (0 < ball_diff < 100 and self.shield == True)):
            return Directions.RIGHT
        if (ball_diff < -100 or (0 > ball_diff > -100 and self.shield == True)):
            return Directions.LEFT

        return Directions.DUCK

