import pygame
from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.game_core import game_state

from bubble_trouble_ai_competition.utils.constants import Directions, Events, DisplayConstants, ArrowColors
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.utils.general_utils import get_closest_ball, get_closest_player, \
    player_to_ball_distance
from bubble_trouble_ai_competition.utils.constants import PowerupsSettings


# The name of the class MUST be the name of the AI, with the filename, followed by 'AI'.
class TukanziAI(BasePlayer):
    def __init__(self, events_observable: EventsObservable, ais_dir_path: str) -> None:
        """
        Constructs the example AI.
        """
        # The first parameter MUST be the name of the AI, as written in the filename.
        super().__init__("Tukanzi", Directions.RIGHT, events_observable, ais_dir_path=ais_dir_path)
        self.arrow_color: ArrowColors = ArrowColors.LIGHT_PINK
        self.dance = True
        self.win = False
        self.max_score = 0

    def pick_x_to_teleport(self) -> int:

        closest_player: BasePlayer = get_closest_player(self)
        if (closest_player != None and self.can_punch):
            return closest_player.x + DisplayConstants.LEFT_BORDER_X_VALUE

        powerup_list = game_state.game_powerups()
        for powerup in powerup_list:
            if powerup.powerup_image_key == PowerupsSettings.SHIELD_POWERUP:
                return powerup.x
            elif powerup.powerup_image_key == PowerupsSettings.TELEPORT_POWERUP:
                return powerup.x
            elif powerup.powerup_image_key == PowerupsSettings.DOUBLE_POINTS_POWERUP:
                return powerup.x

        return closest_player.x + DisplayConstants.LEFT_BORDER_X_VALUE

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
        closest_ball: Ball = get_closest_ball(self)
        ball_diff: int = closest_ball.x - self.x
        ball_diff_y = self.y - closest_ball.y

        if closest_ball != None:
            if self.can_teleport == True:
                if (0 < ball_diff < 100 or self.shield == False):
                    self.do_teleport()
                    self.shoot()


            if 0 < ball_diff <= 240 and ball_diff_y <= 350 and self.shield == False:
                self.shoot()
                return Directions.LEFT
            if 0 > ball_diff >= -240 and ball_diff_y <= 350 and self.shield == False:
                self.shoot()
                return Directions.RIGHT
            powerup_list = game_state.game_powerups()

            for powerup in powerup_list:
                desired_powerup = None
                min = None
                if self.shield:
                    if powerup.powerup_image_key != PowerupsSettings.MUD:
                        if not min or abs(powerup.x - self.x) < abs(min):
                            min = (powerup.x - self.x)
                            if 0 < min:
                                self.shoot()
                                desired_powerup = Directions.RIGHT
                            elif 0 > min:
                                self.shoot()
                                desired_powerup = Directions.LEFT

                elif powerup.powerup_image_key == PowerupsSettings.DOUBLE_POINTS_POWERUP \
                        or powerup.powerup_image_key == PowerupsSettings.SHIELD_POWERUP \
                        or powerup.powerup_image_key == PowerupsSettings.TELEPORT_POWERUP:

                    if 0 < powerup.x - self.x < 1000:
                        self.shoot()
                        desired_powerup = Directions.RIGHT
                    elif 0 > powerup.x - self.x > -1000:
                        self.shoot()
                        desired_powerup = Directions.LEFT
                if desired_powerup:
                    return desired_powerup

            # Freeze enemy:
            closest_player: BasePlayer = get_closest_player(self)
            if (closest_player != None):
                if (self.can_freeze and (
                        player_to_ball_distance(closest_player, get_closest_ball(closest_player)) < 350)):
                    self.do_freeze()



            if (closest_player != None):
                if (self.can_punch == True):
                    self.do_right_punch()
                    self.do_left_punch()
                    self.shoot()
                    if closest_player.x > self.x:
                        self.shoot()
                        return Directions.RIGHT
                    else:
                        self.shoot()
                        return Directions.LEFT
            #
            # if not self.win:
            #     for player in game_state.game_ais():
            #          if player.score > self.max_score:
            #              self.max_score = player.score
            #     if self.score >= self.max_score:
            #         self.win = True

            # if closest_player == None and self.win:
            #
            #     if self.dance:
            #         self.dance = False
            #         self.shoot()
            #         return Directions.DUCK
            #     else:
            #         self.dance = True
            #         self.shoot()
            #         return Directions.STAND

        self.shoot()
        return Directions.DUCK
