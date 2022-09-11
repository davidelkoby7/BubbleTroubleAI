from tkinter import Button
import pygame

from bubble_trouble_ai_competition.utils.constants import DesignConstants, DisplayConstants, Settings, MainMenuConstants
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image
from bubble_trouble_ai_competition.utils.load_display import DisplayObjects
from bubble_trouble_ai_competition.ui_elements.button import Button


class ActionButton(Button):
    """
    Class representing a clickable button.
    Handles both UI & click events.
    """
    def __init__(self, x: int, y: int, width: int, height: int, text: str, text_color: tuple =  MainMenuConstants.BUTTONS_FONT_COLOR, click_action = None):
        """
        Initializes a button.

        Args:
            x (int): The x-coordinate of the button.
            y (int): The y-coordinate of the button.
            width (int): The width of the button.
            height (int): The height of the button.
            text (str): The text of the button.
            text_color (tuple): The color of the text.
            background_color (tuple): The color of the button.
            on_click (function): The function to be called when the button is clicked.
        """
        super().__init__(x, y, width, height, text, text_color)
        self.click_action = click_action
        self.font_size = "BIG_FONT"
        self.button_image_path = Settings.button_IMAGE_PATH
        self.button_image_width = self.width
        self.button_image_height = self.height
        self.clicked = False
        self.can_action = False


    def draw(self, screen: pygame.Surface):
        """
        Draws the button.

        Args:
            screen (pygame.Surface): The surface to draw the button on.
        """

        text_surface, text_rect = self.create_button_text()
        self.button_image_width = self.width
        self.button_image_height = self.width
       
        text_rect.center = (self.x + self.button_image_width / 2, self.y + self.button_image_height / 2)
        bottom_image = load_and_scale_image(self.button_image_path, self.button_image_width, self.button_image_height)  
        screen.blit(bottom_image, (self.x, self.y))
        screen.blit(text_surface, text_rect)

