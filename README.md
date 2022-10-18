# BubbleTroubleAI
Bubble trouble game AI Competition framework.

## Installation
Run `python -m pip install -r .\requirements.txt`.

## Creators
Made by Davidalk, Tehila & Hadar.

## The Game

## Powerups
The game have special powerups for the game's players which players can pick during the game. The powerups timing and place picked ranomly during the game.
The available powerups:
- FreezePowerup - player who have active freeze powerup can freeze another player that will be freeze during the powerup's left active duration. (see more about this at the Getting Started section)
- PunchPowerup - player can use his left and right punch during the powerup's active duration if punch collides player, it will move player from his place to the punch direction (if player at (x,y) get punched from left - player will be moved to (x-HIT_RADIUS,y) and from right will be moved to (x+HIT_RADIUS,y) ).
- TeleportPowerup - player can teleport to another place in the area game during the powerup's active duration. (see more about this at the Getting Started section)
- ShieldPowerup - player will be protect by shield from ball's hits during the powerup's active duration. if player with shield will be punched, the shield will popped and it will deactivated player's shield powerup.
- PlayerDoublePointsPowerup - double points for each ball that player popped during the powerup's active duration.
- PlayerSpeedBoosterPowerup - boost player's speed during the powerup's active duration.
- PlayerSpeedSlowerPowerup - slow player's speed during the powerup's active duration.

NOTES: 
- player can have multiple active diffrenence powerups at once (except PlayerSpeedBoosterPowerup and PlayerSpeedSlowerPowerup that cancels each other action, the action powerup that will be active is the last one to pick).
- player can have multiple active powerups with the same powerup type except the special powerups: FreezePowerup, TeleportPowerup, PlayerSpeedBoosterPowerup.


## Levels


## Players
- Manual - manual player that his move and action made by pressed keyboard keys.
- Manual's movement keys:
return Direction.LEFT - left key
return Direction.RIGHT - right key
return Direction.DUCK - down key
return Direction.STAND - if either then the other's key direction is not pressed.
- Manual's available actions:
self.shoot() - space key
self.do_teleport - q key
self.do_freeze() - 1 key
self.do_left_punch - left_ctrl key
self.do_right_punch - right_ctrl key

- ManualWASD
ManualWASD's movement keys:
return Direction.LEFT - a key
return Direction.RIGHT - d key
return Direction.DUCK - s key
return Direction.STAND - if either then the other's key direction is not pressed.

ManualWASD's available actions:
self.shoot() - w key

# Getting Started - Writing your own AI
The ais bots in the game need to follow for the next condition:
1. each ai must have an .py file and directory with the ai images under /ais directory in the next format: my_ai_name.py(file), my_ai_name_images(dir). player's name must be no longer then 11 letters! 
2. How to Write the my_ai_name.py file:

  ## Methods That Player MUST IMPLEMENT:
  - pick_direction() -  The main function where you decide what to do and what to action duraing the game.
    you MUST *return* a value of which direction to go.
    This can be one of the following:
    return Directions.STAND - player will stand.
    return Directions.DUCK - player will duck.
    return Directions.LEFT - player will go left.
    return Directions.RIGHT - player will go right.
    
    In addition to the ai movment and the return direction's value, you can call the following actions:
       ** The powerups actions will be execuate only in player have the relevent active powerup. **

    self.shoot() - to shoot an arrow.
    self.do_teleport() - to teleport (TeleportPowerup's action). 
    self.do_freeze() - to freeze other player (FreezePowerup's action).
    self.do_right_punch() - to do right punch (PunchPowerup's action).
    self.do_left_punch() - to do left punch (PunchPowerup's action).

  ## Methods and Attribute Player can Override (optional but VERY recommanded for some spice):
  - pick_x_to_teleport() - pick x coordinate to move your player while having active teleport powerup. if not override, will implement the method `pick_x_to_teleport()` from /base_objects/base_player.py and chose x randomly.
  - pick_player_to_freeze() - pick player to freeze while having active freeze powerup. if you dont override this method, it will implement  the method from /base_objects/base_player.py and pick player randomly from all avialable players in the game.
  - self.color - pick the player's avilable arrow color. if not set any - will pick color randomly.

  
## Useful utils, functions and tips for writing your BEST AI.

 1. Access game objects that update with each game frame update - from bubble_trouble_ai_competition.game_core.game_state you can import and use the return values of these following functions: 
  - game_ais() - returns list of ais playing at the current game frame
  - game_powerups() - returns list of the all powerups in game (picked and not picked) at the current game frame
  - game_activated_powerups() - returns list of the all activated powerups in game at the current game frame
  - game_shoots() - returns list of the active shoots at the current game frame
  - game_balls() - returns list of the active balls at the current game frame
  - game_frames_remaining() - returns the frame remaining for the game at the current game frame

2. Level up your ai with usefull utils - from utils.general_utils you can import and use these following functions:
- get_closest_player(player: 'BasePlayer', players: List['BasePlayer']) - Returns the closest player to the player (SEE THE ATTENTION NOTE).
- get_closest_ball(player: 'BasePlayer') - Returns the closest ball to the player (SEE THE ATTENTION NOTE).
- player_to_ball_distance(player: 'BasePlayer', ball: 'Ball') - return distance between player to ball 
- distance(point1: tuple, point2: tuple) - Calculates the distance between two points
- circles_collide(...) - Checks if two circles collide
- rect_collide(...) - Checks if two rectangles collide
- circle_rect_collide(...) - Checks if a circle collides with a rectangle

ATTENTION: be careful when using the functions : get_closest_player(), get_closest_ball(), can return None value and if you dont handle it currectly in your bot it will crash the game.

3. Combine and build your ai actions with use of the game's constans variables - from utils.constants you can import static classes that contains some usefull constants such as: 
DisplayConstants  - FLOOR_Y_VALUE, CIELING_Y_VALUE, LEFT_BORDER_X_VALUE, RIGHT_BORDER_X_VALUE
ATTENTION: Most of the variable in bit unit size - make sure you use only with the called variable and NOT rely directly the int value the variable set, the values will initialize and change during the start of the game.


## Scoring system
The score of a player is determined like this:
- When a ball is popped:
    - The player gets the size of the ball as a score (size = how many times a ball can be partitioned).
    - If the ball is popped by the ceiling (and therefore completely disappears) the player gets the sum of all the sizes from the ball's size to 1.
      For example - if the ball is of size 5 - the player will gain from it being popped by the ceiling 5+4+3+2+1=16 Points.

## Scoreboard
Each player in game have an scoreboard with the player name that indicates:
- Player's arrow color.
- Player's current score.
- Player's active powerups.