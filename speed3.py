""" speed3.py """
import sys
import pygame
from pygame.locals import QUIT, Rect

pygame.init()
SURFACE = pygame.display.set_mode((600, 600))
FPSCLOCK = pygame.time.Clock()

def main():
    """ メインルーチン """
    rect = Rect(0, 600, 10, 10)
    velocity = [5, -20]
    accel = (0, 0.5)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((0, 0, 0))
        velocity[1] += accel[1]
        rect.move_ip(velocity)

        if rect.x > 600:
            rect.x = 0
        if rect.y > 600:
            velocity[1] = -20

        pygame.draw.rect(SURFACE, (255, 255, 255), rect)

        pygame.display.update()
        FPSCLOCK.tick(10)

if __name__ == '__main__':
    main()
