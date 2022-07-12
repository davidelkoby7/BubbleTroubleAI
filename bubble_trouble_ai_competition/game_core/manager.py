import os
import random
import pygame
import importlib
from bubble_trouble_ai_competition.base_objects.arrow_shot import ArrowShot
from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer

# Powerup class
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.powerups.player_speed_boost_powerup import PlayerSpeedBoostPowerup

from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable

from bubble_trouble_ai_competition.game_core.graphics import Graphics
from bubble_trouble_ai_competition.powerups.shield_powerup import ShieldPowerup
from bubble_trouble_ai_competition.ui_elements.ai_scoreboard import AIScoreboard
from bubble_trouble_ai_competition.utils.constants import BallColors, Events, ScoreboardConstants, Settings
from bubble_trouble_ai_competition.utils.exceptions import CantLoadBotException

class GameManager:
    """
    Will manage the game objects, main loop and logic.
    """

    def __init__(self, ais_dir_path: str, fps: int = Settings.FPS, screen_size: tuple = Settings.SCREEN_SIZE) -> None:
        """
        Initializes the game manager.

        Args:
            fps (int): The frames per second to run the game at.
            ais_dir_path (str): The path to the directory containing the ais.
        """
        self.game_over = False
        self.fps = fps
        self.screen_size = screen_size

        self.ai_objects = []
        self.ai_classes = []
        self.shots = []
        self.powerups = [
            PlayerSpeedBoostPowerup(200, 150, Settings.BALL_SPEED, (0, 255, 0)),
            ShieldPowerup(20, 150, Settings.BALL_SPEED, (0, 255, 0)),       
        ]
        self.activated_powerups = []

        self.event_observable = EventsObservable()

        self.event_observable.add_observer(Events.PLAYER_SHOT, self.on_player_shot)
        self.event_observable.add_observer(Events.ARROW_OUT_OF_BOUNDS, self.on_arrow_out_of_bounds)
        self.event_observable.add_observer(Events.BALL_POPPED, self.on_ball_popped)
        self.event_observable.add_observer(Events.POWERUP_PICKED, self.on_powerup_picked)

        self.load_ais(ais_dir_path)

        # Initializing scoreboards.
        self.scoreboards = []
        for i in range(len(self.ais)):
            self.scoreboards.append(AIScoreboard(self.ais[i],Settings.SCOREBOARD_START_POSITION[0] + (Settings.SCOREBOARD_SPACING + ScoreboardConstants.SCOREBOARD_WIDTH) * i,
                                                Settings.SCOREBOARD_START_POSITION[1]))
        
        self.graphics = Graphics()

        self.balls = [
            Ball(100, 100, Settings.BALL_SPEED, 0, 6, BallColors.PURPLE),
            Ball(500, 100, Settings.BALL_SPEED, 0, 2, BallColors.GREEN),
            Ball(300, 200, Settings.BALL_SPEED, 0, 4, BallColors.BLUE),
            ]


    def load_ais(self, ais_dir_path: str) -> None:
        """
        Load the ais from the given directory.

        Args:
            ais_dir_path (str): The path to the directory containing the ais.
    
        Raises:
            CantLoadBotException: If a bot can't be loaded.
        """
        self.ai_classes = []

        # Dynamically load the ais from their files.
        for file in os.listdir(ais_dir_path):
            if (file.endswith(".py") and file != "__init__.py"):
                ai_name = file[:-3] # The minus 3 => Removing the .py ending
                imported_module = importlib.import_module("ais." + ai_name)
                try:
                    self.ai_classes.append(getattr(imported_module, ai_name + "AI"))
                except:
                    raise CantLoadBotException("Could not load ai class: " + ai_name)

        # Create the ai objects.
        self.ais = [class_ref(events_observable = self.event_observable, screen_size = self.screen_size, ais_dir_path = ais_dir_path) for class_ref in self.ai_classes]


    def print_ais(self) -> None:
        """
        Calls the AI's talk method.
        Just for testing to see if the ais are loaded correctly.
        """
        for ai in self.ais:
            ai.talk()


    def run_game(self) -> None:
        """
        Run the main game loop.
        """

        # Main game loop.
        while (self.game_over != True):
            # Keeping the start time of the frame.
            start_time = pygame.time.get_ticks()

            # Shuffling the AI's order to make sure no one has an advantage in the long run by knowing what others are doing.
            random.shuffle(self.ais)

            # Making sure the game isn't over.
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    self.game_over = True  
                    break
            
            all_items = self.balls + self.ais + self.shots + self.powerups
            # Run the main logic for each AI, ball, and shot
            for item in all_items:
                item.update()
            
            for item in self.activated_powerups:
                item.update()
                if (not item.active == True):
                    self.activated_powerups.remove(item)
                
            # Collision detection.
            self.handle_collision()

            # Draw the screen
            self.graphics.draw(self.ais, self.balls, self.shots, self.powerups+self.activated_powerups, self.scoreboards)

            # Calculating the time it took to run this iteration
            time_taken = pygame.time.get_ticks() - start_time

            # Controling the framerate.
            pygame.time.wait(1000 // self.fps - time_taken)


    def handle_collision(self) -> None:
        """
        Handles the collisions in the game.
        """
        # Check if any AI hit a ball.
        for ai in self.ais:
            for ball in self.balls:
                if (ai.collides_with_ball(ball) == True):
                    self.ai_lost(ai)
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

        # Remove all shots made by the AI.
        for shot in self.shots:
            if (shot.shooting_player == ai):
                self.shots.remove(shot)


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

        # Add score to the player that shot the ball.
        shooter.score += ball.size
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

