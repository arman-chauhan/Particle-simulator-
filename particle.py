from typing import Any

import numpy as np


class Particle:
    def __init__(self, pos: tuple, radius: int):
        self.radius = radius
        self.position = np.array(pos, dtype=np.float64)
        self.position_old = np.array(pos, dtype=np.float64)
        self.acceleration = np.zeros(2)
        self.mass = 1

    def updatePosition(self, dt: float, damping=0.75):
        displacement = self.position - self.position_old
        speed = np.sqrt(displacement.dot(displacement))
        max_speed = 30

        if speed > max_speed:
            displacement = (displacement / speed) * max_speed

        # Store current position
        self.position_old = self.position
        # Perform Varlet integration
        self.position = self.position + displacement + self.acceleration * dt * dt
        # Reset acceleration
        self.acceleration = np.zeros(2)

    def accelerate(self, acc: np.ndarray[Any, np.dtype]):
        self.acceleration += acc

    def applyForce(self, force):
        self.acceleration += force / self.mass
