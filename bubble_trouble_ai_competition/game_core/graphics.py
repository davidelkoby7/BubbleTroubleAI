import pygame
from bubble_trouble_ai_competition.base_objects.arrow_shot import ArrowShot
from bubble_trouble_ai_competition.base_objects.base_ball import Ball

from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup
from bubble_trouble_ai_competition.base_objects.countdown_bar import CountdownBar
from bubble_trouble_ai_competition.ui_elements.ai_scoreboard import AIScoreboard
from bubble_trouble_ai_competition.utils.constants import CountdownBarConstans,DesignConstants, DisplayConstants, PowerupsSettings, ScoreboardConstants, Settings, settings_properties_to_scale, design_constants_properties_to_scale, powerup_constants_to_update, countdown_bar_constants_to_update
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image

class Graphics:
    """
    Will handle the graphics.
    """
    
    def __init__(self):
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

        self.game_area_size = DisplayConstants.GAME_AREA_SIZE
        self.game_area_width = self.game_area_size[0]
        self.game_area_height = self.game_area_size[1]

        self.game_area_position = DisplayConstants.GAME_AREA_POSITION

        # Loading the background image. 
        self.background_image = load_and_scale_image(Settings.BACKGROUND_IMAGE_PATH, self.game_area_width, self.game_area_height)
    
        
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
        self.scale_constants_list(countdown_bar_constants_to_update, CountdownBarConstans)

         # Reasign conutdown bar display settings.
        CountdownBarConstans.BAR_POSITION = (DisplayConstants.GAME_AREA_POSITION[0], DisplayConstants.FLOOR_Y_VALUE + 1)
        CountdownBarConstans.BAR_WIDTH = DisplayConstants.RIGHT_BORDER_X_VALUE - DisplayConstants.GAME_AREA_POSITION[0]


        
        # Changing constants after the changes we made.
        DesignConstants.BASE_FONT = pygame.font.SysFont(DesignConstants.BASE_FONT_NAME, DesignConstants.BASE_FONT_SIZE)


    def scale_constants_list(self, constants_list, constants_class):
        for constant_name in constants_list:
            constant_value = getattr(constants_class, constant_name)
            if (type(constant_value) == tuple):
                setattr(constants_class, constant_name, 
                (int(constant_value[0] * DisplayConstants.SCREEN_BIT), int(constant_value[1] * DisplayConstants.SCREEN_BIT)))
            else:
                setattr(constants_class, constant_name, int(constant_value * DisplayConstants.SCREEN_BIT))

    
    def draw(self, ais: list[BasePlayer], balls: list[Ball], shots: list[ArrowShot], powerups: list[Powerup], scoreboards: list[AIScoreboard], countdown_bar: CountdownBar) -> None:
        """
        Draw the game objects.

        Args:
            ais (list[BasePlayer]): The players to draw.
            balls (list[Ball]): The balls to draw.
            shots (list[ArrowShot]): The shots to draw.
        """
        # Clear the screen.
        self.screen.fill((0, 0, 0))

        # Draw background.
        self.screen.blit(self.background_image, DisplayConstants.GAME_AREA_POSITION)
       
        all_items = scoreboards + shots + ais + balls + powerups + [countdown_bar]

        # Draw the ais.
        for item in all_items:
            item.draw(self.screen)
    
        # Updating the screen.
        pygame.display.flip()

    def draw_text_msg(self, msg: str):
        # Drawing the background of the text box
        font = pygame.font.Font('freesansbold.ttf', 32)
        x_middle = (DisplayConstants.LEFT_BORDER_X_VALUE + DisplayConstants.RIGHT_BORDER_X_VALUE) / 2
        y_middle = (DisplayConstants.CIELING_Y_VALUE + DisplayConstants.FLOOR_Y_VALUE) / 2
        pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x_middle,y_middle, 300, 80), border_radius=20)
        # Writing the relevant text.
        text_surface = font.render(msg, False, (255,48,48))
        self.screen.blit(text_surface, (x_middle+30, y_middle+30))
        pygame.display.flip()
  
