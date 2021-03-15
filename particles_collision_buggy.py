from sys import exit

import random
from itertools import combinations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as fan
import math
import threading

particles = []

plt.style.use('fivethirtyeight')

width = 1.0
height = 1.0

class Particle:
    def __init__(self, plot, id, speed=0.01, size=None, vx=None, vy=None, ax=None, ay=None, mass=None, x=None, y=None):
        self.id = id
        self.x = x or random.random() * 0.9 + 0.05
        self.y = y or random.random() * 0.9 + 0.05
        self.size = size or random.random() * 0.03 + 0.01
        self.mass = mass or self.size
        self.color = (0, random.random(), random.random()*0.5+0.5, 1)
        self.patch = plot.add_patch(plt.Circle((self.x, self.y), self.size, color=self.color))
        if not vx == None:
            self.vx = vx
        else:
            self.vx = random.random() * speed
        if not vy == None:
            self.vy = vy
        else:
            self.vy = random.random() * speed
        self.mx = self.mass * self.vx
        self.my = self.mass * self.vy
        self.ax = ax or 0
        self.ay = ay or 0
    def update(self):
        self.vx = self.mx / self.mass
        self.vy = self.my / self.mass
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        if self.x > 1 - self.size:
            self.x = 1 - self.size
            self.mx = -self.mx
        if self.y > 1 - self.size:
            self.y = 1 - self.size
            self.my = -self.my
        if self.x < 0 + self.size:
            self.x = 0 + self.size
            self.mx = -self.mx
        if self.y < 0 + self.size:
            self.y = 0 + self.size
            self.my = -self.my
        self.patch.center = (self.x, self.y)

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(6, 6)
fig.patch.set_facecolor((0, 0, 0))

ax = plt.axes(xlim=(0, 1.0), ylim=(0, 1.0))
ax.set_facecolor((0, 0, 0))
ax.grid(False)

for i in range(10):
    particles.append(Particle(ax, i))

# particles.append(Particle(ax, 0, size=0.02, vx=0.0, vy=0.0, x=0.5, y=0.5, mass=1000))
# for i in range(5):
#     particles.append(Particle(ax, 0, size=0.01, vx=0.004, vy=0.0, x=random.random()*0.25+0.25, y=random.random()*0.25+0.75, mass=0.001))

# particles.append(Particle(ax, 0, size=0.01, vx=0.006, vy=0, x=0.5, y=0.75, mass=0.001))
# particles.append(Particle(ax, 0, size=0.01, vx=0.008, vy=0, x=0.4, y=0.75, mass=0.001))


def gforce(p1, p2):
    rvecx = p1.x - p2.x
    rvecy = p1.y - p2.y
    rmag = math.sqrt(rvecx**2 + rvecy**2 + 0.00001**2)
    rhatx = rvecx / rmag
    rhaty = rvecy / rmag
    fmag = 0.0000001 * p1.mass * p2.mass / rmag**2
    fx = -fmag * rhatx
    fy = -fmag * rhaty
    return fx, fy

def animate(t):
    # if t % 50 == 0:
    #     val = random.random()
    #     x = val * 0.011 + 0.011
    #     x = x * random.sample([-1, 1], 1)[0]
    #     y = 0.0
    #     # particles.append(Particle(ax, 0, size=0.01, vx=x, vy=y, x=0.5, y=0.75, mass=0.0))
    #     # particles.append(Particle(ax, 0, size=0.01, vx=x, vy=y, x=0.5, y=0.75, mass=0.0))
    #     particles.append(Particle(ax, 0, size=0.01, vx=x, vy=y, x=0.5, y=0.75, mass=0.0))
    # for p in particles[1:]:
    #     pfx, pfy = gforce(p, particles[0])
    #     p2fx, p2fy = gforce(particles[0], p)
    #
    #     p.mx = p.mx + pfx
    #     # particles[0].mx = particles[0].mx + p2fx
    #     p.my = p.my + pfy
    #     # particles[0].my = particles[0].my + p2fy
    #
    #     p.update()
        # particles[0].update()

    # for p1, p2 in combinations(particles, 2):
    #     p1fx, p1fy = gforce(p1, p2)
    #     p2fx, p2fy = gforce(p2, p1)
    #
    #     p1.mx = p1.mx + p1fx
    #     p2.mx = p2.mx + p2fx
    #     p1.my = p1.my + p1fy
    #     p2.my = p2.my + p2fy
    #
    #     p1.x = p1.x + p1.mx / p1.mass
    #     p1.y = p1.y + p1.my / p1.mass
    #     p2.x = p2.x + p2.mx / p2.mass
    #     p2.y = p2.y + p2.my / p2.mass
    #     p1.update_patch()
    #     p2.update_patch()
        # p1.x = p1.x + 0.1
        # p1.y = p1.y + 0.1

    for p1, p2 in combinations(particles[:], 2):
        x = p1.x - p2.x
        y = p1.y - p2.y
        z = math.sqrt(x**2 + y**2)
        if z < (p1.size + p2.size):
            print('collide')
            x = p1.x - p2.x
            y = p1.y - p2.y
            unx = x / math.sqrt(x**2 + y**2)
            uny = y / math.sqrt(x**2 + y**2)
            utx = -uny
            uty = unx
            v1n = p1.vx * unx + p1.vy * uny
            v1t = p1.vx * utx + p1.vy * uty
            v2n = p2.vx * unx + p2.vy * uny
            v2t = p2.vx * utx + p2.vy * uty

            v1tf = v1t
            v2tf = v2t
            v1nf = (v1n * (p1.mass - p2.mass) + 2.0 * p2.mass * v2n) / (p1.mass + p2.mass)
            v2nf = (v2n * (p2.mass - p1.mass) + 2.0 * p1.mass * v1n) / (p2.mass + p1.mass)

            v1nfx = v1nf * unx
            v1nfy = v1nf * uny
            v2nfx = v2nf * unx
            v2nfy = v2nf * uny

            v1tfx = v1tf * utx
            v1tfy = v1tf * uty
            v2tfx = v2tf * utx
            v2tfy = v2tf * uty

            p1.mx = (v1nfx + v1tfx) * p1.mass
            p1.my = (v1nfy + v1tfy) * p1.mass
            p2.mx = (v2nfx + v2tfx) * p2.mass
            p2.my = (v2nfy + v2tfy) * p2.mass

    for p in particles:
        p.update()



a = fan(plt.gcf(), animate, interval=20)

# plt.axis('scaled')
plt.show()
