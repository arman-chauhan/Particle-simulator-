import numpy as np

from link import Link
from particle import Particle


class Solver:
    def __init__(self, constraintCenter: tuple, constraintRadius: float):
        self.particles: list[Particle] = []
        self.fixedParticles: list[Particle] = []
        self.constraintCenter = np.array(constraintCenter)
        self.constraintRadius = constraintRadius
        self.gravity = np.array((0, 1000.0))

    def update(self, dt):
        sub_steps = 8
        sub_dt = float(dt / sub_steps)
        for _ in range(sub_steps):
            self.applyGravity()
            self.applyConstraint()
            self.solveCollisions()
            self.updatePositions(sub_dt)

    def updatePositions(self, dt):
        for particle in self.particles:
            particle.updatePosition(dt)

    def applyGravity(self):
        for particle in self.particles:
            particle.accelerate(self.gravity)

    def applyAttraction(self, pos: tuple, G=3000, damping_factor=1):
        pos = np.array(pos)
        for particle in self.particles:
            axis = particle.position - pos
            dist = np.sqrt(axis.dot(axis))

            if dist > particle.radius + 40:
                magnitude = G * particle.mass / (dist ** 2)
                force_direction = axis / dist
                force = force_direction * magnitude

                particle.position -= force * damping_factor

    def addParticle(self, pos, radius):
        self.particles.append(Particle(pos, radius))

    def addFixedParticle(self, pos, radius):
        self.fixedParticles.append(Particle(pos, radius))

    def applyConstraint(self):
        for particle in self.particles:
            to_particle = particle.position - self.constraintCenter
            dist = np.sqrt(to_particle.dot(to_particle))

            if dist > self.constraintRadius - particle.radius:
                normal = to_particle / dist  # normalize the vector
                particle.position = self.constraintCenter + normal * (
                        self.constraintRadius - particle.radius
                )

    def updateLink(self, dt):
        sub_steps = 8
        sub_dt = float(dt / sub_steps)
        for _ in range(sub_steps):
            self.applyGravity()
            self.link(sub_dt)
            self.applyConstraint()
            self.solveCollisions()
            self.fixParticles()
            self.updatePositions(sub_dt)

    def fixParticles(self):
        for particle in self.fixedParticles:
            particle.position = particle.position_old.copy()

    def solveCollisions(self):
        allParticles = self.particles + self.fixedParticles
        for i, p1 in enumerate(allParticles):
            for p2 in allParticles[i + 1:]:
                v = p1.position - p2.position
                dist = np.sqrt(v.dot(v))
                min_dist = p1.radius + p2.radius

                if dist < min_dist:
                    n = v / dist
                    delta = 0.375 * (dist - min_dist)

                    mass_ratio1 = p1.radius / (p1.radius + p2.radius)
                    mass_ratio2 = p2.radius / (p1.radius + p2.radius)

                    p1.position -= n * mass_ratio1 * delta
                    p2.position += n * mass_ratio2 * delta

    def link(self, dt):
        allParticles = self.fixedParticles + self.particles
        for i in range(1, len(allParticles)):
            chain = Link(allParticles[i - 1], allParticles[i])
            chain.apply(dt)
