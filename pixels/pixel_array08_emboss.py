""" pixel_array08_emboss.py """
import sys
from math import floor
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((250, 250))
FPSCLOCK = pygame.time.Clock()

def process_pixels(src_data, dst_data):
    """ process pixels """
    bg_r, bg_g, bg_b = 128, 128, 128
    power = 3

    for ypos in range(0, 250):

        for xpos in range(1, 250):

            val_l = src_data[xpos-1][ypos]  # left pixel
            val = src_data[xpos][ypos]  # target

            rval_l, gval_l, bval_l, _ \
                = SURFACE.unmap_rgb(val_l)

            rval, gval, bval, _ = SURFACE.unmap_rgb(val)

            rval = min(max(bg_r + floor((rval - rval_l) * power),
                           0), 255)
            gval = min(max(bg_g + floor((gval - gval_l) * power),
                           0), 255)
            bval = min(max(bg_b + floor((bval - bval_l) * power),
                           0), 255)

            dst_data[xpos][ypos] = (rval, gval, bval)

def main():
    """ main routine """
    src = pygame.image.load("picture0.jpg").convert()
    dst = pygame.Surface((250, 250))
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
