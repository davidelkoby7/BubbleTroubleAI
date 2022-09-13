import pygame
from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.game_core import game_state

from bubble_trouble_ai_competition.utils.constants import Directions, Events, DisplayConstants
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.general_utils import get_closest_ball, get_closest_player, \
    player_to_ball_distance

FRAME = 0
dont_go_there = []
RUN_KIDDO = False


# The name of the class MUST be the name of the AI, with the filename, followed by 'AI'.
class survivorAI(BasePlayer):
    def __init__(self, events_observable: EventsObservable, ais_dir_path: str) -> None:
        """
        Constructs the survivor AI.
        """
        # The first parameter MUST be the name of the AI, as written in the filename.
        super().__init__("survivor", Directions.RIGHT, events_observable, ais_dir_path=ais_dir_path)

    def INFORMATION_PANIC(self):
        global dont_go_there
        dont_go_there = []
        global FRAME
        for ball in game_state.game_balls():
            frame_when_happens = FRAME
            for_frames = 0
            while ball.y + ball.radius <= self.y - 15:
                # gets the first no no zone
                frame_when_happens += 1
                ball.update()
            bigger_x = ball.x
            smaller_x = ball.x

            while ball.y + ball.radius >= self.y - 15:
                # for_frames += 1
                # end of no no zone
                ball.update()
            if ball.x > bigger_x:
                bigger_x = ball.x
            else:
                smaller_x = ball.x
            smaller_x -= ball.radius * 3 + 10
            bigger_x += ball.radius * 3 + 10
            ball_tuple = (smaller_x, bigger_x, frame_when_happens)  # , for_frames)
            dont_go_there.append(ball_tuple)

    def pick_direction(self) -> Directions:
        global FRAME
        global RUN_KIDDO
        FRAME += 1
        if FRAME == 0:
            RUN_KIDDO = False
        return self.pick_directiond(FRAME)

    def pick_directiond(self, frame) -> Directions:
        global RUN_KIDDO
        global dont_go_there
        if frame % 10 == 0:
            self.INFORMATION_PANIC()

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
        # print("MY LOCATION: " + str(self.x))
        # print("THE FRAME: " + str(frame))
        # print(dont_go_there)

        # powers
        if len(dont_go_there) > 1:
            closest_ball: Ball = get_closest_ball(self)
            if closest_ball is not None:
                ball_diff: int = closest_ball.x - self.x
            if 0 < ball_diff < 100 and not self.shield and self.can_teleport:
                self.do_teleport()

        if self.can_freeze:
            self.do_freeze()

        closest_player: BasePlayer = get_closest_player(self)
        if closest_player is not None:
            ai_diff: int = closest_player.x - self.x
            if self.can_punch:
                if 0 < ai_diff < 100:
                    self.do_right_punch()
                if 0 > ai_diff > -100:
                    self.do_left_punch()

        # movement
        if not dont_go_there:
            dont_go_there = sorted(dont_go_there, key=lambda tup: tup[2])
        for no_no_spot in dont_go_there:
            if no_no_spot[0] <= self.x <= no_no_spot[1]:
                dodge_frames = no_no_spot[2] - frame
                if dodge_frames < 30:
                    if abs(self.x - no_no_spot[0]) > abs(no_no_spot[1] - self.x):
                        self.shoot()
                        return Directions.RIGHT
                    else:
                        self.shoot()
                        return Directions.LEFT
        # shoot
        self.shoot()

        if self.x + 50 >= DisplayConstants.RIGHT_BORDER_X_VALUE / 1.5:
            return Directions.LEFT
        elif self.x - 400 <= DisplayConstants.LEFT_BORDER_X_VALUE:
            return Directions.RIGHT
        return Directions.DUCK
