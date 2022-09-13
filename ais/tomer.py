import math
import random

from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.game_core.game_state import game_balls
from bubble_trouble_ai_competition.utils.constants import Directions, DisplayConstants
from bubble_trouble_ai_competition.utils.general_utils import get_closest_ball, get_closest_player, \
    player_to_ball_distance


# The name of the class MUST be the name of the AI, with the filename, followed by 'AI'.
class tomerAI(BasePlayer):
    def __init__(self, events_observable: EventsObservable, ais_dir_path: str) -> None:
        """
        Constructs the example AI.
        """
        # The first parameter MUST be the name of the AI, as written in the filename.
        super().__init__("tomer", Directions.RIGHT, events_observable, ais_dir_path=ais_dir_path)

    def pick_direction(self) -> Directions:

        self.handle_shoot()
        self.handle_teleport()
        self.handle_freeze()
        self.handle_punch()

        return self.handle_direction()

    def handle_punch(self):
        closest_player: BasePlayer = get_closest_player(self)

        if closest_player:
            ai_diff: int = closest_player.x - self.x
            if self.can_punch:
                if 0 < ai_diff < 100:
                    self.do_right_punch()
                if 0 > ai_diff > -100:
                    self.do_left_punch()

    def handle_teleport(self):
        closest_ball: Ball = get_closest_ball(self)
        if not closest_ball:
            return False
        ball_diff: int = closest_ball.x - self.x
        if 0 < ball_diff < 100 and self.shield == False and self.can_teleport == True:
            self.do_teleport()

    def handle_freeze(self):
        closest_player: BasePlayer = get_closest_player(self)

        if not closest_player:
            return

        closest_ball_to_enemy: Ball = get_closest_ball(closest_player)
        dist_from_enemy: float = player_to_ball_distance(closest_player, closest_ball_to_enemy)

        if self.can_freeze and dist_from_enemy < 100:
            self.do_freeze()

    def handle_shoot(self):

        if self.should_i_shoot():
            self.shoot()

    def handle_direction(self):

        closest_ball: Ball = get_closest_ball(self)
        if not closest_ball:
            return Directions.DUCK
        diff_x: int = closest_ball.x - self.x
        diff_y: int = closest_ball.y - self.y

        if self.freeze:
            return Directions.DUCK

        if self.speed > 0 and closest_ball.speed_x > 0:
            if closest_ball.x < self.x:
                if diff_y > 200 and diff_x < 50:
                    return Directions.LEFT

        if self.speed < 0 and closest_ball.speed_x < 0:
            if closest_ball.x > self.x:
                if diff_y > 200 and diff_x < 50:
                    return Directions.RIGHT

        if self.is_ball_going_to_hit_me() or math.fabs(diff_x) < 50 and not self.shield:
            return self.avoid()
        else:
            return self.chase()

    def pick_x_to_teleport(self):
        if self.can_punch:
            if get_closest_player(self):
                return get_closest_player(self).x
        return random.choice(range(DisplayConstants.LEFT_BORDER_X_VALUE, DisplayConstants.RIGHT_BORDER_X_VALUE))

    def should_i_shoot(self):

        closest_ball: Ball = get_closest_ball(self)
        if not closest_ball:
            return False

        if player_to_ball_distance(self, closest_ball) < 10:
            return True

        if player_to_ball_distance(self, closest_ball) < 250:
            if closest_ball.speed_x < 0:
                if closest_ball.x > self.x:
                    return True
            else:
                if closest_ball.x < self.x:
                    return True

        balls = game_balls()
        list_of_bools = []

        for ball in balls:
            list_of_bools.append(player_to_ball_distance(self, ball) < 250)

        if list_of_bools.count(True) > 2:
            return True

        return False

    def is_closest_ball_coming_to_me(self):
        closest_ball: Ball = get_closest_ball(self)
        if not closest_ball:
            return False
        if closest_ball.speed_x < 0:
            if closest_ball.x > self.x:
                return True
        else:
            if closest_ball.x < self.x:
                return True

    def is_closest_ball_getting_away_from_me(self):
        closest_ball: Ball = get_closest_ball(self)

        if not closest_ball:
            return False

        if closest_ball.speed_x < 0:
            if closest_ball.x < self.x:
                return True
        else:
            if closest_ball.x > self.x:
                return True

    def is_ball_going_to_hit_me(self):
        closest_ball: Ball = get_closest_ball(self)

        if not closest_ball:
            return False

        return self.is_closest_ball_coming_to_me() and \
               player_to_ball_distance(self, closest_ball) < 180

    def avoid(self):
        closest_ball: Ball = get_closest_ball(self)
        if not closest_ball:
            return Directions.DUCK

        diff_x: int = closest_ball.x - self.x
        diff_y: int = closest_ball.y - self.y

        # Moving under the ball, Not working
        # if diff_y * 1.5 > self.y and math.fabs(diff_x) < 100:
        #     if self.speed < 0 and closest_ball.speed_x < 0:
        #         return Directions.RIGHT
        #     if self.speed > 0 and closest_ball.speed_x > 0:
        #         return Directions.LEFT

        if closest_ball.x < self.x:  # Ball is coming from left
            return Directions.RIGHT
        else:
            return Directions.LEFT

    def chase(self):
        closest_ball: Ball = get_closest_ball(self)
        if not closest_ball:
            return Directions.DUCK

        if math.fabs(self.x - closest_ball.x) < 25:
            return Directions.DUCK
        if closest_ball.x > self.x:  # Ball is coming from left
            return Directions.RIGHT
        else:
            return Directions.LEFT
