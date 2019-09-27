""" pixel_array06_wave0.py """
import sys
from math import pi, sin, floor
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((250, 250))
FPSCLOCK = pygame.time.Clock()

def process_pixels(src_data, dst_data):
    """ process pixels """
    waves = 4
    radius = 10
    wave_freq = (waves * pi * 2) / 250

    for xpos in range(250):
        y_offset = floor(sin(xpos * wave_freq) * radius)
        for ypos in range(250):
            if 0 <= ypos + y_offset < 250:
                val = src_data[xpos][ypos + y_offset]

                rval, gval, bval, _ = SURFACE.unmap_rgb(val)
                dst_data[xpos][ypos] = (rval, gval, bval)

def main():
    """ main routine """
    src = pygame.image.load("picture0.jpg").convert()
    dst = pygame.Surface((250, 250), 0, SURFACE)
    src_data = pygame.PixelArray(src)
    dst_data = pygame.PixelArray(dst)
    process_pixels(src_data, dst_data)
    del src_data
    del dst_data

    while True:
        for _ in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()
        SURFACE.blit(dst, (0, 0))
        pygame.display.update()
        FPSCLOCK.tick(5)

if __name__ == '__main__':
    main()
