from bubble_trouble_ai_competition.game_core.manager import GameManager

def main():
    """
    Game starting point.
    """

    gm = GameManager(ais_dir_path="./ais")
    gm.start()

if (__name__ == "__main__"):
    main()
