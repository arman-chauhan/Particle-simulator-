from vector2 import Vector2
import numpy as np


class Particle:
    def __init__(self, pos: Vector2, radius):
        self.radius = radius
        self.position: Vector2 = pos
        self.position_old: Vector2 = pos
        self.acceleration = Vector2()
        self.mass = 1

    def updatePosition(self, dt, damping=0.75):
        velocity = self.position - self.position_old
        max_vel = 30
        if velocity.length() > max_vel:
            velocity = velocity.normalize() * max_vel
        # Store current position
        self.position_old = self.position
        # Perform Verlet integration
        self.position = self.position + velocity + self.acceleration * dt * dt
        # Reset acceleration
        self.acceleration = Vector2(0, 0)

    def accelerate(self, acc):
        self.acceleration += acc

    def applyForce(self, force: Vector2):
        self.acceleration += force / self.mass
