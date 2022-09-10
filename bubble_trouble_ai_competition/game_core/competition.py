
import importlib
import os
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.game_core import graphics
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.game_core.game_manager import GameManager
from bubble_trouble_ai_competition.game_core.graphics import Graphics
from bubble_trouble_ai_competition.game_core.menu_manager import MenuManager
from bubble_trouble_ai_competition.ui_elements.action_button import ActionButton
from bubble_trouble_ai_competition.ui_elements.pick_button import PickButton
from bubble_trouble_ai_competition.utils.constants import Events, GameStates, MainMenuConstants, Settings
from bubble_trouble_ai_competition.utils.exceptions import CantLoadBotException


class Competition:
    def __init__(self, ais_dir_path: str, start: bool = True):
        """
        Initializes the competition.
        
        Args:
            ais_dir_path (str): The path to the directory containing the ais files.
            start (bool): Whether to start the competition immediately or not. By default - True.
        """
        # Initializing values
        self.game_running = True
        self.curr_state: GameStates = GameStates.MAIN_MENU

        # Dynamically loading the ais classes
        self.ais_dir_path = ais_dir_path

        self.graphics: Graphics = None
        self.ais: list[BasePlayer] = []
        self.ais_competting: list[BasePlayer] = []

        self.load_observable()

        self.graphics = Graphics(self.event_observable)

        self.game_manager: GameManager = None
        self.menu_manager: MenuManager = None
        self.generate_menu_manager()
        self.generate_game_manager()

        if (start == True):
            self.start()
        

    def load_observable(self):
        """
        Loads a new instance of the observable class (when we reset a game for example).
        """
        # Listening to relevant events that can change the game's state
        self.event_observable: EventsObservable = EventsObservable()
        self.event_observable.add_observer(Events.CHANGE_MENU_TO_GAME, self.run_game)
        self.event_observable.add_observer(Events.CHANGE_GAME_TO_MENU, self.go_to_menu)
        self.event_observable.add_observer(Events.QUIT_MENU, self.quit_game)
        self.event_observable.add_observer(Events.ACTION_BUTTON_CLICKED, self.on_action_button_clicked)
        self.event_observable.add_observer(Events.PICK_BUTTON_CLICKED, self.on_pick_button_clicked)
        self.event_observable.add_observer(Events.AI_PICKED, self.on_ai_picked)
        self.event_observable.add_observer(Events.AI_UNPICKED, self.on_ai_unpicked)
        self.event_observable.add_observer(Events.LEVEL_PICKED, self.on_level_picked)
        self.event_observable.add_observer(Events.LEVEL_UNPICKED, self.on_level_unpicked)
        
        if (self.graphics != None):
            self.graphics.events_observable = self.event_observable
        
        if (self.ais != []):
            for ai in self.ais:
                ai.events_observable = self.event_observable


    def ais_competing_amount(self):
        """Returns the number of ais competing at game."""
        return len([ai for ai in self.ais if ai.is_competing == True])


    def on_action_button_clicked(self, button: ActionButton):
        """Make sure action's button have all the needed condition for action and perform it."""

        # Check if button is a play button.
        if button.click_action == self.graphics.start_playing:
            if self.ais_competing_amount() >= 1:
                button.can_action = True
        
        # Check if button is a exit button
        elif button.click_action == self.graphics.quit_menu:
            button.can_action = True
        
        # Check if button can preform action.
        if button.can_action:

            # Perform button's action.
            button.click_action()


    def on_pick_button_clicked(self, button: PickButton):
        """Performs the pick and unpick actions of button."""

        if not button.clicked:
            # button is picked
            button.on_pick(button.text)
        
        if button.clicked:
            # button is unpicked.
            button.on_unpick(button.text)
        
        button.clicked = not button.clicked

    def load_ais(self) -> None:
        """
        Load the ais from the given directory.
    
        Raises:
            CantLoadBotException: If a bot can't be loaded.
        """
        self.ai_classes = []
        # Dynamically load the ais from their files.
        for file_name in os.listdir(self.ais_dir_path):
            if (file_name.endswith(".py") and file_name != "__init__.py"):
                ai_name = file_name[:-3] # The minus 3 => Removing the .py ending
                imported_module = importlib.import_module("ais." + ai_name)
                try:
                    self.ai_classes.append(getattr(imported_module, ai_name + "AI"))
                except:
                    raise CantLoadBotException("Could not load ai class: " + ai_name)

        # Create the ai objects.
        self.instanciate_ais()


    def instanciate_ais(self):
        """
        Creates objects for each of the AIs classes from the self.ai_classes property, and stores it in self.ais.
        """
        self.ais: list[BasePlayer] = [class_ref(events_observable = self.event_observable, ais_dir_path = self.ais_dir_path) for class_ref in self.ai_classes]

    
    def quit_game(self):
        """
        Quits the game (both menu and game).
        """
        self.menu_manager.menu_running = False
        self.game_manager.game_over = True

    
    def is_running(self):
        """
        Returns whether the game is still running or not (either menu or the actual game).

        Returns:
            bool: True if the game is still running, False otherwise.
        """
        return (self.game_manager.game_over == False or self.menu_manager.menu_running == True)


    def start(self):
        """
        Starts the game, and runs the game itself or the menu, depending on it's state.
        """
        while (self.is_running()):
            if (self.curr_state == GameStates.MAIN_MENU):
                self.menu_manager.run_menu()
            if (self.curr_state == GameStates.PLAYING):
                self.game_manager.run_game()
    

    def run_game(self):
        """
        Runs the game itself.
        """
        self.menu_manager.menu_running = False
        self.curr_state = GameStates.PLAYING
        self.generate_game_manager()
    

    def on_ai_picked(self, ai_name):
        [setattr(ai, "is_competing", True) for ai in self.ais if ai.name == ai_name]


    def on_ai_unpicked(self, ai_name):
        [setattr(ai, "is_competing", False) for ai in self.ais if ai.name == ai_name]


    def on_level_picked(self, level_name):
        """Picked only the request level, one level at a time."""
        curr_level_name = self.menu_manager.get_curr_level_name()
        curr_level_button = self.get_level_button_by_name(curr_level_name)
        curr_level_button.clicked = False
        for level in self.menu_manager.levels:
            if level["name"] == level_name:
                self.menu_manager.curr_active_level_index = self.menu_manager.levels.index(level)


    def on_level_unpicked(self, level_name):
        # Pick the default level.
        self.menu_manager.curr_active_level_index = MainMenuConstants.DEFAULT_LEVEL_INDEX
        default_level_name = self.menu_manager.levels[MainMenuConstants.DEFAULT_LEVEL_INDEX]["name"]
        if default_level_name != level_name:
            # Change selection for the default value.
            default_level_button = self.get_level_button_by_name(default_level_name)
            default_level_button.on_pick(default_level_name)
            default_level_button.clicked = True
        else:

            # Save the selection at the default level
            self.get_level_button_by_name(level_name).clicked = False



    def get_level_button_by_name(self, level_name) -> PickButton:
        for button in self.graphics.levels_buttons:
            if button.text == level_name:
                return button
        
        return None


    def go_to_menu(self):
        """
        Goes back to the menu.
        """
        self.curr_state = GameStates.MAIN_MENU
        self.game_manager.game_over = True
        self.generate_menu_manager()
    

    def generate_menu_manager(self):
        """
        Generates the menu manager.
        """
        self.load_ais()
        self.menu_manager = MenuManager(self.graphics, self.ais, self.event_observable)


    def generate_game_manager(self):
        """
        Generates the game manager.
        """
        self.load_observable()
        level_to_run = self.menu_manager.levels[self.menu_manager.curr_active_level_index]["name"]
        self.game_manager = GameManager(self.ais_dir_path, self.ais, self.event_observable, self.graphics, Settings.LEVELS_DIR + level_to_run + ".json")
