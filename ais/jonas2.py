import pygame
from bubble_trouble_ai_competition.base_objects.arrow_shot import ArrowShot
from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.game_core import game_state

from bubble_trouble_ai_competition.utils.constants import Directions, Events, Settings
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.general_utils import get_closest_ball, get_closest_player, player_to_ball_distance

# The name of the class MUST be the name of the AI, with the filename, followed by 'AI'.
class jonas2AI(BasePlayer):
    def __init__(self, events_observable: EventsObservable, ais_dir_path: str) -> None:
        """
        Constructs the example AI.
        """
        # The first parameter MUST be the name of the AI, as written in the filename.
        super().__init__("jonas2", Directions.RIGHT, events_observable, ais_dir_path=ais_dir_path)


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
        closest_player: BasePlayer = get_closest_player(self)
        closest_ball: Ball = get_closest_ball(self)
        total = 0
        num = 0
        for ball in game_state.game_balls():
            total +=ball.x
            num +=1
        average_x = total/num
        if (closest_player != None):
            ai_diff: int = closest_player.x - self.x
            if (self.can_punch == True):
                if (0 < ai_diff < 100):
                    self.do_right_punch()
                if (0 > ai_diff > -100):
                    self.do_left_punch()
        ball_diff: int = closest_ball.x - self.x
        if (0 < ball_diff < 100 and self.shield == False and self.can_teleport == True):
            self.do_teleport()
        
        if (self.can_freeze):
            self.do_freeze()


        yaad_x = average_x#650#closest_ball.x#650
        distance_to_ball = self.distance((self.x, self.y), (closest_ball.x + closest_ball.radius, closest_ball.y + closest_ball.radius))
        if(self.can_shoot()):
            if(distance_to_ball<250):
                self.shoot()
        if(distance_to_ball<150):
            ball_diff: int = closest_ball.x - self.x
            if(ball_diff>0): return Directions.LEFT
            if(ball_diff<0): return Directions.RIGHT
        
        if((self.x-yaad_x) > 100): 
            return Directions.LEFT
        if((self.x-yaad_x) < -100):
            return Directions.RIGHT
        print(self.x-650)
        return Directions.DUCK
        print(self.x)
        closest_ball: Ball = get_closest_ball(self)
        #if (player_to_ball_distance(self, closest_ball) < 300):
        #    self.shoot()

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
        #if(closest_ball.y > 450):
        #    print(closest_ball.y)
        #    if(ball_diff>0): 
        #        print("EMERGENCY MOVE", ball_diff)
        #        return Directions.RIGHT
        #    if(ball_diff<0): 
        #        return Directions.LEFT
        if (ball_diff > 100 or (0 < ball_diff < 100 and self.shield == True)):
            return Directions.RIGHT
        if (ball_diff < -100 or (0 > ball_diff > -100 and self.shield == True)):
            return Directions.LEFT

        return Directions.DUCK

    def update_89_time_all_balls_and_check_if_we_will_kill_one(self):
        if(self.can_shoot()):
            for ball in game_state.game_balls():
                #new_shot : ArrowShot = ArrowShot(Settings.ARROW_SPEED, self, None)
                for i in range(80):
                    ball.update()
                    #new_shot.update()
                    '''print("ball.x", ball.x)
                    print("ball.y", ball.y)
                    #print(ball.x)
                    print(new_shot.y)
                    #print("self.x", self.x)
                    print(ball.collides_with_shot(new_shot))
                    if(ball.collides_with_shot(new_shot)):'''
                    if(abs(ball.x - self.x) < 1):

                        return True
            return False
    def distance(self, point1: tuple, point2: tuple) -> float:
        """
        Calculates the distance between two points.

        Args:
            point1 (tuple): The first point.
            point2 (tuple): The second point.
        
        Returns:
            float: The distance between the two points.
        """
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5