import pygame
from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.game_core import game_state

from bubble_trouble_ai_competition.utils.constants import Directions, Events, DisplayConstants
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.general_utils import get_closest_ball, get_closest_player, player_to_ball_distance

# The name of the class MUST be the name of the AI, with the filename, followed by 'AI'.
class winnerAI(BasePlayer):
    def __init__(self, events_observable: EventsObservable, ais_dir_path: str) -> None:
        """
        Constructs the example AI.
        """
        # The first parameter MUST be the name of the AI, as written in the filename.
        super().__init__("winner", Directions.RIGHT, events_observable, ais_dir_path=ais_dir_path)


    def pick_x_to_teleport(self):
        for power_up in game_state.game_powerups():
            if "shield" in str(power_up):
                return power_up.x
        player = get_closest_player(self)
        if not player == None:
            return player.x
        return DisplayConstants.RIGHT_BORDER_X_VALUE


    def in_range(self, loc1, loc2, radius):
        # If x range
        if (int(loc2[0] - radius) <= int(loc1[0]) <= int(loc2[0] + radius)):
            #if (int(loc2[1] - radius) < int(loc1[1])) and (int(loc2[1] + radius) > int(loc1[1])):
            return True
        return False


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

        #print("-"*10)

        my_choice = Directions.DUCK
        prediction_options_player = {}
        prediction_options_player["1"] = (self.x + 1*self.speed*game_state.Settings.FRAME_TIME, self.y)
        prediction_options_player["-1"] = (self.x + -1*self.speed*game_state.Settings.FRAME_TIME, self.y)
        prediction_options_player["0"] = (self.x, self.y)
        prediction_options_player["2"] = (self.x, self.y*0.3)

        closest_ball: Ball = get_closest_ball(self)
        closest_player: BasePlayer = get_closest_player(self)

        if (self.can_freeze and closest_player!=None):
            self.do_freeze()

        if closest_ball == None:
            self.shoot()
            return Directions.STAND

        # If I am frozen
        if self.freeze:
            if (self.can_freeze):
                self.do_freeze()
            if (player_to_ball_distance(self, closest_ball) < 300):
                self.shoot()
            return Directions.DUCK

        # If I can punch
        closest_player: BasePlayer = get_closest_player(self)
        if (closest_player != None):
            ai_diff: int = closest_player.x - self.x
            if (self.can_punch == True):
                if (0 < ai_diff < 100):
                    self.do_right_punch()
                if (0 > ai_diff > -100):
                    self.do_left_punch()

        prediction_options_ball = {}
        for ball in game_state.game_balls():
            prediction_options_ball[ball] = (ball.x+ball.speed_x*game_state.Settings.FRAME_TIME, ball.y+ball.speed_y*game_state.Settings.FRAME_TIME)

        # Maybe 100 is better TODO
        if closest_ball.x < self.x and closest_ball.speed_x > 0 and self.x - closest_ball.x < 150:
            self.shoot()
        elif closest_ball.x > self.x and closest_ball.speed_x < 0 and closest_ball.x - self.x < 150:
            self.shoot()

        for ball in prediction_options_ball:
            # Ball goes down
            if ball.speed_y > 0:
                if self.in_range(prediction_options_player[str(my_choice)], prediction_options_ball[ball],
                                 ball.radius + self.head_radius + 30):
                    if self.can_shoot():
                        self.shoot()
                        # Ball goes left
                        if ball.speed_x < 0:
                            my_choice = Directions.LEFT
                        else:
                            my_choice = Directions.RIGHT
                    # Run from the ball
                    else:
                        # Ball goes left
                        if ball.speed_x < 0:
                            my_choice = Directions.RIGHT
                        else:
                            my_choice = Directions.LEFT
            # Ball goes up
            else:
                if self.in_range(prediction_options_player[str(my_choice)], prediction_options_ball[ball],
                                 ball.radius + self.head_radius + 25):
                    self.shoot()
                    my_choice = Directions.DUCK

        # Map powerups
        teleport = None
        shield = None
        points = None
        flag = True
        for power_up in game_state.game_powerups():
            if "teleport" in str(power_up):
                teleport = power_up
            if "shield" in str(power_up):
                shield = power_up
            if "double_points" in str(power_up):
                points = power_up

        # If I have a shield
        if self.shield and teleport:
            if self.x > teleport.x and self.x - teleport.x <250:
                flag = False
                my_choice = Directions.LEFT
            elif self.x < teleport.x and teleport.x - self.x < 250:
                flag = False
                my_choice = Directions.RIGHT
        # If shield on the map
        elif shield:
            if self.x < power_up.x:
                flag = False
                my_choice = Directions.RIGHT
            else:
                flag = False
                my_choice = Directions.LEFT
        # No sheild on map try to go to the teleport
        elif teleport:
            if self.x > teleport.x and self.x - teleport.x < 250:
                flag = False
                my_choice = Directions.LEFT
            elif self.x < teleport.x and teleport.x - self.x < 250:
                flag = False
                my_choice = Directions.RIGHT
            # No teleport in range
            elif points:
                if self.x > points.x and self.x - points.x < 250:
                    flag = False
                    my_choice = Directions.LEFT
                elif self.x < points.x and points.x - self.x < 250:
                    flag = False
                    my_choice = Directions.RIGHT
        # No shield no teleport
        elif points:
            if self.x > points.x and self.x - points.x < 250:
                flag = False
                my_choice = Directions.LEFT
            elif self.x < points.x and points.x - self.x < 250:
                flag = False
                my_choice = Directions.RIGHT

        # If no sheild on the map go to the ball
        if shield == None and flag:
            #print("GO to balls")
            ball_diff: int = closest_ball.x - self.x
            if (ball_diff > 100 and closest_ball.speed_x > 0):
                my_choice = Directions.RIGHT
            if (ball_diff < -100 and closest_ball.speed_x < 0):
                my_choice = Directions.LEFT


        for ball in prediction_options_ball:
            if self.in_range(prediction_options_player[str(my_choice)], prediction_options_ball[ball],
                             ball.radius + self.head_radius+30):
                #print("DANGER DIE")
                #print(my_choice)
                # If stay dies - then move the opposite
                if self.in_range(prediction_options_player[str(Directions.DUCK)], prediction_options_ball[ball],
                                 ball.radius + self.head_radius +25):
                    self.shoot()
                    if my_choice == Directions.RIGHT:
                        my_choice = Directions.LEFT
                    elif my_choice == Directions.LEFT:
                        my_choice = Directions.RIGHT
                else:
                    self.shoot()
                    my_choice = Directions.DUCK

        for ball in prediction_options_ball:
            if self.in_range(prediction_options_player[str(my_choice)], prediction_options_ball[ball],
                             ball.radius + self.head_radius +25):
                if not self.can_shoot():
                    self.do_teleport()
                else:
                    self.shoot()

        #print(my_choice)
        return my_choice
