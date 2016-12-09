from galaxy import Galaxy, Body

import pygame
pygame.init()

size = (1000, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Universe")
done = False
clock = pygame.time.Clock()

g = Galaxy(size)

center = (int(size[0] / 2), int(size[1] / 2))

sol = Body(pos=center, radius=695500, mass=1.98892*10**30, color=(250, 200, 20))
terra = Body(pos=center, radius=6371, mass=5.9742*10**24, color=(50, 50, 200))
lua = Body(pos=center, radius=1737, mass=7.36*10**22, color=(50,50,50))
marte = Body(pos=center, radius=3390, mass=6.39*10**23, color=(200, 50, 50))

terra.set_distance_to(sol, 149600000)
lua.set_distance_to(terra, 384400)
marte.set_distance_to(sol, 227900000)

terra.orbit(sol)
lua.orbit(terra)
lua.orbit(sol)
marte.orbit(sol)

g.add(sol, terra, lua, marte)

while not done:
    for event in pygame.event.get():
        # if event.type == pygame.MOUSEBUTTONUP:
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))

    g.draw(screen)
    g.step()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
