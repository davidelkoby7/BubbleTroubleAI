import pygame
import os
import math
from bubble_trouble_ai_competition.base_objects.arrow_shot import ArrowShot
from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.base_objects.base_alert import Alert
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.base_objects.countdown_bar import CountdownBar
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.ui_elements.ai_scoreboard import AIScoreboard
from bubble_trouble_ai_competition.ui_elements.action_button import ActionButton
from bubble_trouble_ai_competition.ui_elements.pick_button import PickButton
from bubble_trouble_ai_competition.utils.constants import AlertConstants, CountdownBarConstants, DesignConstants, DisplayConstants, Events, MainMenuConstants, PowerupsSettings, ScoreboardConstants, Settings, settings_properties_to_scale, design_constants_properties_to_scale, powerup_constants_to_update, countdown_bar_constants_to_update, alert_constants_to_update, main_menu_constants_to_update
from bubble_trouble_ai_competition.utils.load_display import Images, DisplayObjects

class Graphics:
    """
    Will handle the graphics.
    """
    
    def __init__(self, events_observable: EventsObservable):
        """
        Initialize the graphics.

        Args:
            screen_size (tuple): The size of the screen.
            background_color (tuple): The background color.
        """
        # Initialize the pygame module.
        pygame.init()
        self.handle_display_constants()

        # Store initial values.

        self.events_observable = events_observable

        self.game_area_size = DisplayConstants.GAME_AREA_SIZE
        self.game_area_width = self.game_area_size[0]
        self.game_area_height = self.game_area_size[1]

        self.game_area_position = DisplayConstants.GAME_AREA_POSITION

        # Initializing action buttons
        self.menu_buttons: list[ActionButton] = []
        action_buttons_to_create = [("Play!", self.start_playing), ("Exit", self.quit_menu)]
        self.create_action_buttons(action_buttons_to_create)

        # Initializing selection of level and players buttons.
        ai_buttons_to_create = [(ai, self.pick_ai, self.unpick_ai) for ai in self.get_ai_names()]
        levels_buttons_to_create = [(level_name, self.pick_level, self.unpick_level) for level_name in self.get_levels_names()]
        self.levels_buttons: list[PickButton] = self.create_pick_buttons(levels_buttons_to_create, MainMenuConstants.LEVELS_INITIAL_HEIGHT, MainMenuConstants.LEVELS_LEFT_MARGIN)
        self.ai_buttons: list[PickButton] = self.create_pick_buttons(ai_buttons_to_create, MainMenuConstants.AIS_BUTTONS_INITIAL_HEIGHT, MainMenuConstants.AIS_BUTTONS_LEFT_MARGIN)
    
    def keep_button_in_border(self, button, buttons_initial_height, buttons_left_margin):
        if button.y > MainMenuConstants.MENU_FLOOR_Y_BORDER:
            MainMenuConstants.SHIFT_RIGHT_AMOUNT += 1
            button.y = buttons_initial_height
            button.x = buttons_left_margin + MainMenuConstants.BUTTONS_PICK_WIDTH*MainMenuConstants.SHIFT_RIGHT_AMOUNT*1.2


    def create_pick_buttons(self, pick_buttons_to_create, buttons_initial_height, buttons_left_margin) -> list[PickButton]:
        bottons: list[PickButton] = []
        curr_y: int = buttons_initial_height
        curr_x: int = buttons_left_margin
        MainMenuConstants.SHIFT_RIGHT_AMOUNT = 0
        for button_name, pick_button, unpick_button in pick_buttons_to_create:
            button = PickButton(curr_x, curr_y, 
                MainMenuConstants.BUTTONS_PICK_WIDTH, MainMenuConstants.BUTTONS_PICK_HEIGHT,
                button_name, on_pick=pick_button, on_unpick=unpick_button)
            bottons.append(button)
            self.keep_button_in_border(button, buttons_initial_height, buttons_left_margin)
            curr_y = button.y + MainMenuConstants.BUTTONS_PICK_HEIGHT
            curr_x = button.x
        
        return bottons


    def create_action_buttons(self, buttons_to_create: list[tuple]) -> None:
        """
        Create the buttons.

        Args:
            buttons_to_create (list[tuple]): The buttons to create, where each item in the list is a tuple like this - ("Play!", self.start_playing).
        """
        curr_y: int = MainMenuConstants.BUTTONS_INITIAL_HEIGHT
        for button_name, button_action in buttons_to_create:
            self.menu_buttons.append(ActionButton(MainMenuConstants.BUTTONS_LEFT_MARGIN, curr_y, 
                MainMenuConstants.BUTTONS_WIDTH, MainMenuConstants.BUTTONS_HEIGHT,
                button_name,click_action=button_action))
            
            curr_y += MainMenuConstants.BUTTONS_WIDTH + MainMenuConstants.BUTTONS_HEIGHT_MARGIN
    

    def start_playing(self):
        self.events_observable.notify_observers(Events.CHANGE_MENU_TO_GAME)
    

    def quit_menu(self):
        self.events_observable.notify_observers(Events.QUIT_MENU)


    def pick_ai(self, ai_name):
        self.events_observable.notify_observers(Events.AI_PICKED, ai_name)


    def unpick_ai(self, ai_name):
        self.events_observable.notify_observers(Events.AI_UNPICKED, ai_name)
    

    def pick_level(self,  level_name):
        self.events_observable.notify_observers(Events.LEVEL_PICKED, level_name)
        

    def unpick_level(self,  level_name):
        self.events_observable.notify_observers(Events.LEVEL_UNPICKED, level_name)


    def handle_display_constants(self):
        DisplayConstants.SCREEN_SIZE = DisplayObjects.screen_size
        DisplayConstants.SCREEN_WIDTH = DisplayObjects.screen_size[0]
        DisplayConstants.SCREEN_HEIGHT = DisplayObjects.screen_size[1]
        DisplayConstants.SCREEN_BIT = int(DisplayConstants.SCREEN_WIDTH * DisplayConstants.SCREEN_BIT)
        

        # Scale everything relative to the screen bits.
        display_constants_to_update = [x for x in dir(DisplayConstants) if ("__" not in x and "SCREEN_" not in x)]
        scoreboard_constants_to_update = [x for x in dir(ScoreboardConstants) if ("__" not in x and "BACKGROUND_COLOR" not in x and "IMAGE_PATH" not in x)]

        self.scale_constants_list(display_constants_to_update, DisplayConstants)
        self.scale_constants_list(scoreboard_constants_to_update, ScoreboardConstants)
        self.scale_constants_list(settings_properties_to_scale, Settings)

        DisplayConstants.SCOREBOARD_SCREEN_HEIGHT = DisplayConstants.SCREEN_HEIGHT - DisplayConstants.FLOOR_Y_VALUE - ScoreboardConstants.SCOREBOARD_HEIGHT_SHIFT
        DisplayConstants.SCOREBOARD_SCREEN_WIDTH = math.floor((DisplayConstants.SCREEN_WIDTH - ScoreboardConstants.SHIFT*2) / Settings.MAX_PLAYERS)
        self.scale_constants_list(design_constants_properties_to_scale, DesignConstants)
        self.scale_constants_list(powerup_constants_to_update, PowerupsSettings)
        self.scale_constants_list(countdown_bar_constants_to_update, CountdownBarConstants)
        self.scale_constants_list(alert_constants_to_update, AlertConstants)
        self.scale_constants_list(main_menu_constants_to_update, MainMenuConstants)

        # Reasign conutdown bar display constants settings.
        CountdownBarConstants.BAR_POSITION = (DisplayConstants.GAME_AREA_POSITION[0], DisplayConstants.FLOOR_Y_VALUE + CountdownBarConstants.COUNTDOWN_SCREEN_MARGIN)
        CountdownBarConstants.BAR_WIDTH = DisplayConstants.RIGHT_BORDER_X_VALUE - DisplayConstants.GAME_AREA_POSITION[0]

        # Reasign alert display constants settings.
        AlertConstants.AlERT_POSITION = ((DisplayConstants.LEFT_BORDER_X_VALUE + DisplayConstants.RIGHT_BORDER_X_VALUE)/DisplayConstants.SCREEN_BIT*2,
                                        (DisplayConstants.CIELING_Y_VALUE + DisplayConstants.FLOOR_Y_VALUE)/DisplayConstants.SCREEN_BIT*2)
        
        # Changing constants after the changes we made.
        DesignConstants.BASE_FONT = pygame.font.SysFont(DesignConstants.BASE_FONT_NAME, DesignConstants.BASE_FONT_SIZE)
        DesignConstants.BIG_FONT = pygame.font.SysFont(DesignConstants.BASE_FONT_NAME, DesignConstants.BIG_FONT_SIZE)
        DesignConstants.MID_FONT = pygame.font.SysFont(DesignConstants.BASE_FONT_NAME, DesignConstants.MID_FONT_SIZE)

        MainMenuConstants.TITLE_FONT = pygame.font.SysFont(MainMenuConstants.TITLE_FONT_NAME, MainMenuConstants.TITLE_FONT_SIZE)
        MainMenuConstants.AIS_TITLE_FONT = pygame.font.SysFont(DesignConstants.BASE_FONT_NAME, DesignConstants.BASE_FONT_SIZE)
        MainMenuConstants.LEVELS_TITLE_FONT = pygame.font.SysFont(DesignConstants.BASE_FONT_NAME, DesignConstants.BASE_FONT_SIZE)

        AlertConstants.ALERT_FONT = pygame.font.SysFont(AlertConstants.ALERT_FONT_NAME, AlertConstants.ALERT_FONT_SIZE)


    def scale_constants_list(self, constants_list, constants_class):
        for constant_name in constants_list:
            constant_value = getattr(constants_class, constant_name)
            if (type(constant_value) == tuple):
                setattr(constants_class, constant_name, 
                (int(constant_value[0] * DisplayConstants.SCREEN_BIT), int(constant_value[1] * DisplayConstants.SCREEN_BIT)))
            else:
                setattr(constants_class, constant_name, int(constant_value * DisplayConstants.SCREEN_BIT))

    
    def draw(self, ais: list[BasePlayer], balls: list[Ball], shots: list[ArrowShot], powerups: list[Powerup], scoreboards: list[AIScoreboard], alert: Alert, countdown_bar: CountdownBar) -> None:
        """
        Draw the game objects.

        Args:
            ais (list[BasePlayer]): The players to draw.
            balls (list[Ball]): The balls to draw.
            shots (list[ArrowShot]): The shots to draw.
            alert (Alert): The alert to draw.
            countdown_bar (CountdownBar): The countdown bar to draw.
        """
        # Clear the screen.
        DisplayObjects.screen.fill((0, 0, 0))

        # Draw background.
        DisplayObjects.screen.blit(Images.general_images["background_image"], DisplayConstants.GAME_AREA_POSITION)
       
        all_items = scoreboards + shots + ais + balls + powerups + [countdown_bar] 

        # Draw the alert
        if alert:
            alert.draw(DisplayObjects.screen)

        # Draw the ais.
        for item in all_items:
            item.draw(DisplayObjects.screen)
            
        # Updating the screen.
        pygame.display.flip()

    def draw_menu(self, ais: list[BasePlayer], levels: list[dict]) -> None:
        """
        Draw the menu.
        """
        
        # Clear the screen.
        DisplayObjects.screen.fill((0, 0, 0))

        # Draw background.
        DisplayObjects.screen.blit(Images.general_images["menu_background_image"], (0,0))

        # Draw title.
        text_surface = MainMenuConstants.TITLE_FONT.render(Settings.TITLE, True, MainMenuConstants.TITLE_COLOR)
        DisplayObjects.screen.blit(text_surface, MainMenuConstants.TITLE_POSITION)

        # Draw buttons titles.
        ais_buttons_text_surface = MainMenuConstants.AIS_TITLE_FONT.render(MainMenuConstants.AIS_TITLE, True, MainMenuConstants.TITLE_COLOR)
        levels_buttons_text_surface = MainMenuConstants.LEVELS_TITLE_FONT.render(MainMenuConstants.LEVELS_TITLE, True, MainMenuConstants.TITLE_COLOR)
        DisplayObjects.screen.blit(ais_buttons_text_surface, MainMenuConstants.AIS_TO_PICK_TITLE_POSITION)
        DisplayObjects.screen.blit(levels_buttons_text_surface, MainMenuConstants.LEVELS_TO_PICK_TITLE_POSITION)

        # Drawing buttons.
        for button in self.menu_buttons + self.ai_buttons + self.levels_buttons:
            button.draw(DisplayObjects.screen)
     
        # Updating the screen.
        pygame.display.flip()


    def get_ai_names(self) -> list[str]:
        ais_names = []
        for file_name in os.listdir(Settings.BASE_AI_DIR):
            # Get the ais files.
            if file_name.endswith(".py"):
                ai_name = file_name.replace(".py", "") # The minus 3 => Removing the .py ending
                ais_names.append(ai_name)

        return ais_names
    

    def get_levels_names(self) -> list[str]:
        levels_names = []
        for level in os.listdir(Settings.LEVELS_DIR):
            if (level.endswith(".json")):
                level_name = level.replace(".json", "")
                levels_names.append(level_name)

        return levels_names
    