import pygame
import sys
import math
import numpy as np
import typer
import logging


# SETUP
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# CONSTANTS
G = 9.8
REBOUND_FACTOR = 0.5
MASS = 10

COLORS = [
    (217, 237, 146),
    (93, 115, 126),
    (30, 96, 145),
    (62, 63, 63),
    (143, 45, 86),
    (116, 0, 184),
    (56, 4, 14),
]


class Body:
    def __init__(self, x, y, mass, velocity, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = int(math.sqrt(mass) * 2)
        self.vx, self.vy = velocity
        self.color = color
        self.trace = []

    def __eq__(self, other) -> bool:
        """
        Check if the current object is equal to another object by comparing their colors.

        Parameters
        ----------
        self : object
            The current object to compare.
        other : object
            The other object for comparison.

        Returns
        -------
        bool
            True if the colors of the current object and the other object are equal; otherwise, False.

        Notes
        -----
        This special method (__eq__) is used to determine whether the current object is equal to another object.
        It compares the colors of both objects and returns True if the colors are the same, indicating equality.
        If the colors are not the same, it returns False.

        See Also
        --------
        - color: The color attribute of the objects used for the comparison.
        """
        if self.color == other.color:
            return True
        else:
            return False

    def calculate_grav_force(self, bodies: list):
        """
        Calculate and apply the gravitational force from multiple bodies on the current object.

        Parameters
        ----------
        self : object
            The object on which the gravitational forces are applied.
        bodies : list
            A list of Body objects representing the other bodies influencing the current object.

        Returns
        -------
        None

        Notes
        -----
        This method calculates the cumulative gravitational force acting on the current object due to the presence of
        other bodies in the provided list. It iterates through the 'bodies' list, excluding itself, and accumulates
        the gravitational forces applied by each of the other bodies. The resulting force is then split into its
        horizontal and vertical components, and the 'update' method is called to adjust the object's position and velocity
        based on the calculated force.

        See Also
        --------
        - calculate_gravitational_force: The method for calculating the gravitational force between two objects.
        - add_tuples: The method for summing components of a tuple.
        - update: The method for updating the object's position and velocity.
        """
        force = (0, 0)
        for body in bodies:
            if body != self:
                force += calculate_gravitational_force(self, body)
        force1x, force1y = add_tuples(force)
        self.update(force1x, force1y)

    def update(self, force_x: float, force_y: float):
        """
        Update the object's position and velocity based on applied forces.

        Parameters
        ----------
        self : object
            The object to be updated.
        force_x : float
            The horizontal component of the applied force.
        force_y : float
            The vertical component of the applied force.

        Returns
        -------
        None

        Notes
        -----
        This method updates the object's position and velocity based on the forces applied to it. It calculates
        the acceleration components (ax and ay) by dividing the applied forces by the object's mass. The velocities
        (vx and vy) are then adjusted based on the acceleration, and the positions (x and y) are updated accordingly.
        After the position update, it calls the `check_boundaries` and `update_trace` methods to ensure the object
        stays within boundaries and keeps a trace of its path.

        See Also
        --------
        - check_boundaries: The method for handling object boundaries.
        - update_trace: The method for updating the object's path trace.
        """
        ax = force_x / self.mass
        ay = force_y / self.mass
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy
        self.check_boundaries()
        self.update_trace()

    def update_trace(self):
        """
        Update the trace of object's path with its current position.

        Parameters
        ----------
        self : object
            The object whose trace is being updated.

        Returns
        -------
        None

        Notes
        -----
        This method adds the current position (x, y) of the object to its trace, which is represented as a list of points.
        If the trace length reaches 100 points, the oldest point (at the beginning of the list) is removed to maintain
        a fixed length of 100 points.

        See Also
        --------
        - trace: The list representing the object's path.
        """
        self.trace.append((self.x, self.y))
        if len(self.trace) == 100:
            self.trace.pop(0)

    def check_boundaries(self):
        """
        Check and handle object boundaries to prevent it from going out of bounds.

        Parameters
        ----------
        self : object
            The object representing the moving entity with attributes 'x', 'y', 'vx', 'vy'.

        Returns
        -------
        None

        Notes
        -----
        This method checks the boundaries of the object's position and velocity and takes appropriate actions
        to prevent the object from going out of bounds. If the object's vertical position (`y`) is less than 0,
        it's set to 0, and the vertical velocity (`vy`) is reversed with a rebound factor. If `y` is greater
        than the specified height, it's set to the height, and `vy` is reversed with a rebound factor. Similarly,
        if `x` is less than 0, it's set to 0, and the horizontal velocity (`vx`) is reversed with a rebound factor.
        If `x` is greater than the specified width, it's set to the width, and `vx` is reversed with a rebound factor.

        The rebound factor should be defined as a constant, and the `height` and `width` values should be
        provided to ensure proper boundary checking and adjustment.

        See Also
        --------
        - REBOUND_FACTOR: The constant determining the rebound factor.
        - height: The maximum height of the boundary.
        - width: The maximum width of the boundary.
        """
        if self.y < 0:
            self.y = 0
            self.vy *= -REBOUND_FACTOR
        elif self.y > height:
            self.y = height
            self.vy *= -REBOUND_FACTOR
        if self.x < 0:
            self.x = 0
            self.vx *= -REBOUND_FACTOR
        elif self.x > width:
            self.x = width
            self.vx *= -REBOUND_FACTOR

    def draw(self, screen):
        """
        Draw the object on a Pygame screen.

        Parameters
        ----------
        self : object
            The object to be drawn, with attributes 'x', 'y', 'color', and 'radius'.
        screen : pygame.Surface
            The Pygame surface where the object should be drawn.

        Returns
        -------
        None

        Notes
        -----
        This method draws the object on the specified Pygame screen. It first draws a series of circles to represent
        a trace of the object's path, using the object's color and a small radius. Then, it draws a larger circle to
        represent the current position of the object, using the object's color and radius. The position and color of
        the object are determined by its attributes ('x', 'y', 'color', and 'radius').

        Note that this method relies on Pygame functionality, and you should have Pygame properly set up for it to work.

        See Also
        --------
        - Pygame: The Pygame library (https://www.pygame.org) used for game and multimedia development.
        """
        for point in self.trace:
            pygame.draw.circle(screen, self.color, point, 1)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


def calculate_gravitational_force(p1: Body, p2: Body) -> tuple:
    """
    Calculate the gravitational force between two objects in a 2D space.

    Parameters
    ----------
    p1 : Body
        An object representing the first body with attributes 'x', 'y', and 'mass' for position and mass.
    p2 : Body
        An object representing the second body with attributes 'x', 'y', and 'mass' for position and mass.

    Returns
    -------
    tuple
        A tuple containing two components:
        - The horizontal component of the gravitational force between the bodies.
        - The vertical component of the gravitational force between the bodies.

    Notes
    -----
    This function computes the gravitational force between two objects in a 2D space using Newton's law of universal gravitation.
    It takes into account the positions (x, y) and masses of both objects. The force is calculated as follows:
    - dx and dy represent the differences in the x and y coordinates of the two bodies.
    - The distance between the bodies is computed using the Euclidean distance formula.
    - If the distance is less than 40 (to prevent extremely strong forces at close range), no force is applied.
    - The gravitational force is then calculated using Newton's formula and divided into horizontal and vertical components.
    - The resulting force components are returned as a tuple.

    See Also
    --------
    - Newton's law of universal gravitation: The physical law describing the gravitational force between two objects.
    """
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance = max(1, math.sqrt(dx**2 + dy**2))
    if distance < 40:
        return (0, 0)
    force = (G * p1.mass * p2.mass) / (distance**2)
    angle = math.atan2(dy, dx)
    force_x = force * math.cos(angle)
    force_y = force * math.sin(angle)
    return (force_x, force_y)


def add_tuples(tuple: tuple) -> tuple:
    """
    Splits a given tuple into two parts: even-indexed and odd-indexed elements,
    sums the elements in each part separately, and returns a new tuple containing
    the sums.

    Parameters
    ----------
    input_tuple : tuple
        A tuple containing numeric elements.

    Returns
    -------
    tuple
        A new tuple with two elements:
        - The sum of the even-indexed elements in the input tuple.
        - The sum of the odd-indexed elements in the input tuple.
    """
    even = 0
    odd = 0
    for i in range(len(tuple)):
        if i % 2 == 0:
            even += tuple[i]
        else:
            odd += tuple[i]
    return (even, odd)


def main():
    # CALCULATE NECESSARY TRIGONOMETRY
    side = 200
    x = np.sqrt(side**2 - (side / 2) ** 2)
    initial_x = 300
    initial_y = 400

    # INITIAL BODIES
    body1 = Body(
        initial_x, initial_y, mass=MASS, velocity=(0.1, 0.1), color=(116, 148, 196)
    )
    body2 = Body(
        (initial_x + (initial_x + side)) / 2,
        initial_y - x,
        mass=MASS,
        velocity=(-0.1, 0.1),
        color=(106, 77, 97),
    )
    body3 = Body(
        initial_x + side,
        initial_y,
        mass=MASS,
        velocity=(0.1, -0.1),
        color=(195, 212, 7),
    )
    bodies = [body1, body2, body3]

    # MAIN LOOP
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(bodies) < 10:
                    mouse = pygame.mouse.get_pos()
                    bodies.append(
                        Body(
                            mouse[0],
                            mouse[1],
                            mass=MASS,
                            velocity=(0.1, 0.1),
                            color=COLORS[len(bodies) - 3],
                        )
                    )
                else:
                    logging.warning("You've reached the maximum of bodies!")

        screen.fill((0, 0, 0))

        for body in bodies:
            body.calculate_grav_force(bodies)
            body.draw(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    typer.run(main)
