from operator import add, mul
from itertools import repeat
import re
import pygame as pg

pattern = re.compile(r"< ?(-?\d+),  ?(-?\d+)>")


def simulate(points, steps):
    for i, p in enumerate(points):
        distance = map(mul, p[1], repeat(steps))
        points[i] = (tuple(map(add, p[0], distance)), p[1])


def move(points, xy):
    for i, p in enumerate(points):
        points[i] = (tuple(map(add, p[0], xy)), p[1])


def parse(line):
    print(line)
    m = pattern.findall(line)

    return tuple(map(int, m[0])), tuple(map(int, m[1]))


def printmap(screen, points):
    for p in points:
        pg.draw.rect(screen, (0, 0, 0), (*p[0], 2, 2))


if __name__ == '__main__':

    with open("input.txt", "r") as f:
        li = [parse(line) for line in f]
    simulate(li, 10000)
    move(li, (200, 200))
    pg.init()
    screen = pg.display.set_mode([800, 800])
    print(type(screen), screen)
    running = True
    clock = pg.time.Clock()
    sim_steps = 0

    simulate(li, 345)  # Found by manually checking with code below
    # Answer to part 2 is 10000+345
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                print(sim_steps)
        screen.fill((255, 255, 255))
        printmap(screen, li)

        pressed = pg.key.get_pressed()

        if pressed[pg.K_RIGHT]:
            simulate(li, 1)
            sim_steps += 1
        if pressed[pg.K_LEFT]:
            simulate(li, -1)
            sim_steps -= 1
        if pressed[pg.K_w]:
            move(li, (0, -1))

        if pressed[pg.K_d]:
            move(li, (1, 0))

        if pressed[pg.K_s]:
            move(li, (0, 1))

        if pressed[pg.K_a]:
            move(li, (-1, 0))

        pg.display.flip()
        pg.display.update()
        clock.tick(30)
