""" vector_add.py sample """
import sys
from math import floor
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

pygame.init()
SURFACE = pygame.display.set_mode((500, 500))
FPSCLOCK = pygame.time.Clock()

def main():
    """ main routine """
    count = 0
    pos0 = (0, 0)
    pos1 = (0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                xpos = floor((event.pos[0] - 240) / 25)
                ypos = floor((event.pos[1] - 240) / 25)
                if count % 2 == 0:
                    pos0 = (xpos, ypos)
                    pos1 = (0, 0)
                else:
                    pos1 = (xpos, ypos)
                count += 1

        # Paint
        SURFACE.fill((0, 0, 0))
        for ypos in range(0, 500, 25):
            for xpos in range(0, 500, 25):
                pygame.draw.ellipse(SURFACE, (64, 64, 64),
                                    (xpos, ypos, 2, 2))
        pygame.draw.line(SURFACE, (255, 0, 0),
                         (250, 0), (250, 500), 3)
        pygame.draw.line(SURFACE, (255, 0, 0),
                         (0, 250), (500, 250), 3)

        coord0 = pos0[0] * 25 + 250, pos0[1] * 25 + 250
        pygame.draw.line(SURFACE, (0, 255, 0),
                         (250, 250), coord0, 2)

        coord1 = pos1[0] * 25 + 250, pos1[1] * 25 + 250
        pygame.draw.line(SURFACE, (0, 255, 255),
                         (250, 250), coord1, 2)

        coord2 = ((pos0[0] + pos1[0]) * 25 + 250,
                  (pos0[1] + pos1[1]) * 25 + 250)
        pygame.draw.line(SURFACE, (255, 0, 255),
                         (250, 250), coord2, 3)

        pygame.display.update()
        FPSCLOCK.tick(10)

if __name__ == '__main__':
    main()
