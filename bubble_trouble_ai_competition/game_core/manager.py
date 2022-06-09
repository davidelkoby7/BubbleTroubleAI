import os
import importlib

from bubble_trouble_ai_competition.utils.constants import Settings
from bubble_trouble_ai_competition.utils.exceptions import CantLoadBotException

class GameManager:
    """
    Will manage the game objects, main loop and logic.
    """

    def __init__(self, ais_dir_path: str = None, fps: int = Settings.FPS):
        """
        Initializes the game manager.

        Args:
            fps (int): The frames per second to run the game at.
            ais_dir_path (str): The path to the directory containing the ais.
        """
        self.fps = fps
        self.ai_objects = []
        self.ai_classes = []

        if (ais_dir_path != None):
            self.load_ais(ais_dir_path)


    def load_ais(self, ais_dir_path: str):
        """
        Load the ais from the given directory.

        Args:
            ais_dir_path (str): The path to the directory containing the ais.
    
        Raises:
            CantLoadBotException: If a bot can't be loaded.
        """
        self.ai_classes = []

        # Dynamically load the ais from their files.
        for file in os.listdir(ais_dir_path):
            if (file.endswith(".py") and file != "__init__.py"):
                ai_name = file[:-3]
                imported_module = importlib.import_module("ais." + ai_name)
                try:
                    self.ai_classes.append(getattr(imported_module, ai_name + "AI"))
                except:
                    raise CantLoadBotException("Could not load ai class: " + ai_name)

        # Create the ai objects.
        self.ais = [class_ref() for class_ref in self.ai_classes]


    def print_ais(self):
        """
        Calls the AI's talk method.
        Just for testing to see if the ais are loaded correctly.
        """
        for ai in self.ais:
            ai.talk()


