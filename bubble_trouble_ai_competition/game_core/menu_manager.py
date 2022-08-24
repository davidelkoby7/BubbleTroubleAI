import pygame
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable

from bubble_trouble_ai_competition.game_core.graphics import Graphics
from bubble_trouble_ai_competition.utils.constants import Events

class MenuManager:
    def __init__(self, graphics: Graphics, ais: list[BasePlayer], events_observable: EventsObservable):
        self.menu_running = True
        self.graphics = graphics
        self.ais = ais
        self.events_observable = events_observable

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
                    break

                # Handling key presses (only for valid keys, not something like alt etc.).
                if (event.type == pygame.KEYDOWN and event.key < 100):
                    if (event.key == pygame.K_RETURN):
                        self.events_observable.notify_observers(Events.CHANGE_MENU_TO_GAME)
                        continue
                    
                    if (event.key == pygame.K_ESCAPE):
                        self.events_observable.notify_observers(Events.QUIT_MENU)
                        continue
                    
                    key_pressed = chr(event.key)
                    if (not key_pressed.isdigit()):
                        continue

                    key_pressed = int(key_pressed)
                    if (key_pressed > len(self.ais)):
                        continue
                    self.ais[key_pressed - 1].is_competing = not self.ais[key_pressed - 1].is_competing
                    

                    

            # Drawing the menu.
            self.graphics.draw_menu(self.ais)
