from bubble_trouble_ai_competition.game_core.manager import GameManager

def main():
    """
    Game starting point.
    """

    gm = GameManager()
    gm.load_ais("./ais")
    gm.print_ais()

if (__name__ == "__main__"):
    main()
