import numpy as np

from particle import Particle


class Link:
    def __init__(self, particle1: Particle, particle2: Particle) -> None:
        self.p1: Particle = particle1
        self.p2: Particle = particle2
        self.target_dist = 20
        self.link_constant = 1  # Lowering this reduces the movement per update

    def apply(self, dt):
        axis = self.p1.position - self.p2.position
        dist = np.sqrt(axis.dot(axis))
        n = axis / dist

        delta = self.target_dist - dist
        correction = self.link_constant * delta

        # Move each particle by half the correction distance
        self.p1.position += 0.5 * n * correction
        self.p2.position -= 0.5 * n * correction
