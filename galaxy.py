import numpy as np
from math import sqrt, log
from pygame import gfxdraw
from random import randint, uniform

G = 6.67408 * 10**-11

SCALE = 10**6


def px_to_km(x):
    return int(x * SCALE)


def km_to_px(x):
    return int(x / SCALE)


class Galaxy:

    def __init__(self, size):
        self.bodies = []
        self.size = size

    def add_random(pos=None, mass_range=(5, 25), radius_range=(5, 25)):
        if not pos:
            pos = (randint(0, self.size[0]), randint(0, self.size[1]))

        b = Body(pos, randint(*radius_range), uniform(*mass_range),
                 color=(randint(0, 255), randint(0, 255), randint(0, 255)))
        self.add(b)

    def add(self, *args):
        for b in args:
            if type(b) == Body:
                self.bodies.append(b)

    def add_forces(self):
        for b1 in self.bodies:
            b1.acceleration = np.array([0., 0.])
            for b2 in self.bodies:
                if b1 is not b2:
                    d = b2.pos - b1.pos
                    r = np.sqrt(d.dot(d))
                    if r < 1:
                        force = 0
                    else:
                        force = d * G * b1.mass * b2.mass / r**3
                    b1.apply_force(force)

    def step(self, n=1):
        for _ in range(n):
            self.add_forces()
            for b1 in self.bodies:
                b1.step()
                # for b2 in self.bodies:
                    # self.test_collision(b1, b2)

    def draw(self, screen):
        for b in self.bodies:
            b.draw(screen)

    def test_collision(self, b1, b2):
        if b1 is not b2:
            r = b2.pos - b1.pos
            d = km_to_px(np.sqrt(r.dot(r)))
            r1 = int(log(b1.radius)*8-50)
            r2 = int(log(b2.radius)*8-50)
            if d < r1+r2:
                self.collide(b1, b2)

    def collide(self, b1, b2):
        if b1.mass > b2.mass:
            bigger, smaller = b1, b2
        else:
            bigger, smaller = b2, b1

        bigger.radius += smaller.radius
        bigger.mass += smaller.mass
        self.bodies.remove(smaller)


class Body:

    def __init__(self, pos, radius, mass, initial_speed=(0., 0.),
                 color=(255, 255, 255), static=False):
        self.pos = np.array([px_to_km(pos[0]), px_to_km(pos[1])]).astype(float)
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
        pixel_pos = [int(km_to_px(p)) for p in self.pos]
        pixel_radius = int(log(self.radius)*8-50)
        gfxdraw.filled_circle(screen, *pixel_pos, pixel_radius, self.color)
        gfxdraw.aacircle(screen, *pixel_pos, pixel_radius, self.color)

    def orbit(self, body):
        r = body.pos - self.pos
        d = sqrt(r.dot(r))
        if d != 0:
            self.acceleration = np.array([0., 0.])
            self.speed += sqrt(G * body.mass / d**3) * np.array([-r[1], r[0]])*1.2

    def distance_to(self, body):
        r = body.pos - self.pos
        return sqrt(r.dot(r))

    def set_distance_to(self, body, distance):
        r = body.pos - self.pos
        d = sqrt(r.dot(r))
        if d == 0:
            self.pos += np.array([distance, 0])
        else:
            self.pos += r * distance / d
