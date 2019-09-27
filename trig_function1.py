""" trig_function1.py """
import sys
from math import sin, cos, radians
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((600, 600))
FPSCLOCK = pygame.time.Clock()

def main():
    """ メインルーチン """
    theta = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((255, 255, 255))

        pygame.draw.line(SURFACE, (0, 0, 0), (100, 0), (100, 600))
        pygame.draw.line(SURFACE, (0, 0, 0), (0, 100), (600, 100))
        pygame.draw.circle(SURFACE, (255, 0, 0), (100, 100), 70, 1)

        theta += 3
        cos_v = cos(radians(theta)) * 70
        sin_v = sin(radians(theta)) * 70
        pygame.draw.line(SURFACE, (255, 0, 0),
                         (100, 100), (100+cos_v, 100-sin_v))
        pygame.draw.line(SURFACE, (0, 0, 255),
                         (100+cos_v, 100-sin_v), (100+cos_v, 100))
        pygame.draw.line(SURFACE, (0, 255, 0),
                         (100+cos_v, 100-sin_v), (100, 100-sin_v))

        xpoints, ypoints = [], []
        for index in range(0, 500):
            xpoints.append(
                (index+100, -sin(radians(theta+index))*70+100))
            ypoints.append(
                (cos(radians(theta+index))*70+100, index+100))
        pygame.draw.aalines(SURFACE, (0, 255, 0), False, xpoints)
        pygame.draw.aalines(SURFACE, (0, 0, 255), False, ypoints)
        pygame.display.update()
        FPSCLOCK.tick(20)

if __name__ == '__main__':
    main()
