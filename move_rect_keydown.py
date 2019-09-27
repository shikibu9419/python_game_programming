""" Move Rectangle - Copyright 2016 Kenichiro Tanaka """
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, Rect

pygame.init()
SURFACE = pygame.display.set_mode([400, 300])
FPSCLOCK = pygame.time.Clock()
FPS = 30
WHITE = (255, 255, 255)

def main():
    """ main routine """
    paddle = Rect(150, 250, 100, 30)
    pygame.key.set_repeat(5, 5)

    while True:
        SURFACE.fill(WHITE)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    paddle.centerx -= 5
                elif event.key == K_RIGHT:
                    paddle.centerx += 5

        pygame.draw.rect(SURFACE, (255, 255, 0), paddle)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
