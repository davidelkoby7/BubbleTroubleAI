import pygame
from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.game_core import game_state
from bubble_trouble_ai_competition.utils.constants import DisplayConstants
from bubble_trouble_ai_competition.utils.constants import Directions, DisplayConstants, Events
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.general_utils import get_closest_ball, get_closest_player, player_to_ball_distance

# The name of the class MUST be the name of the AI, with the filename, followed by 'AI'.
class bot_yagelAI(BasePlayer):
    def __init__(self, events_observable: EventsObservable, ais_dir_path: str) -> None:
        """
        Constructs the example AI.
        """
        # The first parameter MUST be the name of the AI, as written in the filename.
        super().__init__("bot_yagel", Directions.RIGHT, events_observable, ais_dir_path=ais_dir_path)


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
        bubble_exist = True
        # while(bubble_exist):

        #     closest_ball.update()
        #     if()
        all_balls = game_state.game_balls()
        for ball in all_balls:
            if((ball.x >= self.x and (ball.x - (self.width*6)) <= self.x)or (ball.x <= self.x and (ball.x +(self.width*6)) >= self.x)):
            # if (ball.x -10 < self.x or ball.x -10  > self.x):
                self.shoot()
            # print(ball)



        # if (player_to_ball_distance(self, closest_ball) < 300):
        #     self.shoot()

        ball_diff: int = closest_ball.x - self.x
        if (0 < ball_diff < 10 and self.shield == False and self.can_teleport == True):
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
        DisplayConstants1: DisplayConstants
        while(bubble_exist):
            closest_ball.update()
            ball_diff1: int = closest_ball.x - self.x
            if(closest_ball.y + closest_ball.radius >= 535):
                if(closest_ball.x > self.x):
                    # self.shoot()
                    bubble_exist = False
                    if(ball_diff < 100):
                        return Directions.LEFT
                    else:
                        return Directions.RIGHT
                if(closest_ball.x < self.x):
                    # self.shoot()
                    bubble_exist = False
                    if(ball_diff1 > -100):
                        return Directions.RIGHT
                    else:
                        return Directions.LEFT
                
            # bubble_exist = False


            #     return Directions.RIGHT
            # if(player_to_ball_distance(self, closest_ball) < 30):
                
            
        # if (ball_diff > 100 or (0 < ball_diff < 100 and self.shield == True)):
        #     return Directions.RIGHT
        # if (ball_diff < -100 or (0 > ball_diff > -100 and self.shield == True)):
        #     return Directions.LEFT

        return Directions.DUCK