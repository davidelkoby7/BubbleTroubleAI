from asyncio import shield
import random
from re import X
import pygame
from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.game_core import game_state


from bubble_trouble_ai_competition.utils.constants import Directions, DisplayConstants, Events, Settings, PowerupsSettings, ArrowColors
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.general_utils import circle_rect_collide, circles_collide, distance, get_closest_ball, get_closest_player, player_to_ball_distance




# Constants
BALL = "high"
LENGHT = 100


# The name of the class MUST be the name of the AI, with the filename, followed by 'AI'.
class ggcgAI(BasePlayer):
    priority_teleport = -1
    priority_x = -1
    def __init__(self, events_observable: EventsObservable, ais_dir_path: str) -> None:
        """
        Constructs the example AI.
        """
        # The first parameter MUST be the name of the AI, as written in the filename.
        super().__init__("ggcg", Directions.RIGHT, events_observable, ais_dir_path=ais_dir_path)

    def pick_x_to_teleport(self):
        if self.priority_teleport != -1:
            return self.priority_teleport
        possible = None
        while not possible:
            possible = random.choice(range(DisplayConstants.LEFT_BORDER_X_VALUE, DisplayConstants.RIGHT_BORDER_X_VALUE))
            if self.is_x_safe(possible):
                pass
            else:
                possible = None
        return possible


    def do_teleport(self) -> None:
        """Teleport to another place in game with the teleport powerup"""
        if self.can_teleport:
            self.is_teleporting = True
    
    
    def get_closest_ball_to_x(self, x) -> 'Ball':
        """
        Returns the closest ball to a point.

        Args:
            point (BasePlayer): The player.
            balls (List['Ball']): The list of balls.
        
        Returns:
            Ball: The closest ball to the player.
        """
        return min(game_state.game_balls(), key=lambda ball: distance((x, Settings.PLAYER_DIMENSIONS[1]), (ball.x + ball.radius, ball.y + ball.radius)))


    def is_x_safe(self, targrt_x):
        closest_ball_to_x: Ball = self.get_closest_ball_to_x(X)
        if self.shield == True or self.is_teleporting == True:
            return True

        # Check if the player's head collides with the ball
        if (circles_collide(targrt_x, self.head_radius, (closest_ball_to_x.x, closest_ball_to_x.y), closest_ball_to_x.radius)):
            return False
        
        # Check if the player's body collides with the ball
        if (circle_rect_collide(targrt_x, self.y, self.width, self.height, closest_ball_to_x.x, closest_ball_to_x.y, closest_ball_to_x.radius)):
            return False
        
        # No collision - return False
        return True
        

    def pick_direction(self) -> Directions:
        """
        The main function where you decide what to do.
        In here - you MUST *return* a value of which direction to go.
        This can be one of the following:
        Directions.LEFT, Directions.RIGHT, Directions.STAND, Directions.DUCK
        In addition - you can call self.shoot() to shoot an arrow, and self.do_teleport() to teleport.
        Also - if you have the freeze powerup on you (can be checked with self.can_freeze), you can call self.do_freeze() to freeze an enemy.
        Another powerup is the punch powerup, which can be used with self.do_left_punch() and self.do_right_punch()and powerups can be used *in addition* to your mov    ement - which is the return value.
        """
        # To get info about other things in the game - use the game_state file.
        closest_ball: Ball = get_closest_ball(self)
        if closest_ball:
            if (player_to_ball_distance(self, closest_ball) < 130):
                self.shoot()
                return Directions.DUCK

            ball_diff: int = closest_ball.x - self.x
            # Teleports
            
            closest_player: BasePlayer = get_closest_player(self)
            powerups = game_state.game_powerups()
            closest_shield_x = -1
            closest_teleport_x = -1
            closest_doublepoint_x = -1
            for powerup in powerups:
                # Find closest shield
                if powerup.powerup_image_key == PowerupsSettings.SHIELD_POWERUP:
                    if powerup.x < closest_shield_x:
                        closest_shield_x = powerup.x
                # Find closest teleport
                if powerup.powerup_image_key == PowerupsSettings.TELEPORT_POWERUP:
                    if powerup.x < closest_teleport_x:
                        closest_teleport_x = powerup.x
                # Find closest doublepoint 
                if powerup.powerup_image_key == PowerupsSettings.DOUBLE_POINTS_POWERUP:
                    if powerup.x < closest_doublepoint_x:
                        closest_doublepoint_x = powerup.x

            if self.can_teleport == True:
                if (self.shield == False):
                    if closest_shield_x != -1:
                        self.priority_teleport = closest_shield_x
                        self.do_teleport()
                    if (0 < ball_diff < 50):
                        if closest_doublepoint_x != -1:
                            self.priority_teleport = closest_doublepoint_x
                            self.do_teleport()
                        else:
                            self.do_teleport()
            
            
            # Powerup Priority
            if closest_shield_x != -1 and closest_shield_x < closest_teleport_x:
                self.priority_x = closest_shield_x
            elif closest_doublepoint_x != -1 and closest_doublepoint_x < closest_teleport_x:
                self.priority_x = closest_doublepoint_x
            elif closest_teleport_x != -1 and not self.can_teleport:
                self.priority_x = closest_doublepoint_x
                
            
            if closest_player:
                # closest_ball_to_enemy: closest_ball = BasePlayerBasePlayer
                if (self.can_freeze and closest_player.x < 100):
                    if (BALL == "high") and (LENGHT <= 100):
                        self.do_freeze()
                        self.talk("{} is gonna be frozen HAHA YOU NOOBBBB".format(self.pick_player_to_freeze()))
                        self.do_freeze()
                ai_diff: int = closest_player.x - self.x
                if (self.can_punch == True):
                    if (0 < ai_diff < 100):
                        self.do_right_punch()
                        self.talk()
                    if (0 > ai_diff > -100):
                        self.do_left_punch()
                        self.talk()
            if (self.priority_x != -1):
                if ((self.x - self.priority_x) < 0):
                    self.priority_x = -1
                    return Directions.RIGHT
                else:
                    self.priority_x = -1
                    return Directions.LEFT

            
            if (ball_diff > 100 or (0 < ball_diff < 100 and self.shield == True)):
                return Directions.RIGHT
            if (ball_diff < -100 or (0 > ball_diff > -100 and self.shield == True)):
                return Directions.LEFT
            return Directions.DUCK                
