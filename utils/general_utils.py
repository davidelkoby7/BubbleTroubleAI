import os
import importlib

from utils.constants import Settings
from utils.exceptions import CantLoadBotException

def load_ais():
    """
    Loads all ais from the bots folder.

    Returns:
        list[BasePlayer]: A list of all loaded ais.
    
    Raises:
        CantLoadBotException: If a bot can't be loaded.
    """
    ais_classes = []
    for file in os.listdir(Settings.AIS_DIR_PATH):
        if (file.endswith(".py") and file != "__init__.py"):
            ai_name = file[:-3]
            imported_module = importlib.import_module("ais." + ai_name)
            try:
                ais_classes.append(getattr(imported_module, ai_name + "AI"))
            except:
                raise CantLoadBotException("Could not load ai class: " + ai_name)

    # Create bots from classes
    ais = [class_ref() for class_ref in ais_classes]

    return ais
