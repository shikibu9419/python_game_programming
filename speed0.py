""" speed0.py """
import sys
import pygame
from pygame.locals import QUIT, Rect

pygame.init()
SURFACE = pygame.display.set_mode((600, 600))
FPSCLOCK = pygame.time.Clock()

def main():
    """ メインルーチン """
    pos_x = 0
    velocity_x = 5
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((0, 0, 0))
        pos_x += velocity_x
        if pos_x > 600:
            pos_x = 0

        pygame.draw.rect(SURFACE, (255, 255, 255),
                         Rect(pos_x, 200, 10, 10))

        pygame.display.update()
        FPSCLOCK.tick(10)

if __name__ == '__main__':
    main()
