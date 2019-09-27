""" pixel_array02_invert.py """
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
            val = data[xpos][ypos]
            rval, gval, bval, _ = SURFACE.unmap_rgb(val)

            invert_r = rval ^ 0xff
            invert_g = gval ^ 0xff
            invert_b = bval ^ 0xff

            data[xpos][ypos] = (invert_r, invert_g, invert_b)

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
