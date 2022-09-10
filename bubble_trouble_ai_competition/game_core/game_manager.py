import os
import sys
import json
import random
import pygame

# Base objects class
from bubble_trouble_ai_competition.base_objects.arrow_shot import ArrowShot
from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.base_objects.countdown_bar import CountdownBar
from bubble_trouble_ai_competition.base_objects.base_alert import Alert

# Powerup class
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.powerups.player_speed_boost_powerup import PlayerSpeedBoostPowerup
from bubble_trouble_ai_competition.powerups.player_speed_slower_powerup import PlayerSpeedSlowerPowerup
from bubble_trouble_ai_competition.powerups.player_double_points_powerup import PlayerDoublePointsPowerup
from bubble_trouble_ai_competition.powerups.teleport_powerup import TeleportPowerup
from bubble_trouble_ai_competition.powerups.shield_powerup import ShieldPowerup
from bubble_trouble_ai_competition.powerups.punch_powerup import PunchPowerup
from bubble_trouble_ai_competition.powerups.freeze_powerup import FreezePowerup

# Games utils and graphics
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.game_core.graphics import Graphics
from bubble_trouble_ai_competition.ui_elements.ai_scoreboard import AIScoreboard
from bubble_trouble_ai_competition.utils.constants import AlertConstants, DisplayConstants, Events, ScoreboardConstants, Settings
from bubble_trouble_ai_competition.utils.exceptions import LevelNotFound
from bubble_trouble_ai_competition.utils.load_display import load_game_images, load_display_objects
from bubble_trouble_ai_competition.game_core.game_state import GameState, update_game_state


class GameManager:
    """
    Will manage the game objects, main loop and logic.
    """

    def __init__(self, ais_dir_path: str, ais:list[BasePlayer], event_observable: EventsObservable, graphics: Graphics, level: str, fps: int = Settings.FPS) -> None:
        """
        Initializes the game manager.

        Args:
            fps (int): The frames per second to run the game at.
            ais_dir_path (str): The path to the directory containing the ais.
            level (str): The path of the level to load.
        """
        load_display_objects()
        load_game_images()
        
        if (self.load_level_data(level) == False):
            raise LevelNotFound(f"{level}")
        
        self.initialize_level()
        
        self.event_observable = event_observable
        self.graphics = graphics
        self.ais_dir_path = ais_dir_path
        self.ais = [ai for ai in ais if ai.is_competing == True]

        self.game_over = False
        self.fps = fps

        self.shots: list[ArrowShot] = []
        self.alert: Alert = None

        self.activated_powerups = []

        self.event_observable.add_observer(Events.PLAYER_SHOT, self.on_player_shot)
        self.event_observable.add_observer(Events.ARROW_OUT_OF_BOUNDS, self.on_arrow_out_of_bounds)
        self.event_observable.add_observer(Events.BALL_POPPED, self.on_ball_popped)
        self.event_observable.add_observer(Events.POWERUP_PICKED, self.on_powerup_picked)
        self.event_observable.add_observer(Events.GAME_TIMEOUT, self.on_game_timeout)
        self.event_observable.add_observer(Events.SHOWED_ALERT, self.on_showed_alert)
        self.event_observable.add_observer(Events.PLAYER_LPUNCH, self.on_player_left_punch)
        self.event_observable.add_observer(Events.PLAYER_RPUNCH, self.on_player_right_punch)
        self.event_observable.add_observer(Events.PLAYER_COLLIDES_LPUNCH, self.on_player_collides_left_punch)
        self.event_observable.add_observer(Events.PLAYER_COLLIDES_RPUNCH, self.on_player_collides_right_punch)
        self.event_observable.add_observer(Events.FREEZE_PLAYER, self.on_freeze_player)
        self.event_observable.add_observer(Events.TELEPORTING_PLAYER, self.on_teleporting_player)
        
        # Initializing scoreboards.
        self.scoreboards = []
        for i in range(len(self.ais)):
            self.scoreboards.append(AIScoreboard(self.ais[i], ScoreboardConstants.SCOREBOARD_START_POSITION[0] + (ScoreboardConstants.SCOREBOARD_SPACING + ScoreboardConstants.SCOREBOARD_WIDTH) * i,
                                                ScoreboardConstants.SCOREBOARD_START_POSITION[1]))

        # Initializing countdown bar
        self.countdown_bar = CountdownBar(self.game_timeout, self.event_observable)
    

    def initialize_level(self) -> None:
        self.game_timeout = self.level_data["duration"] * Settings.FPS

        self.balls: list[Ball] = []
        for ball in self.level_data["balls"]:
            self.balls.append(
                Ball(
                    ball["x"] * DisplayConstants.SCREEN_BIT,
                    ball["y"] * DisplayConstants.SCREEN_BIT,
                    ball["speed_x"] * DisplayConstants.SCREEN_BIT,
                    ball["speed_y"] * DisplayConstants.SCREEN_BIT,
                    ball["size"],
                    ball["color"]
                    )
                )
        
        self.powerups = []
        self.powerups_data: list[Powerup] = []
        for powerup in self.level_data["powerups"]:
            self.powerups_data.append({"class": getattr(sys.modules[__name__], powerup["name"]), "probability": powerup["spawn_probability"]})


    def load_level_data(self, level:str):
        if (not os.path.exists(level)):
            return False
        
        with open(level, "r") as f:
            self.level_data = json.load(f)
        
        return True


    def run_game(self) -> None:
        """
        Run the main game loop.
        """
        # Main game loop.
        while (self.game_over != True):

            # Update the game state at the current game's frame.
            update_game_state(self.ais, self.shots, self.balls, self.powerups, self.activated_powerups, self.countdown_bar.frames_remaining)

            # Keeping the start time of the frame.
            start_time = pygame.time.get_ticks()

            # Shuffling the AI's order to make sure no one has an advantage in the long run by knowing what others are doing.
            random.shuffle(self.ais)

            # Making sure the game isn't over.
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    self.game_over = True  
                    break
            
            if self.alert:
                self.alert.update()
            
            self.handle_powerup_creation()

            all_items = self.balls + self.ais + self.shots + self.powerups + [self.countdown_bar] 

            # Run the main logic for each AI, ball, and shot
            for item in all_items:
                item.update()
            
            for item in self.activated_powerups:
                item.update()
                if (not item.active == True):
                    self.activated_powerups.remove(item)
            
                                        
            # Handle powerups actions
            self.handle_powerup_actions()

            # Collision detection.
            self.handle_collision()

            # Draw the screen
            self.graphics.draw(self.ais, self.balls, self.shots, self.powerups+self.activated_powerups, self.scoreboards, self.alert, self.countdown_bar)
  
            # Calculating the time it took to run this iteration
            time_taken = pygame.time.get_ticks() - start_time

            # Controling the framerate.
            pygame.time.wait(1000 // self.fps - time_taken)
        
        self.event_observable.notify_observers(Events.CHANGE_GAME_TO_MENU)

    
    def handle_powerup_creation(self):
        for powerup in self.powerups_data:
            rand_value:int = random.random()
            if (rand_value <= powerup["probability"]):
                rand_x = random.randint(DisplayConstants.LEFT_BORDER_X_VALUE, DisplayConstants.RIGHT_BORDER_X_VALUE)
                self.powerups.append(powerup["class"](rand_x, DisplayConstants.CIELING_Y_VALUE, Settings.BALL_SPEED))


    def get_active_powerups_by_type(self, powerup_type) -> list[Powerup]:
        return [powerup for powerup in self.activated_powerups if isinstance(powerup, powerup_type)]


    def handle_powerup_actions(self) -> None:
        # Handle punch powerup actions.
        for punch_powerup in self.get_active_powerups_by_type(PunchPowerup):
            # Creates action punch event by punch direction.
            if punch_powerup.player.punch_right:
                self.event_observable.notify_observers(Events.PLAYER_RPUNCH, punch_powerup)

            elif punch_powerup.player.punch_left:
                self.event_observable.notify_observers(Events.PLAYER_LPUNCH, punch_powerup)
        
        # Handle freeze powerup action.
        for freeze_powerup in self.get_active_powerups_by_type(FreezePowerup):
            # Creates freeze player event.
            if freeze_powerup.player.freeze_action:
                self.event_observable.notify_observers(Events.FREEZE_PLAYER, freeze_powerup,
                                                        freeze_powerup.player.pick_player_to_freeze())
        
        # Handle teleport powerup action.
        for teleport_powerup in self.get_active_powerups_by_type(TeleportPowerup):
            # Creates teleporting player event.
            if teleport_powerup.player.is_teleporting:
                self.event_observable.notify_observers(Events.TELEPORTING_PLAYER, teleport_powerup)
    

    def get_player_powerup(self, ai, powerup_instance):
        """Get powerup by player and powerup instance. """
        for powerup in self.activated_powerups:
            if powerup.player == ai and type(powerup) == powerup_instance:
                return powerup
        return None


    def handle_punch_collision(self) -> None:

         # Check if ai punched by other ai's punch.
        for powerup_punch in self.get_active_powerups_by_type(PunchPowerup):

            # Get all ais that are not the player with the powerup punch.
            for ai in [ai for ai in self.ais if ai != powerup_punch.player]:

                # Check if ai collides with punch.
                if ai.collides_with_punch(powerup_punch, powerup_punch.player.punch_left, powerup_punch.player.punch_right):

                    if ai.shield:

                        # Pop ai shield
                        shield_powerup = self.get_player_powerup(ai, ShieldPowerup)
                        ai.shield = False
                        self.activated_powerups.remove(shield_powerup)

                    # Creates punch collision events by direction.
                    if powerup_punch.player.punch_left:
                        self.event_observable.notify_observers(Events.PLAYER_COLLIDES_LPUNCH, powerup_punch, ai)
                    
                    elif powerup_punch.player.punch_right:
                        self.event_observable.notify_observers(Events.PLAYER_COLLIDES_RPUNCH, powerup_punch, ai)


    def handle_collision(self) -> None:
        """
        Handles the collisions in the game.

        """
        self.handle_punch_collision()

        # Check collision for the ais.
        for ai in self.ais:

            # Check if AI hit by a ball.
            for ball in self.balls:
                if (ai.collides_with_ball(ball) == True):
                    self.ai_lost(ai)

            # Check if AI pickup a powerup.
            for powerup in self.powerups:
                if (ai.collides_with_powerup(powerup) == True):
                    self.event_observable.notify_observers(Events.POWERUP_PICKED, powerup, ai)

        # Check if any ball hit a shot.
        for ball in self.balls:
            for shot in self.shots:
                if (ball.collides_with_shot(shot) == True):
                    shot.shooting_player.is_shooting = False
                    ball.last_shot_by = shot.shooting_player
                    self.shots.remove(shot)
                    self.event_observable.notify_observers(Events.BALL_POPPED, ball, ball.last_shot_by)
        
        # Check if a ball hit the ceiling.
        for ball in self.balls[:]:
            if (ball.collides_with_ceiling() == True):
                self.event_observable.notify_observers(Events.BALL_POPPED, ball, ball.last_shot_by, ceiling_shot = True)
        
        # check if powerup is not pickable anymore
        for powerup in self.powerups:
            if powerup.pickable == False:
                self.powerups.remove(powerup)
        

    def ai_lost(self, ai: BasePlayer) -> None:
        """
        Called when an AI loses.
        Will remove it from the actively playing ais.

        Args:
            ai (BasePlayer): The AI that lost.
        """
        # TODO: Implement something normal.

        # Kill the AI.
        self.ais.remove(ai)

        # Remove the freezing made by other players.
        ai.freeze = False
        
        # Remove all shots made by the AI.
        for shot in self.shots:
            if (shot.shooting_player == ai):
                self.shots.remove(shot)
        
        # Deactivate and remove all powerups of AI.
        for powerup in self.activated_powerups[:]:
            if powerup.player == ai:
                powerup.deactivate()
                self.activated_powerups.remove(powerup)


    def on_player_shot(self, ai: BasePlayer) -> None:
        """
        Called when a player shoots.

        Args:
            ai (BasePlayer): The AI that shot.
        """
        self.shots.append(ArrowShot(Settings.ARROW_SPEED, ai, self.event_observable))
    

    def on_arrow_out_of_bounds(self, arrow: ArrowShot) -> None:
        """
        Called when an arrow goes out of bounds.

        Args:
            arrow (ArrowShot): The arrow that went out of bounds.
        """
        arrow.shooting_player.is_shooting = False
        self.shots.remove(arrow)


    def on_powerup_picked(self, powerup: Powerup, player: BasePlayer) -> None:
        """
        Called when a powerup is picked.

        Args:
            powerup (Powerup): The powerup that was picked.
        """
        self.powerups.remove(powerup)
        self.activated_powerups.append(powerup)
        powerup.activate(player)


    def on_ball_popped(self, ball: Ball, shooter: BasePlayer, ceiling_shot = False) -> None:
        """
        Called when a ball is popped.

        Args:
            ball (Ball): The ball that was popped.
            shooting_player (BasePlayer): The player that shot the ball.
        """
        # Remove the ball from the game.
        self.balls.remove(ball)

        # Add points to player's score that shot the ball.
        points = ball.size

        # Double the points if player have active double points powerup.
        if self.get_player_powerup(shooter, PlayerDoublePointsPowerup):
            points = points * 2
        
        # Add to points from shot to player's score.
        shooter.score += points
        if (ceiling_shot == True):
            shooter.score += sum([i for i in range(ball.size)])

        # If the ball is at a minimum size, it will not be split.
        if (ball.size == 1):
            return
        
        # Otherwise - split the ball into 2 smaller balls, if it's not a ceiling shot.
        if (ceiling_shot == False):
            if (ball.speed_y > 0):
                new_vertical_speed = Settings.BALL_POPPED_DOWN_SPEED
            else:
                new_vertical_speed = ball.speed_y - Settings.BALL_POPPED_UP_SPEED_DEC

            self.balls.append(Ball(ball.get_raw_x(), ball.get_raw_y(), ball.speed_x, new_vertical_speed, ball.size - 1, ball.color, last_shot_by=ball.last_shot_by))
            self.balls.append(Ball(ball.get_raw_x(), ball.get_raw_y(), -ball.speed_x, new_vertical_speed, ball.size - 1, ball.color, last_shot_by=ball.last_shot_by))


    def on_game_timeout(self) -> None:
        """
        Called when game time is up.
        Creates and Alert object to notice and end game.
        """
        self.alert = Alert(alert_type=AlertConstants.ALERT_GAME_TIMEOUT, end_game=True, events_observable=self.event_observable)


    def on_showed_alert(self, alert: Alert) -> None:
        """
        Called when alert was shown to screen.
        Freeze the screen and get the alert's action in game (ends or continue).
        """

        pygame.time.wait(alert.frames_freeze)
        self.alert = None
        self.game_over = alert.end_game
    

    def on_player_right_punch(self, punch: PunchPowerup):
        """ Player's right punch action. """
        punch.action_right_punch = True
    

    def on_player_left_punch(self, punch: PunchPowerup):
        """ Player's left punch action. """
        punch.action_left_punch = True
    

    def on_player_collides_left_punch(self, punch: PunchPowerup, ai: BasePlayer):
        """ Player's left punch action collides. """
        punch.collides_left_punch = True
        ai.get_left_punch_hit(punch)
    
    
    def on_player_collides_right_punch(self, punch: PunchPowerup, ai:BasePlayer):
        """ Player's right punch action collides. """
        punch.collides_right_punch = True
        ai.get_right_punch_hit(punch)
    

    def on_freeze_player(self, freeze_powerup: FreezePowerup, player_name: BasePlayer):
        """ Freeze player. """
        ai = self.get_ai_by_name(player_name)
        freeze_powerup.freeze_player = ai
        freeze_powerup.player.freeze_action = False


    def get_ai_by_name(self, ai_name) -> BasePlayer:
        """ Returns the ai object by his name. """
        searched_ai = [ai for ai in self.ais if ai.name == ai_name]
        if (searched_ai == []):
            return None
        return searched_ai[0]


    def on_teleporting_player(self, teleport_powerup: TeleportPowerup):
        """ Teleporting player """
        teleport_powerup.action = True
        teleport_powerup.player.teleport()
        if teleport_powerup.was_teleported:
            teleport_powerup.deactivate()
            
