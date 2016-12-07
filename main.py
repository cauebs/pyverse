from galaxy import Galaxy, Body

import pygame
pygame.init()

size = (1000, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Universe")
done = False
clock = pygame.time.Clock()

g = Galaxy(size, ammount=0)

sol = Body(pos=(700, 300), radius=60, mass=1000, color=(200,250,20), static=True)
marte = Body(pos=(400, 300), radius=13, mass=15, color=(200,50,20))
terra = Body(pos=(850, 300), radius=15, mass=20, color=(20,50,200))
lua = Body(pos=(880, 300), radius=5, mass=5, color=(50,50,50))

g.add([sol, marte, terra, lua])

marte.orbit(sol)
terra.orbit(sol)
lua.orbit(terra)
lua.orbit(sol)

while not done:
    for event in pygame.event.get():
        # if event.type == pygame.MOUSEBUTTONUP:
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))

    g.draw(screen)
    g.step(5)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
