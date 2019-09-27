""" pixel_array07_edge.py """
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((250, 250))
FPSCLOCK = pygame.time.Clock()

def process_pixels(src_data, dst_data):
    """ process pixels """
    intensity = 10

    for ypos in range(1, 250):

        for xpos in range(1, 250):

            val_l = src_data[xpos-1][ypos]  # left pixel
            val_u = src_data[xpos][ypos-1]  # up pixel
            val = src_data[xpos][ypos]  # target

            rval_l, gval_l, bval_l, _ \
                = SURFACE.unmap_rgb(val_l)
            rval_u, gval_u, bval_u, _ \
                = SURFACE.unmap_rgb(val_u)
            rval, gval, bval, _ = SURFACE.unmap_rgb(val)

            rval = min((abs(rval_l - rval) \
                +abs(rval_u - rval)) * intensity, 255)
            gval = min((abs(gval_l - gval) \
                +abs(gval_u - gval)) * intensity, 255)
            bval = min((abs(bval_l - bval) \
                +abs(bval_u - bval)) * intensity, 255)

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
