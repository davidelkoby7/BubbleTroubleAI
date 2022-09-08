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


def update_game_state(ais: list['BasePlayer'], shoots:list['ArrowShot'], balls: list['Ball'], powerups: list['Powerup'], activated_powerups: list['Powerup'], frames_remaining: int) -> None:
    GameState.__ais__ = ais
    GameState.__shoots__ = shoots
    GameState.__balls__ = balls
    GameState.__powerups__ = powerups
    GameState.__activated_powerups__ = activated_powerups
    GameState.__frames_remaining__ = frames_remaining


def game_ais() -> list['BasePlayer']:
    """returns list of ais playing at the current game frame."""
    return GameState.__ais__


def game_powerups() -> list['Powerup']:
    """returns list of the all powerups in game at the current game frame."""
    return GameState.__powerups__


def game_activated_powerups() -> list['Powerup']:
    """returns list of the all activated powerups in game at the current game frame."""
    return GameState.__activated_powerups__




def game_active_powerups() -> list['Powerup']:
    return [powerup for powerup in game_powerups() if powerup.player]


def game_shoots() -> list['ArrowShot']:
    """returns list of the active shoots at the current game frame."""
    return GameState.__shoots__


def game_balls() -> list['Ball']:
    """returns list of the active balls at the current game frame."""
    return GameState.__balls__


def game_frames_remaining() -> int:
    """returns the frame remaining for the game at the current game frame."""
    return GameState.__frames_remaining__