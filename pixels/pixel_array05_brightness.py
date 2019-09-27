""" pixel_array05_brightness.py """
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((250, 250))
FPSCLOCK = pygame.time.Clock()

def process_pixels(data):
    """ process pixels """
    brightness = 1.5

    for ypos in range(250):
        for xpos in range(250):
            val = data[xpos][ypos]

            rval, gval, bval, _ = SURFACE.unmap_rgb(val)

            rval = max(0, min(255, int(rval * brightness)))
            gval = max(0, min(255, int(gval * brightness)))
            bval = max(0, min(255, int(bval * brightness)))

            data[xpos][ypos] = (rval, gval, bval)

def main():
    """ main routine """
    src = pygame.image.load("picture0.jpg").convert()
    data = pygame.PixelArray(src)
    process_pixels(data)
    del data

    while True:
        for _ in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()
        SURFACE.blit(src, (0, 0))
        pygame.display.update()
        FPSCLOCK.tick(5)

if __name__ == '__main__':
    main()
