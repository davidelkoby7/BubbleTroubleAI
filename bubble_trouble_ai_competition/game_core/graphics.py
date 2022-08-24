import pygame
from bubble_trouble_ai_competition.base_objects.arrow_shot import ArrowShot
from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.base_objects.base_alert import Alert
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.base_objects.countdown_bar import CountdownBar
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.ui_elements.ai_scoreboard import AIScoreboard
from bubble_trouble_ai_competition.ui_elements.button import Button
from bubble_trouble_ai_competition.utils.constants import AlertConstants, CountdownBarConstants, DesignConstants, DisplayConstants, Events, MainMenuConstants, PowerupsSettings, ScoreboardConstants, Settings, settings_properties_to_scale, design_constants_properties_to_scale, powerup_constants_to_update, countdown_bar_constants_to_update, alert_constants_to_update, main_menu_constants_to_update
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image

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
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.screen_size = self.screen.get_size()
        self.screen_width = self.screen_size[0]
        self.screen_height = self.screen_size[1]

        self.handle_display_constants()

        # Store initial values.

        self.events_observable = events_observable

        self.game_area_size = DisplayConstants.GAME_AREA_SIZE
        self.game_area_width = self.game_area_size[0]
        self.game_area_height = self.game_area_size[1]

        self.game_area_position = DisplayConstants.GAME_AREA_POSITION

        # Loading the background image. 
        self.background_image = load_and_scale_image(Settings.BACKGROUND_IMAGE_PATH, self.game_area_width, self.game_area_height)
        self.menu_background_image = load_and_scale_image(Settings.MENU_BACKGROUND_IMAGE_PATH, self.screen_width, self.screen_height)

        # Initializing buttons
        buttons_to_create = [("Play!", self.start_playing), ("Exit", self.quit_menu)]
        self.menu_buttons: list[Button] = []
        self.create_buttons(buttons_to_create)


    def create_buttons(self, buttons_to_create: list[tuple]) -> None:
        """
        Create the buttons.

        Args:
            buttons_to_create (list[tuple]): The buttons to create, where each item in the list is a tuple like this - ("Play!", self.start_playing).
        """
        curr_y: int = MainMenuConstants.BUTTONS_INITIAL_HEIGHT
        for button_name, button_action in buttons_to_create:
            self.menu_buttons.append(Button(MainMenuConstants.BUTTONS_LEFT_MARGIN, curr_y, 
                MainMenuConstants.BUTTONS_WIDTH, MainMenuConstants.BUTTONS_HEIGHT,
                button_name, on_click=button_action))
            
            curr_y += MainMenuConstants.BUTTONS_HEIGHT + MainMenuConstants.BUTTONS_HEIGHT_MARGIN
    

    def start_playing(self):
        self.events_observable.notify_observers(Events.CHANGE_MENU_TO_GAME)
    

    def quit_menu(self):
        self.events_observable.notify_observers(Events.QUIT_MENU)

        
    def handle_display_constants(self):
        DisplayConstants.SCREEN_SIZE = self.screen_size
        DisplayConstants.SCREEN_WIDTH = self.screen_width
        DisplayConstants.SCREEN_HEIGHT = self.screen_height
        DisplayConstants.SCREEN_BIT = int(DisplayConstants.SCREEN_WIDTH * DisplayConstants.SCREEN_BIT)

        # Scale everything relative to the screen bits.
        display_constants_to_update = [x for x in dir(DisplayConstants) if ("__" not in x and "SCREEN_" not in x)]
        scoreboard_constants_to_update = [x for x in dir(ScoreboardConstants) if ("__" not in x and "BACKGROUND_COLOR" not in x)]

        self.scale_constants_list(display_constants_to_update, DisplayConstants)
        self.scale_constants_list(scoreboard_constants_to_update, ScoreboardConstants)
        self.scale_constants_list(settings_properties_to_scale, Settings)
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
        MainMenuConstants.TITLE_FONT = pygame.font.SysFont(DesignConstants.BASE_FONT_NAME, MainMenuConstants.TITLE_FONT_SIZE)
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
        self.screen.fill((0, 0, 0))

        # Draw background.
        self.screen.blit(self.background_image, DisplayConstants.GAME_AREA_POSITION)
       
        all_items = scoreboards + shots + ais + balls + powerups + [countdown_bar]

        # Draw the ais.
        for item in all_items:
            item.draw(self.screen)

        if alert:
            alert.draw(self.screen)
            
        # Updating the screen.
        pygame.display.flip()

    def draw_menu(self, ais: list[BasePlayer]) -> None:
        """
        Draw the menu.
        """

        # Clear the screen.
        self.screen.fill((0, 0, 0))

        # Draw background.
        self.screen.blit(self.menu_background_image, (0,0))

        # Draw title.
        text_surface = MainMenuConstants.TITLE_FONT.render(Settings.TITLE, False, MainMenuConstants.TITLE_COLOR)
        self.screen.blit(text_surface, MainMenuConstants.TITLE_POSITION)

        # Drawing buttons.
        for button in self.menu_buttons:
            button.draw(self.screen)

        # Draw the ais that can be played.
        curr_y: int = MainMenuConstants.AIS_INITIAL_HEIGHT
        for i, ai in enumerate(ais):
            color = (255, 0, 0)
            if (ai.is_competing):
                color = (0, 255, 0)
            text_surface = DesignConstants.BASE_FONT.render(f'#{i + 1}: {ai.name}', False, color)
            self.screen.blit(text_surface, (MainMenuConstants.AIS_LEFT_MARGIN, curr_y))
            curr_y += MainMenuConstants.AIS_HEIGHT_MARGIN

        # Updating the screen.
        pygame.display.flip()
