import math
from vector2 import Vector2
from particle import Particle


class Solver:

    def __init__(self):
        self.particles: list[Particle] = []
        self.gravity = Vector2(0.0, 1000.0)
        self.constraintCenter = Vector2()
        self.constraintRadius = 0

    def update(self, dt):
        sub_steps = 20
        sub_dt = float(dt / sub_steps)
        for i in range(sub_steps):
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

    def addParticle(self, pos, radius):
        self.particles.append(Particle(pos, radius))

    def setConstraint(self, position, radius):
        self.constraintCenter = Vector2(*position)
        self.constraintRadius = radius

    def applyConstraint(self):
        for particle in self.particles:
            to_particle = particle.position - self.constraintCenter
            dist = to_particle.len()

            if dist > self.constraintRadius - particle.radius:
                normal = to_particle.normalize()  # normalize the vector
                particle.position = self.constraintCenter + normal * (self.constraintRadius - particle.radius)

    def solveCollisions(self):
        for i, p1 in enumerate(self.particles):
            for p2 in self.particles[i + 1:]:
                v = p1.position - p2.position
                dist = v.len()
                min_dist = p1.radius + p2.radius

                if dist < min_dist:
                    n = v.normalize()
                    massratio1 = p1.radius / (p1.radius + p2.radius)
                    massratio2 = p2.radius / (p1.radius + p2.radius)
                    delta = 0.375 * (dist - min_dist)
                    p1.position -= n * massratio1 * delta
                    p2.position += n * massratio2 * delta
