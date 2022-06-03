from utils.constants import Directions
from base_objects.base_player import BasePlayer

class tehilaBot(BasePlayer):
    def __init__(self) -> None:
        """
        Constructs a base player AI.
        """
        super().__init__("tehila", Directions.RIGHT)
    