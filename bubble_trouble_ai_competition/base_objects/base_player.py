import random
from typing import TYPE_CHECKING
if TYPE_CHECKING:

    # avoiding import cyclic error
    from bubble_trouble_ai_competition.powerups.punch_powerup import PunchPowerup, Powerup


from bubble_trouble_ai_competition.base_objects.base_ball import Ball
from bubble_trouble_ai_competition.game_core.events_observable import EventsObservable

from bubble_trouble_ai_competition.utils.constants import Directions, DisplayConstants, Events, Settings, PowerupsSettings
from bubble_trouble_ai_competition.utils.general_utils import circles_collide, circle_rect_collide, rect_collide
from bubble_trouble_ai_competition.utils.types import SpeedTypes
from bubble_trouble_ai_competition.utils.load_display import Images, get_ai_images
from bubble_trouble_ai_competition.game_core.game_state import game_ais, game_active_powerups

class BasePlayer:
    """
    Base class to create an AI playing the game.
    """

    def __init__(self, name: str, direction: Directions, events_observable: EventsObservable,
                 position: tuple = (1000, 0), ais_dir_path = None) -> None:
        """
        Args:
            name (str): The name of the player.
            direction (Directions): The direction the player is facing.
        """
        self.name = name
        self.direction = direction
        self.position = position
        self.width = Settings.PLAYER_DIMENSIONS[0]
        self._height = Settings.PLAYER_DIMENSIONS[1] # player's height changes during game
        self.x = position[0] + DisplayConstants.LEFT_BORDER_X_VALUE
        self.y = DisplayConstants.FLOOR_Y_VALUE - position[1] - self.height # player's height changes during game 
        self.head_radius = Settings.HEAD_RADIUS
        self.dimensions = Settings.PLAYER_DIMENSIONS
        self.update_head_center()
        self.speed = SpeedTypes.NORMAL
        self.events_observable = events_observable
        self.is_shooting = False
        self.score = 0
        self.is_competing = True
        self.is_ducking = False
        self.arrow_color = "grey"

        # Section for some of the player's active powerups.
        self.punch_powerup = False
        self.punch = False
        self.punch_right = False
        self.punch_left = False
        self.shield = False
        self.double_points = False
        self.can_freeze = False
        self.freeze_action = False
        self.freeze = False # ai flag if freeze.
        self.can_teleport = False
        self.is_teleporting = False


    @property
    def height(self):
        """
        Player's height
        """
        return self._height

    @height.setter
    def height(self, new_height):
        """
        Set new height for player and update  player y coordiantes.
        """
        self._height = new_height
        self.y = DisplayConstants.FLOOR_Y_VALUE - self.position[1] - self.height


    def update(self) -> None:
        """
        Updates the player's attributes.
        """

        self.direction = self.pick_direction()

        if self.direction == Directions.DUCK:
            self.duck()
        else:
            self.stand()
            if not self.freeze:
                self.move()

        self.update_head_center()


    def duck(self):
        """Player will duck."""

        #  update player's new height and body image
        self.height = Settings.PLAYER_DUCK_HEIGHT
        self.is_ducking = True


    def stand(self):
        """Player will stand."""

        #  update player's new height and body image
        self.height = Settings.PLAYER_DIMENSIONS[1]
        self.is_ducking = False


    def pick_direction(self) -> Directions:
        """
        Function to be implemented by the inheriting class of each ai.
        """
        return random.choice([Directions.LEFT, Directions.RIGHT])


    def do_right_punch(self):
        """
        Player will punch with his right punch.
        """
        if self.punch_powerup:            
            self.punch_right = True
        

    def do_left_punch(self):
        """
        Player will punch with his left punch.
        """
        if self.punch_powerup:
            self.punch_left = True
            
    def shoot(self):
        """
        Player will shoot.
        """
        if (self.is_shooting == False):
            self.is_shooting = True
            self.events_observable.notify_observers(Events.PLAYER_SHOT, self)
    

    def move(self) -> None:
        """
        Moves the player.
        """

        self.x += self.direction * Settings.FRAME_TIME * self.speed
        self.keep_player_in_borders()

    def teleport(self) -> None:
        self.x = self.pick_x_to_teleport_to()
        self.keep_player_in_borders()

    def keep_player_in_borders(self):
        """ Keep player at the game borders."""

        # Making sure the AI is not going out of bounds.
        if (self.x < DisplayConstants.LEFT_BORDER_X_VALUE):
            self.x = DisplayConstants.LEFT_BORDER_X_VALUE
        if (self.x > DisplayConstants.RIGHT_BORDER_X_VALUE - self.width):
            self.x = DisplayConstants.RIGHT_BORDER_X_VALUE - self.width

    def talk(self) -> None:
        """
        Player will talk.
        """
        print (self.name)
    

    def update_head_center(self) -> None:
        """
        Updates the head center of the player.
        """
        self.head_center = ((self.x + (self.x + self.width)) / 2, self.y - self.head_radius)


    def collides_with_ball(self, ball: Ball) -> bool:
        """
        Checks if the player collides with a ball.

        Args:
            ball (Ball): The ball to check if the player collides with.
        
        Returns:
            bool: True if the player collides with the ball, False otherwise.
        """
        # Check if the player has shield
        if self.shield == True or self.is_teleporting:
            return False

        # Check if the player's head collides with the ball
        if (circles_collide(self.head_center, self.head_radius, (ball.x, ball.y), ball.radius)):
            return True
        
        # Check if the player's body collides with the ball
        if (circle_rect_collide(self.x, self.y, self.width, self.height, ball.x, ball.y, ball.radius)):
            return True
        
        # No collision - return False
        return False


    def collides_with_powerup(self, powerup: 'Powerup') -> bool:
        """
        Checks if the player collides with a power up.

        Args:
            powerup (Powerup): The power up to check if the player collides with.
        
        Returns:
            bool: True if the player collides with the power up, False otherwise.
        """
        # Check if player already have an active powerup.
        if str(type(powerup).__name__) in ['TeleportPowerup', 'FreezePowerup', 'PlayerSpeedBoostPowerup']:
            for active_powerup in game_active_powerups():
                print(active_powerup)
                if type(powerup) == type(active_powerup) and self.name == active_powerup.player.name:
                    return False


        # Check if the player's head collides with the powerup
        if (circle_rect_collide(powerup.x, powerup.y, powerup.width, powerup.height, self.head_center[0], self.head_center[1], self.head_radius)):
            return True

        # Check if the player's body collides with the powerup
        if rect_collide(self.x, self.y, self.width, self.height, powerup.x, powerup.y, powerup.width, powerup.height):
            return True      
 
        # No collision - return False
        return False
    

    def collides_with_punch(self, punch: 'PunchPowerup', punch_left, punch_right):
        """
        Checks if the player collides with other player's punch..

        Args:
            punch (PunchPowerup): The punch to check if the player collides with.
        
        Returns:
            bool: True if the player collides with the punch, False otherwise.
        """

        # Check if the player's body collides with the powerup
        if punch_left == True:
            (punch_x, punch_y) = punch.get_left_punch_action_coordinates()
        else:
            (punch_x, punch_y) = punch.get_right_punch_action_coordinates()

        if (punch_right and self.x > punch_x) or (punch_left and self.x-PowerupsSettings.PUNCH_ACTION_WIDTH < punch_x):
            if rect_collide(self.x, self.y, self.width, self.height, punch_x, punch_y, PowerupsSettings.PUNCH_ACTION_WIDTH, PowerupsSettings.PUNCH_ACTION_HEIGHT):
                return True      
 
        # No collision - return False
        return False
    

    def get_right_punch_hit(self, punch: 'PunchPowerup'):
        """
        """
        # move ai to right
        if (self.x + Settings.HIT_RADIUS > DisplayConstants.RIGHT_BORDER_X_VALUE - self.width):
            self.x = DisplayConstants.RIGHT_BORDER_X_VALUE - self.width
            
        else:
            self.x = self.x + Settings.HIT_RADIUS


    def get_left_punch_hit(self, punch: 'PunchPowerup'):
        """
        """
        # move ai to left
        if (self.x - Settings.HIT_RADIUS < DisplayConstants.LEFT_BORDER_X_VALUE):
            self.x = DisplayConstants.LEFT_BORDER_X_VALUE
        else:
            self.x = self.x - Settings.HIT_RADIUS

    def draw(self, screen) -> None:
        """
        Draws the player on the screen.

        Args:
            screen (pygame.Surface): The screen to draw the player on.
        """
        ai_images = get_ai_images(self.name)

        # Drawing body
        body_image, body_image_coordinates = self.get_body_image_and_coordinates(ai_images)        
        screen.blit(body_image, body_image_coordinates)

        # Drawing head
        head_image_draw_position = (self.head_center[0] - self.head_radius, self.head_center[1] - self.head_radius)

        if (self.direction == Directions.STAND or self.direction == Directions.DUCK):
            screen.blit(ai_images[Settings.PLAYER_HEAD], head_image_draw_position)
        elif (self.direction == Directions.LEFT):
            screen.blit(ai_images[Settings.PLAYER_LEFT_HEAD], head_image_draw_position)
        elif (self.direction == Directions.RIGHT):
            screen.blit(ai_images[Settings.PLAYER_RIGHT_HEAD], head_image_draw_position)


    def get_body_image_and_coordinates(self, ai_images) -> tuple:
        """Return the body image and body image coordinates of player."""

        # Set the regular player body image and coordinates.
        body_image = ai_images[Settings.PLAYER_STAND_BODY]
        body_image_coordinates = (self.x, self.y)

        # Check if player have active speed boost powerup.
        if self.speed == SpeedTypes.FAST:
            # Set flash suit body coordinates.
            body_image_coordinates = (self.x - PowerupsSettings.FLASH_SUIT_SHIFT_X, self.y - PowerupsSettings.FLASH_SUIT_SHIFT_Y)
            if self.is_ducking == True:
                # Set the duck flash suit body image.
                body_image = Images.powerups_images[PowerupsSettings.DUCK_FLASH_SUIT]
            else:
                # Set the stand flash suit body image.
                body_image = Images.powerups_images[PowerupsSettings.STAND_FLASH_SUIT]

        else:
            if self.is_ducking == True:
                # Set the regular duck body image.
                body_image = ai_images[Settings.PLAYER_DUCK_BODY]
        
        return body_image, body_image_coordinates
    
     
    def can_shoot(self) -> bool:
        """
        Checks if the player can shoot.

        Returns:
            bool: True if the player can shoot, False otherwise.
        """
        return self.is_shooting == False

    def get_player_top_right_corner(self) -> tuple:
        """
        Returns the top right corner of the player.

        Returns:
            tuple: The top right corner of the player.
        """
        return (self.x + self.width, self.y - self.head_radius*2)


    def get_player_top_left_corner(self) -> tuple:
        """
        Returns the top left corner of the player.

        Returns:
            tuple: The top left corner of the player.
        """
        return (self.x, self.y - self.head_radius*2)

    def get_player_left_hand_coordinates(self) -> tuple:
        """
        Returns the player's left hand coordinates.

        Returns:
            tuple: The left hand coordinates of the player (x,y).
        """
        return (self.x - self.head_radius + Settings.PLAYER_HANDS_SPACING, self.y - self.head_radius)
    
    def get_player_right_hand_coordinates(self) -> tuple:
        """
        Returns the player's right hand coordinates.

        Returns:
            tuple: The right hand coordinates of the player (x,y).
        """
        return (self.x + self.width - (self.width/2 - self.head_radius) - Settings.PLAYER_HANDS_SPACING, self.y - self.head_radius)

    def get_score(self) -> int:
        """
        Returns the player's score.

        Returns:
            int: The player's score.
        """
        return self.score
    

    def do_freeze(self) -> None:
        """Freeze another ai player with the freeze powerup"""
        if self.can_freeze:
            self.freeze_action = True # make sure player freeze only one player

    def do_teleport(self) -> None:
        """Teleport to another place in game with the teleport powerup"""
        if self.can_teleport:
            self.is_teleporting = True

    def pick_x_to_teleport_to(self):
        return self.x + 100

    def pick_player_to_freeze(self):
        """ Returns the name of the ai that player chose to freeze, randomly."""
        other_ais = [ai for ai in game_ais() if ai.name != self.name]
        # Check that there are still others ais in game.
        if other_ais != []:
            ai = random.choice(other_ais) 
            return ai.name
        else:
            return None



    