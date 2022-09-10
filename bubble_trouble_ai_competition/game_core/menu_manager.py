from argparse import Action
import os
import pygame
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable

from bubble_trouble_ai_competition.game_core.graphics import Graphics
from bubble_trouble_ai_competition.ui_elements.action_button import ActionButton
from bubble_trouble_ai_competition.ui_elements.pick_button import PickButton
from bubble_trouble_ai_competition.utils.constants import Events, Settings
from bubble_trouble_ai_competition.utils.exceptions import NoLevelsImplemented

class MenuManager:
    def __init__(self, graphics: Graphics, ais: list[BasePlayer], events_observable: EventsObservable):
        """
        Initializes the menu manager.

        Args:
            graphics (Graphics): The graphics object.
            ais (list[BasePlayer]): The list of AI players.
            events_observable (EventsObservable): The events observable.
        """
        self.menu_running = True
        self.graphics = graphics
        self.ais = ais
        self.events_observable = events_observable
        self.levels: list[str] = []
        self.curr_active_level_index: int = 0

        self.load_levels_from_dir()
    
    def load_levels_from_dir(self) -> None:
        """
        Loads the levels from the given directory.
        
        Returns:
            list[str]: The levels files.
        """

        for level in os.listdir(Settings.LEVELS_DIR):
            if (level.endswith(".json")):
                self.levels.append({"name": level[:-5], "active": False}) # The minus 5 => Removing the .json ending
        
        if (len(self.levels) == 0):
            raise NoLevelsImplemented()

        self.levels[self.curr_active_level_index]["active"] = True
    

    def get_curr_level_name(self):
        return self.levels[self.curr_active_level_index]["name"]

    
    def reset_buttons(self):
        """Reset all menu buttons to default."""
        for button in self.graphics.menu_buttons:
            button.can_action = False

        for button in self.graphics.ai_buttons + self.graphics.levels_buttons:
            button.clicked = False
        
        # first level will be default picked.
        self.graphics.levels_buttons[0].clicked = True
       


    def run_menu(self) -> None:
        """
        Runs the menu.
        """
        self.reset_buttons()
        while self.menu_running:
            

            # Handle events.
            for event in pygame.event.get():
                # If the user wants to force-quit.  
                if (event.type == pygame.QUIT):  
                    self.menu_running = False  
                    break
                
                # If the user clicks the mouse - check for button clicks.
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()
                    for button in self.graphics.menu_buttons+self.graphics.ai_buttons+self.graphics.levels_buttons:
                        if (button.is_clicked(mouse_x, mouse_y)):
                            if isinstance(button, PickButton):
                                self.events_observable.notify_observers(Events.PICK_BUTTON_CLICKED, button)
                            if isinstance(button, ActionButton):
                                self.events_observable.notify_observers(Events.ACTION_BUTTON_CLICKED, button)
                            break
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
                    if (not key_pressed.isdigit() and not key_pressed.isalpha()):
                        continue

                    if (not key_pressed.isdigit()):
                        key_pressed = key_pressed.upper()
                        index = ord(key_pressed) - ord("A")
                        if (index >= len(self.levels)):
                            continue
                        
                        self.levels[self.curr_active_level_index]["active"] = False
                        self.curr_active_level_index = index
                        self.levels[index]["active"] = True
                        continue

                    key_pressed = int(key_pressed)
                    
            
            # Drawing the menu.
            for button in self.graphics.menu_buttons + self.graphics.ai_buttons + self.graphics.levels_buttons:
                button.update()
            self.graphics.draw_menu(self.ais, self.levels)
