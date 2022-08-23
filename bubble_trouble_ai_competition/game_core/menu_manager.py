import pygame
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer

from bubble_trouble_ai_competition.game_core.graphics import Graphics

class MenuManager:
    def __init__(self, graphics: Graphics, ais: list[BasePlayer]):
        self.menu_running = True
        self.graphics = graphics
        self.ais = ais

    def run_menu(self) -> None:
        """
        Runs the menu.
        """
        while self.menu_running:
            # Handle events.
            for event in pygame.event.get():
                # If the user wants to force-quit.  
                if (event.type == pygame.QUIT):  
                    self.menu_running = False  
                    break
                
                # If the user clicks the mouse - check for button clicks.
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                    for button in self.graphics.menu_buttons:
                        if ((button.x <= pos[0] <= button.x + button.width) and
                            (button.y <= pos[1] <= button.y + button.height)):
                            button.on_click()
                            print(f"{button.text} clicked")
                    break

                # Handling key presses (only for valid keys, not something like alt etc.).
                if (event.type == pygame.KEYDOWN and event.key < 100):
                    key_pressed = chr(event.key)
                    print(f"NUMEVENTS, {key_pressed=}")

            # Drawing the menu.
            self.graphics.draw_menu(self.ais)
