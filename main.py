from time import time

import pygame as pg

from render import Renderer
from solver import Solver
from vector2 import Vector2

pg.init()

Size = (1000, 900)
screen = pg.display.set_mode(Size)
pg.display.set_caption("Pygame Gravity Example")
screen.fill("GRAY")
clock = pg.time.Clock()

fpsColor = (162, 177, 219)
font = pg.font.Font(None, 36)

dt = 1 / 60
radius = 8
running = True

lastClickTime = 0
debounceTime = 0.2

constraintCenter = Vector2(Size[0] * 0.5, Size[1] * 0.5)
constraintRadius = 400

solver = Solver()
solver.setConstraint(constraintCenter, constraintRadius)
renderer = Renderer(screen)

while running:
    currentTime = time()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if pg.mouse.get_pressed()[0]:
        pos = Vector2(*pg.mouse.get_pos())
        dist = (pos - constraintCenter).length()
        if dist < constraintRadius - radius:
            if currentTime - lastClickTime > debounceTime:
                lastClickTime = currentTime
                solver.addParticle(pos, radius)

    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        pos = Vector2(*pg.mouse.get_pos())
        solver.applyAttraction(pos)

    fps = clock.get_fps()
    fps_text = f"FPS: {fps:.2f}"
    text_surface = font.render(fps_text, True, fpsColor)

    solver.update(dt)
    screen.fill("GRAY")
    screen.blit(text_surface, (10, 10))
    renderer.render(solver)

    clock.tick(60)
    pg.display.flip()

# Quit Pygame
pg.quit()
