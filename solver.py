from vector2 import Vector2
from particle import Particle
from link import Link


class Solver:
    def __init__(self):
        self.particles: list[Particle] = []
        self.fixedParticles: list[Particle] = []
        self.constraintCenter = Vector2()
        self.constraintRadius = 0

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

    def applyGravity(self, gravity=Vector2(0, 1000.0)):
        for particle in self.particles:
            particle.accelerate(gravity)

    def applyAttraction(self, pos: Vector2, G=5000, damping_factor=0.5):
        for particle in self.particles:
            force_vector = pos - particle.position
            distance = force_vector.length()
            if distance > particle.radius + 30:
                magnitude = G * (particle.mass) / (distance**2)

                force_direction = force_vector.normalize()
                force = force_direction * magnitude
                particle.position += force * damping_factor

    def addParticle(self, pos, radius):
        self.particles.append(Particle(pos, radius))

    def addFixedParticle(self, pos, radius):
        self.fixedParticles.append(Particle(pos, radius))

    def setConstraint(self, position: Vector2, radius: float):
        self.constraintCenter = position
        self.constraintRadius = radius

    def applyConstraint(self):
        for particle in self.particles:
            to_particle = particle.position - self.constraintCenter
            dist = to_particle.length()

            if dist > self.constraintRadius - particle.radius:
                normal = to_particle.normalize()  # normalize the vector
                particle.position = self.constraintCenter + normal * (
                    self.constraintRadius - particle.radius
                )

    def updateLink(self, dt):
        sub_steps = 8
        sub_dt = float(dt / sub_steps)
        for _ in range(sub_steps):
            self.applyGravity()
            self.applyConstraint()
            self.solveCollisions()
            self.link()
            self.fixParticles()
            self.updatePositions(sub_dt)

    def fixParticles(self):
        for particle in self.fixedParticles:
            particle.position = particle.position_old

    def solveCollisions(self):
        allParticles = self.particles + self.fixedParticles
        for i, p1 in enumerate(allParticles):
            for p2 in allParticles[i + 1 :]:
                v = p1.position - p2.position
                dist = v.length()
                min_dist = p1.radius + p2.radius

                if dist < min_dist:
                    n = v.normalize()
                    massratio1 = p1.radius / (p1.radius + p2.radius)
                    massratio2 = p2.radius / (p1.radius + p2.radius)
                    delta = 0.375 * (dist - min_dist)
                    p1.position -= n * massratio1 * delta
                    p2.position += n * massratio2 * delta

    def link(self):
        allParticles = self.fixedParticles + self.particles
        for i in range(1, len(allParticles)):
            chain = Link(allParticles[i - 1], allParticles[i])
            chain.apply()
