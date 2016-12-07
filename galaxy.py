import numpy as np
from math import sqrt
from random import randint, uniform
from pygame import gfxdraw

G = 0.02


class Galaxy:

    def __init__(self, size, ammount=10, mass_range=(5, 25), radius_range=(5, 25)):
        self.bodies = []
        for _ in range(ammount):
            b = Body(
                    (randint(0, size[0]), randint(0, size[1])),
                radius=randint(*radius_range),
                mass=uniform(*mass_range),
                # initial_speed=(uniform(0, 1), uniform(0, 1)),
                initial_speed=(0, 0),
                color=(randint(0, 255), randint(0, 255), randint(0, 255))
            )
            self.add_body(b)

    def add(self, b):
        if type(b) == list:
            for i in b:
                self.bodies.append(i)
        else:
            self.bodies.append(b)

    def add_forces(self):
        for b1 in self.bodies:
            temp_list = list(self.bodies)
            temp_list.remove(b1)
            b1.acceleration = np.array([0., 0.])
            for b2 in temp_list:
                d = b2.pos - b1.pos
                r = np.sqrt(d.dot(d))
                if r < 5:
                    force = 0
                else:
                    force = d * G * b1.mass * b2.mass / r**3
                b1.apply_force(force)

    def draw(self, screen):
        for b in self.bodies:
            b.draw(screen)

    def step(self, n=1):
        self.add_forces()
        for _ in range(n):
            for b in self.bodies:
                b.step()


class Body:

    def __init__(self, pos, radius, mass, initial_speed=(0., 0.), color=(255, 255, 255), static=False):
        self.pos = np.array(pos).astype(float)
        self.radius = radius
        self.mass = mass
        self.color = color
        self.acceleration = np.array([0., 0.])
        self.speed = np.array(initial_speed).astype(float)
        self.static = static

    @property
    def velocity(self):
        np.sqrt(self.speed.dot(self.speed))

    def apply_force(self, force):
        self.acceleration += force / self.mass

    def step(self):
        if not self.static:
            self.pos += self.speed
            self.speed += self.acceleration

    def draw(self, screen):
        gfxdraw.filled_circle(screen, *self.pos.astype(int), self.radius, self.color)
        gfxdraw.aacircle(screen, *self.pos.astype(int), self.radius, self.color)

    def orbit(self, body):
        r = body.pos - self.pos
        d = sqrt(r.dot(r))
        # self.acceleration = np.array([0., 0.])
        self.speed += sqrt(G * body.mass / d**3) * \
            np.array([-r[1], r[0]]) * 1.1
