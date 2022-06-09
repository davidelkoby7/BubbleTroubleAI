import pygame

from utils.general_utils import load_ais

def main():
    """
    Game starting point.
    """

    ais = load_ais()
    
    # Make the bots talk
    for ai in ais:
        ai.talk()

if (__name__ == "__main__"):
    main()
