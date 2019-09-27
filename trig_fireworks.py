""" trig_firework.py - Copyright 2016 Kenichiro Tanaka """
import sys
from math import sin, cos, radians
from random import randint
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((800, 600))
FPSCLOCK = pygame.time.Clock()

class Firework():
    """ Firework object """
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
        self.initialize()

    def initialize(self):
        """ initialize the firework """
        self.count = 0
        self.scale = 0
        self.pos = [randint(0, 800), randint(0, 20) + 600]
        self.speed = [randint(-3, 3), randint(-10, -2)]

    def move(self):
        """ move this firework """
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.speed[0] /= 1.01
        self.speed[1] += 0.1

    def draw(self):
        """ draw this firework """
        if self.speed[1] < -1:
            posint = (int(self.pos[0]), int(self.pos[1]))
            pygame.draw.circle(SURFACE, self.color, posint, 1)
        else:
            self.count += 1
            for _ in range(4):
                self.scale += 0.06 / self.count
                rad = self.radius * self.scale
                for theta in range(0, 360, 36):
                    pos = (int(cos(radians(theta)) * rad \
                                + self.pos[0]),
                           int(sin(radians(theta)) * rad \
                                + self.pos[1]))
                    pygame.draw.circle(SURFACE, self.color, pos, 2)

            if self.count > 30:
                self.initialize()

def main():
    """ main routine """
    fires = []
    colors = ((255, 0, 0), (255, 255, 0), (225, 225, 225), \
        (255, 0, 255), (0, 255, 0), (128, 128, 255), (0, 255, 255))
    SURFACE.set_alpha(128)

    for index in range(14):
        fires.append(
            Firework(randint(0, 60) + 60, colors[index % 7]))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        for fire in fires:
            fire.move()

        surface = pygame.Surface((800, 600))
        surface.set_alpha(96)
        surface.fill((0, 0, 0))
        SURFACE.blit(surface, (0, 0))

        for fire in fires:
            fire.draw()

        pygame.display.update()
        FPSCLOCK.tick(10)

if __name__ == '__main__':
    main()
