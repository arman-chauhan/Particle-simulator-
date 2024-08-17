import pygame


class Renderer:
    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen

    def render(self, solver):
        self.renderConstraint()
        self.renderParticles(solver)

    def renderParticles(self, solver):
        # Render particles
        for particle in solver.particles:
            pos = (particle.position.x, particle.position.y)
            radius = particle.radius
            color = "WHITE"

            pygame.draw.circle(self.screen, color, pos, radius)

    def renderConstraint(self):
        # Render container
        size = self.screen.get_size()
        center = size[0] * 0.5, size[1] * 0.5

        pygame.draw.circle(self.screen, "BLACK", center, 400)
