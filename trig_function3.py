""" trig_function3.py """
import sys
from math import sin, radians
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((800, 800))
FPSCLOCK = pygame.time.Clock()

def main():
    """ メインルーチン """
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((255, 255, 255))

        pygame.draw.line(SURFACE, (0, 0, 255), (0, 400), (800, 400), 2)
        pygame.draw.line(SURFACE, (0, 0, 255), (400, 0), (400, 800), 2)

        lines = []
        for theta in range(-360, 360):
            xpos = 800 * (theta+360) / 720
            ypos = (sin(radians(theta)) + \
                    sin(radians(theta*2))) * -200 + 400
            lines.append((xpos, ypos))
        pygame.draw.aalines(SURFACE, (0, 0, 0), False, lines)
        pygame.display.update()
        FPSCLOCK.tick(1)

if __name__ == '__main__':
    main()
