""" trig_snow.py - Copyright 2016 Kenichiro Tanaka """
import sys
from math import sin
from random import uniform, random
import pygame
from pygame.locals import QUIT, Rect

pygame.init()
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()

class Snow():
    """ snow flake object """
    def __init__(self):
        self.xpos = uniform(0, 600)
        self.ypos = -10
        self.drift = random()
        self.speed = uniform(0, 5) + 1
        self.width = uniform(0, 3) + 2
        self.height = self.width
        self.theta = uniform(0, 100)
        self.radius = uniform(0, 10) + 3

    def draw(self):
        """ draw this snow flake """
        x_offset = sin(self.theta) * self.radius
        rect = Rect(self.xpos + x_offset, self.ypos,
                    self.width, self.height)
        color = int(self.width / 5 * 225)
        pygame.draw.ellipse(SURFACE, (color, color, color), rect)

    def move(self):
        """ move this snow flake """
        self.ypos += self.speed
        if self.ypos > 600:
            self.ypos = -5
        self.xpos += self.drift
        if self.xpos > 600:
            self.xpos = 0
        self.theta += 0.1

def main():
    """ main routine """
    counter = 0
    snows = []
    background = pygame.image.load("picture1.jpg")
    background = background.convert()
    background.set_alpha(64)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        counter += 1
        if counter % 10 == 0 and len(snows) < 100:
            snows.append(Snow())
        for snow in snows:
            snow.move()

        SURFACE.fill((0, 0, 0))
        SURFACE.blit(background, (0, 0))
        for snow in snows:
            snow.draw()

        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()
