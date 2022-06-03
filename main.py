from base_objects.base_player import BasePlayer
from utils.constants import Directions
from utils.types import SpeedTypes

def main():
    print("Starting the bubble trouble game!")
    p = BasePlayer("Davidalk", Directions.LEFT, SpeedTypes.NORMAL)
    print (p.direction)

if (__name__ == "__main__"):
    main()
