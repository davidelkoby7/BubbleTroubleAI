from asyncio import constants
from csv import DictWriter
from fileinput import close
from pkgutil import extend_path
import re
from sys import get_coroutine_origin_tracking_depth
from typing import get_origin
import pygame
from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.game_core import game_state
import time 
from bubble_trouble_ai_competition.utils.constants import Directions, Events , DisplayConstants
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.general_utils import get_closest_ball, get_closest_player, player_to_ball_distance

# The name of the class MUST be the name of the AI, with the filename, followed by 'AI'.
class therebelsAI(BasePlayer):
    def __init__(self, events_observable: EventsObservable, ais_dir_path: str) -> None:
        """
        Constructs the example AI.
        """
        # The first parameter MUST be the name of the AI, as written in the filename.
        super().__init__("therebels", Directions.RIGHT, events_observable, ais_dir_path=ais_dir_path)
        self.going_right = True 


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
        #for initial run only 
        try:
            getattr(self, 'going_right')
        except: 
            self.going_right = True

            # self.going_right.__getattribute__
        # To get info about other things in the game - use the game_state file.
        closest_ball: Ball = get_closest_ball(self)
        
        #print (self.x)
        # if self.x == 30:

            
        dangrous_but_allowed_in_case_of_real_emergency = [Directions.DUCK, Directions.LEFT, Directions.RIGHT]
        allowed = [ Directions.RIGHT,Directions.LEFT]
        
        recommended_moves = []
        try: 
            #Recommendations 
            safe_zone = (DisplayConstants.RIGHT_BORDER_X_VALUE-self.most_extreme_right()) /2
            #Recommend player to go back and forth 
            if self.x <  DisplayConstants.RIGHT_BORDER_X_VALUE - self.width - safe_zone or DisplayConstants.RIGHT_BORDER_X_VALUE - self.width - 100 == self.x :
                self.going_right = True
                #self.shoot()
            if self.x == DisplayConstants.RIGHT_BORDER_X_VALUE - self.width:
                self.going_right = False
                # if self.is_ball_in_range(DisplayConstants.RIGHT_BORDER_X_VALUE - self.width - 300, DisplayConstants.RIGHT_BORDER_X_VALUE - self.width):
                #     recommended_moves.append(Directions.DUCK)
                #     return Directions.DUCK
            
            #Not-Allowing stuff 
            #Don't allow player to go in the direction of the closest ball
            if player_to_ball_distance(self, closest_ball) < 200:

                if self.if_ball_to_right(closest_ball):
                    allowed.remove(Directions.RIGHT)
                else: 
                    allowed.remove(Directions.LEFT)
        
        
            if self.is_ball_in_range(self.x -60, self.x + 60, and_low = True ):
                self.shoot()
                pass 

            #a move which will kill us in the next 100 frames will be removed from the allowed_moves list 
            #optional: a move which will kill us in the next 20 frames will be removed from the dangerous_but_allowed 


            #FUN PART 
            #a move which will give us fun bonuses (for now it's positive/negative, maybe later it will be a 'score')
            #will be added to the recommended_moves 



            # if closest_ball.x == self.x + 50 or closest_ball.x +50 == self.x:
            #     return Directions.DUCK
            # if (player_to_ball_distance(self, closest_ball) < 100):
            #     return Directions.DUCK
            # if (player_to_ball_distance(self, closest_ball) < 200):
            #     self.shoot()
        except:
            pass

        #If there are still no directions given, 
        
        if self.going_right:
            recommended_moves.append(Directions.RIGHT)
        else: 
            recommended_moves.append(Directions.LEFT)
            # self.shoot()
        
        move_list = [Directions.DUCK, Directions.RIGHT, Directions.LEFT]

        for move in move_list:
            if move in recommended_moves and move in allowed:
                return move 
        for move in allowed:
            #print("We didn't MOVE YET" * 88, allowed, recommended_moves, move_list)
            return move
        for move in dangrous_but_allowed_in_case_of_real_emergency:
            return move
        # self.shoot()
        
        return Directions.LEFT
        
        # if (self.can_freeze):
        #     self.do_freeze()
        
        # closest_player: BasePlayer = get_closest_player(self)
        # if (closest_player != None):
        #     ai_diff: int = closest_player.x - self.x
        #     if (self.can_punch == True):
        #         if (0 < ai_diff < 100):
        #             self.do_right_punch()
        #         if (0 > ai_diff > -100):
        #             self.do_left_punch()
            
        # if (ball_diff > 100 or (0 < ball_diff < 100 and self.shield == True)):
        #     return Directions.RIGHT
        # if (ball_diff < -100 or (0 > ball_diff > -100 and self.shield == True)):
        #     return Directions.LEFT
    def is_ball_in_range(self, x_start, x_end, and_low = False):
        balls = []
        for ball in game_state.game_balls():
            # balls.append(ball.x)
            if x_start < ball.x and ball.x < x_end:
                if and_low:
                    if  400 > ball.y:# DisplayConstants.   RIGHT_BORDER_X_VALUE
                        return True 
                    else: pass 
                else: return True 

        return False 
    
    def most_extreme_right(self):
        extreme = 0
        for ball in game_state.game_balls():
            if ball.x > extreme:
                extreme = ball.x
        return extreme

    def if_ball_to_right(self, close_ball):
        return close_ball.x > self.x
