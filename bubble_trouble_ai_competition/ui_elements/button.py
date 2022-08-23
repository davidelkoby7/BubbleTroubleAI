import pygame

from bubble_trouble_ai_competition.utils.constants import DesignConstants, DisplayConstants


class Button:
    def __init__(self, x, y, width, height, text, text_color: tuple = (0, 0, 0), background_color = (200, 200, 200), on_click = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = DesignConstants.BASE_FONT
        self.text_color = text_color
        self.background_color = background_color
        self.on_click = on_click
    

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, pygame.Rect(self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, False, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width / 2, self.y + self.height / 2)
        screen.blit(text_surface, text_rect)


    def is_clicked(self, mouse_x, mouse_y):
        if mouse_x > self.x and mouse_x < self.x + self.width:
            if mouse_y > self.y and mouse_y < self.y + self.height:
                return True
        return False

