import numpy as np

import quadtree
from link import Link
from particle import Particle
from quadtree import Quadtree, Rectangle


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
            # self.bruteCollisions()
            # self.link()
            self.fixParticles()
            self.updatePositions(sub_dt)
            self.quadTreeCollisions()

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

    def fixParticles(self):
        for particle in self.fixedParticles:
            particle.position = particle.position_old.copy()

    def bruteCollisions(self):
        all_particles = self.particles + self.fixedParticles
        for i, particle in enumerate(all_particles):
            self.handle_collisions(all_particles[i + 1:], particle)

    def quadTreeCollisions(self):
        qt = Quadtree(0, Rectangle(0, 0, 900, 900))
        qt.clear()
        for p in self.particles:
            qt.insert(p)

        for p in self.particles:
            neighbours = qt.retrieve(p)
            self.handle_collisions(neighbours, p)

    @staticmethod
    def handle_collisions(neighbours: list[Particle], particle: Particle):
        for neighbour in neighbours:
            if particle is neighbour:
                continue
            v = particle.position - neighbour.position
            dist = np.sqrt(v.dot(v))
            min_dist = particle.radius + neighbour.radius

            if dist < min_dist:
                n = v / dist
                delta = 0.375 * (dist - min_dist)

                mass_ratio1 = particle.radius / (particle.radius + neighbour.radius)
                mass_ratio2 = neighbour.radius / (particle.radius + neighbour.radius)

                particle.position -= n * mass_ratio1 * delta
                neighbour.position += n * mass_ratio2 * delta

    def link(self, dt):
        all_particles = self.fixedParticles + self.particles
        for i in range(1, len(all_particles)):
            chain = Link(all_particles[i - 1], all_particles[i])
            chain.apply(dt)
