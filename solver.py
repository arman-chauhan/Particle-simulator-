import numpy as np

from link import Link
from particle import Particle
from quadtree import Quadtree, Rectangle
from scipy.spatial import KDTree


# TODO: change the particles buffer into a matrix  for easier matrix operations
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
            # self.link(sub_dt)
            self.fixParticles()
            # self.bruteCollisions()
            # self.quadTreeCollisions()
            self.KDtreeCollisions()
            self.updatePositions(sub_dt)

    def updatePositions(self, dt):
        for particle in self.particles:
            particle.updatePosition(dt)

    # TODO: vectorize gravity addition
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
            for neighbour in all_particles[i + 1:]:
                self.handle_collisions(neighbour, particle)

    def quadTreeCollisions(self):
        qt = Quadtree(0, Rectangle(0, 0, 900, 900))
        qt.clear()
        all_particles = self.particles + self.fixedParticles
        for p in all_particles:
            qt.insert(p)

        neighbours = []
        for p in all_particles:
            neighbours.clear()
            qt.retrieve(neighbours, p)

            # handle collision
            for neighbour in neighbours:
                self.handle_collisions(neighbour, p)

    def KDtreeCollisions(self):
        all = (self.particles + self.fixedParticles)
        data = np.array([particle.position for particle in all])
        if data.shape[0] == 0:
            return

        kd = KDTree(data)
        pairs = kd.query_pairs(r=16)
        for (i, j) in pairs:
            self.handle_collisions(all[i], all[j])

    @staticmethod
    def handle_collisions(neighbour: Particle, particle: Particle):
        if particle is neighbour:
            return

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
