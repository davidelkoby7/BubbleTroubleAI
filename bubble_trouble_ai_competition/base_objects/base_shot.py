
class BaseShot:
    def __init__(self, x: int, y: int, speed: float):
        """
        Initialize the shot object.
        Args:
            x (int): The x coordinate of the shot.
            y (int): The y coordinate of the shot.
            speed (float): The speed of the shot.
        """
        self.x = x
        self.y = y
        self.speed = speed
