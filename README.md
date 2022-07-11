# BubbleTroubleAI
Bubble trouble game AI Competition framework.

## Installation
Run `python -m pip install -r .\requirements.txt`.

## Creators
Made by davidalk & tehila.

## Scoring system
The score of a player is determined like this:
- When a ball is popped:
    - The player gets the size of the ball as a score (size = how many times a ball can be partitioned).
    - If the ball is popped by the ceiling (and therefore completely disappears) the player gets the sum of all the sizes from the ball's size to 1.
      For example - if the ball is of size 5 - the player will gain from it being popped by the ceiling 5+4+3+2+1=16 Points.
