import pygame

from bubble_trouble_ai_competition.utils.constants import DesignConstants, DisplayConstants


class Button:
    """
    Class representing a clickable button.
    Handles both UI & click events.
    """
    def __init__(self, x: int, y: int, width: int, height: int, text: str, text_color: tuple = (0, 0, 0), background_color = (200, 200, 200), on_click = None):
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
        self.font = DesignConstants.BASE_FONT
        self.text_color = text_color
        self.background_color = background_color
        self.on_click = on_click
    

    def draw(self, screen: pygame.Surface):
        """
        Draws the button.

        Args:
            screen (pygame.Surface): The surface to draw the button on.
        """
        pygame.draw.rect(screen, self.background_color, pygame.Rect(self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, False, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width / 2, self.y + self.height / 2)
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
        return self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height
