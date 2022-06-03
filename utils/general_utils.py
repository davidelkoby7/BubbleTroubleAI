import os
import importlib

def load_bots():
    """
    Loads all bots from the bots folder.
    """
    bots_classes = []
    for file in os.listdir("bots"):
        if (file.endswith(".py") and file != "__init__.py"):
            bot_name = file[:-3]
            imported_module = importlib.import_module("bots." + bot_name)
            bots_classes.append(getattr(imported_module, bot_name + "Bot"))

    # Create bots from classes
    bots = [class_ref() for class_ref in bots_classes]

    return bots
