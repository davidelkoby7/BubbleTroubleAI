import math


def distance(point1: tuple, point2: tuple) -> float:
    """
    Calculates the distance between two points.

    Args:
        point1 (tuple): The first point.
        point2 (tuple): The second point.
    
    Returns:
        float: The distance between the two points.
    """
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def circles_collide(circle1_center: tuple, circle1_radius: int, circle2_center: tuple, circle2_radius: int) -> bool:
    """
    Checks if two circles collide.

    Args:
        circle1_center (tuple): The center of the first circle.
        circle1_radius (int): The radius of the first circle.
        circle2_center (tuple): The center of the second circle.
        circle2_radius (int): The radius of the second circle.
    
    Returns:
        bool: True if the two circles collide, False otherwise.
    """
    return distance(circle1_center, circle2_center) < circle1_radius + circle2_radius


def circle_rect_collide(rleft: int, rtop: int, width: int, height: int, center_x: int, center_y: int, radius: int) -> bool:
    """
    Checks if a circle collides with a rectangle.
    Thanks for stackoverflow, saved me here.

    Args:
        rleft (int): The left coordinate of the rectangle.
        rtop (int): The top coordinate of the rectangle.
        width (int): The width of the rectangle.
        height (int): The height of the rectangle.
        center_x (int): The x coordinate of the circle's center.
        center_y (int): The y coordinate of the circle's center.
        radius (int): The radius of the circle.
    
    Returns:
        bool: True if the circle collides with the rectangle, False otherwise.
    """

    # complete boundbox of the rectangle
    rright, rbottom = rleft + width/2, rtop + height/2

    # bounding box of the circle
    cleft, ctop     = center_x-radius, center_y-radius
    cright, cbottom = center_x+radius, center_y+radius

    # trivial reject if bounding boxes do not intersect
    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False  # no collision possible

    # check whether any point of rectangle is inside circle's radius
    for x in (rleft, rleft+width):
        for y in (rtop, rtop+height):
            # compare distance between circle's center point and each point of
            # the rectangle with the circle's radius
            if math.hypot(x-center_x, y-center_y) <= radius:
                return True  # collision detected

    # check if center of circle is inside rectangle
    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True  # overlaid

    return False  # no collision detected

