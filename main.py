import pygame

from utils.general_utils import load_bots

def main():
    """
    Main game function.
    """

    bots = load_bots()
    
    # Make the bots talk
    for bot in bots:
        bot.talk()

if (__name__ == "__main__"):
    main()
