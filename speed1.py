""" speed1.py """
import sys
import pygame
from pygame.locals import QUIT, Rect

pygame.init()
SURFACE = pygame.display.set_mode((600, 600))
FPSCLOCK = pygame.time.Clock()

def main():
    """ メインルーチン """
    rect = Rect(0, 0, 10, 10)
    velocity = (5, 2)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((0, 0, 0))
        rect.move_ip(velocity)
        if rect.x > 600:
            rect.x = 0
        if rect.y > 600:
            rect.y = 0

        pygame.draw.rect(SURFACE, (255, 255, 255), rect)

        pygame.display.update()
        FPSCLOCK.tick(10)

if __name__ == '__main__':
    main()
