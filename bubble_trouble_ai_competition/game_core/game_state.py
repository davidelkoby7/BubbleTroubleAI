
import pickle
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    # avoiding import cyclic error
    from bubble_trouble_ai_competition.base_objects.base_player import BasePlayer
    from bubble_trouble_ai_competition.base_objects.arrow_shot import ArrowShot
    from bubble_trouble_ai_competition.base_objects.base_ball import Ball
    from bubble_trouble_ai_competition.base_objects.base_powerup import Powerup

from bubble_trouble_ai_competition.utils.constants import Settings



class GameState:
    """ Save the current frame's game state."""

    __ais__ : list['BasePlayer'] = []
    __shoots__: list['ArrowShot'] = []
    __balls__: list['Ball'] = []
    __powerups__:list['Powerup'] = []
    __frames_remaining__ : int = Settings.TOTAL_GAME_FRAMES


def update_game_state(ais: list['BasePlayer'], shoots:list['ArrowShot'], balls: list['Ball'], powerups: list['Powerup'], frames_remaining: int) -> None:
    GameState.__ais__ = pickle.loads(pickle.dumps(ais))
    GameState.__shoots__ = pickle.loads(pickle.dumps(shoots))
    GameState.__balls__ = pickle.loads(pickle.dumps(balls))
    GameState.__powerups__ = pickle.loads(pickle.dumps(powerups))
    GameState.__frames_remaining__ = frames_remaining


def game_ais() -> list['BasePlayer']:
    """returns list of ais playing at the current game frame."""
    return pickle.loads(pickle.dumps(GameState.__ais__))


def game_powerups() -> list['Powerup']:
    """returns list of the all powerups in game at the current game frame."""
    return pickle.loads(pickle.dumps(GameState.__powerups__))


def game_shoots() -> list['ArrowShot']:
    """returns list of the active shoots at the current game frame."""
    return pickle.loads(pickle.dumps(GameState.__shoots__))


def game_balls() -> list['Ball']:
    """returns list of the active balls at the current game frame."""
    return pickle.loads(pickle.dumps(GameState.__balls__))


def game_frames_remaining() -> int:
    """returns the frame remaining for the game at the current game frame."""
    return GameState.__frames_remaining__