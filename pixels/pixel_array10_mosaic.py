""" pixel_array10_mosaic.py """
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((250, 250))
FPSCLOCK = pygame.time.Clock()

def process_pixels(src_data, dst_data):
    """ process pixels """
    for ypos in range(0, 250, 10):
        for xpos in range(0, 250, 10):
            r_total, g_total, b_total = 0, 0, 0

            for y_offset in range(ypos, ypos+10):
                for x_offset in range(xpos, xpos+10):
                    val = src_data[x_offset][y_offset]
                    rval, gval, bval, _ = SURFACE.unmap_rgb(val)
                    r_total += rval
                    g_total += gval
                    b_total += bval

            rval = int(r_total / 100)
            gval = int(g_total / 100)
            bval = int(b_total / 100)
            for y_offset in range(ypos, ypos+10):
                for x_offset in range(xpos, xpos+10):
                    dst_data[x_offset][y_offset] = (rval, gval, bval)

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
