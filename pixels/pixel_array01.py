""" pixel_array01.py """
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((250, 250))
FPSCLOCK = pygame.time.Clock()

def process_pixels(data):
    """ process pixels """
    for ypos in range(250):
        for xpos in range(250):
            data[ypos][xpos] = (0, xpos, ypos)

def main():
    """ main routine """
    src = pygame.Surface((250, 250))
    data = pygame.PixelArray(src)
    process_pixels(data)
    del data

    while True:
        for _ in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()
        SURFACE.blit(src, (0, 0))
        pygame.display.update()

if __name__ == '__main__':
    main()
