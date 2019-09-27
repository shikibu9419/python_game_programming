""" Pixel operation sample - Copyright 2016 Kenichiro Tanaka """
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode([250, 250])
FPSCLOCK = pygame.time.Clock()

def main():
    """ main routine """
    src = pygame.image.load("picture0.jpg").convert()
    data = pygame.PixelArray(src)
    data[:] = data[:, ::-1]
    del data
    while True:
        for _ in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()
        SURFACE.blit(src, (0, 0))
        pygame.display.update()

if __name__ == '__main__':
    main()
