from particle import Particle


class Link:
    def __init__(self, particle1: Particle, particle2: Particle) -> None:
        self.p1: Particle = particle1
        self.p2: Particle = particle2
        self.target_dist = 20
        self.damping_factor = 0.1  # Lowering this reduces the movement per update

    def apply(self):
        axis = self.p1.position - self.p2.position
        dist = axis.length()
        n = axis.normalize()
        delta = self.target_dist - dist
        correction = self.damping_factor * delta

        # Move each particle by half the correction distance
        self.p1.position += n * (correction)
        self.p2.position -= n * (correction)
