import pygame

from bubble_trouble_ai_competition.utils.constants import DesignConstants, DisplayConstants, MainMenuConstants, Settings
from bubble_trouble_ai_competition.utils.general_utils import load_and_scale_image
from bubble_trouble_ai_competition.utils.load_display import DisplayObjects


class Button:
    """
    Class representing a clickable button.
    Handles both UI & click events.
    """
    def __init__(self, x: int, y: int, width: int, height: int, text: str, text_color: tuple =  MainMenuConstants.BUTTONS_FONT_COLOR):
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
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.font_size = "BIG_FONT"
        self.button_image_path = Settings.button_IMAGE_PATH
        self.button_image_width = self.width
        self.button_image_height = self.height
        self.clicked = False

    def create_button_text(self):
      
        text_surface = getattr(DesignConstants, self.font_size).render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        return text_surface, text_rect


    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        """
        Draws the button.

        Args:
            screen (pygame.Surface): The surface to draw the button on.
        """

        text_surface, text_rect = self.create_button_text()
        text_rect.center = (self.x + self.button_image_width / 2, self.y + self.button_image_height / 2)
        bottom_image = load_and_scale_image(self.button_image_path, self.button_image_width, self.button_image_height)  
        screen.blit(bottom_image, (self.x, self.y))
        screen.blit(text_surface, text_rect)


    def is_clicked(self, mouse_x: int, mouse_y: int):
        """
        Checks if the button is clicked.

        Args:
            mouse_x (int): The x-coordinate of the mouse.
            mouse_y (int): The y-coordinate of the mouse.
        
        Returns:
            bool: True if the button is clicked (meaning - the mouse_x and mouse_y are in the button's rectangle), False otherwise.
        """
        return self.x < mouse_x < self.x + self.button_image_width and self.y < mouse_y < self.y + self.button_image_height
