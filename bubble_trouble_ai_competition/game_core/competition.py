
import importlib
import os
from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable
from bubble_trouble_ai_competition.game_core.game_manager import GameManager
from bubble_trouble_ai_competition.game_core.graphics import Graphics
from bubble_trouble_ai_competition.game_core.menu_manager import MenuManager
from bubble_trouble_ai_competition.utils.constants import Events, GameStates
from bubble_trouble_ai_competition.utils.exceptions import CantLoadBotException


class Competition:
    def __init__(self, ais_dir_path: str, start: bool = True):
        # Initializing values
        self.game_running = True
        self.curr_state: GameStates = GameStates.MAIN_MENU

        # Dynamically loading the ais classes
        self.ais_dir_path = ais_dir_path

        self.graphics: Graphics = None
        self.ais: list[BasePlayer] = []

        self.load_observable()

        self.graphics = Graphics(self.event_observable)

        self.game_manager: GameManager = None
        self.menu_manager: MenuManager = None
        self.generate_menu_manager()
        self.generate_game_manager()
        

        if (start == True):
            self.start()


    def load_observable(self):
        # Listening to relevant events that can change the game's state
        self.event_observable: EventsObservable = EventsObservable()
        self.event_observable.add_observer(Events.CHANGE_MENU_TO_GAME, self.run_game)
        self.event_observable.add_observer(Events.CHANGE_GAME_TO_MENU, self.go_to_menu)
        self.event_observable.add_observer(Events.QUIT_MENU, self.quit_game)
        
        if (self.graphics != None):
            self.graphics.events_observable = self.event_observable
        
        if (self.ais != []):
            for ai in self.ais:
                ai.events_observable = self.event_observable


    def load_ais(self) -> None:
        """
        Load the ais from the given directory.
    
        Raises:
            CantLoadBotException: If a bot can't be loaded.
        """
        self.ai_classes = []

        # Dynamically load the ais from their files.
        for file in os.listdir(self.ais_dir_path):
            if (file.endswith(".py") and file != "__init__.py"):
                ai_name = file[:-3] # The minus 3 => Removing the .py ending
                imported_module = importlib.import_module("ais." + ai_name)
                try:
                    self.ai_classes.append(getattr(imported_module, ai_name + "AI"))
                except:
                    raise CantLoadBotException("Could not load ai class: " + ai_name)

        # Create the ai objects.
        self.instanciate_ais()


    def instanciate_ais(self):
        self.ais: list[BasePlayer] = [class_ref(events_observable = self.event_observable, ais_dir_path = self.ais_dir_path) for class_ref in self.ai_classes]

    
    def quit_game(self):
        self.menu_manager.menu_running = False
        self.game_manager.game_over = True

    
    def is_running(self):
        return ((self.game_manager == None or self.game_manager.game_over == False) or self.menu_manager.menu_running == True)


    def start(self):
        while (self.is_running()):
            if (self.curr_state == GameStates.MAIN_MENU):
                self.menu_manager.run_menu()
            if (self.curr_state == GameStates.PLAYING):
                print ("Running a game!")
                self.game_manager.run_game()
    

    def run_game(self):
        self.curr_state = GameStates.PLAYING
        self.menu_manager.menu_running = False
        self.generate_game_manager()


    def go_to_menu(self):
        print ('Going to ment')
        self.curr_state = GameStates.MAIN_MENU
        self.game_manager.game_over = True
        self.generate_menu_manager()
    

    def generate_menu_manager(self):
        self.load_ais()
        self.menu_manager = MenuManager(self.graphics, self.ais)


    def generate_game_manager(self):
        self.load_observable()

        self.game_manager = GameManager(self.ais_dir_path, self.ais, self.event_observable, self.graphics)
