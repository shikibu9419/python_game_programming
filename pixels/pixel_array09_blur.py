""" pixel_array09_blur.py """
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((250, 250))
FPSCLOCK = pygame.time.Clock()

def process_pixels(src_data, dst_data):
    """ process pixels """
    power = 2

    for ypos in range(0, 250):
        for xpos in range(0, 250):
            r_total, g_total, b_total = 0, 0, 0
            colors = 0

            for diff_y in range(-power, power+1):
                for diff_x in range(-power, power+1):
                    (pos_x, pos_y) = (xpos + diff_x, ypos + diff_y)
                    if 0 <= pos_x < 250 and 0 <= pos_y < 250:
                        val = src_data[pos_x][pos_y]
                        rval, gval, bval, _ = SURFACE.unmap_rgb(val)
                        r_total += rval
                        g_total += gval
                        b_total += bval
                        colors += 1

            rval = int(r_total / colors)
            gval = int(g_total / colors)
            bval = int(b_total / colors)
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

if __name__ == '__main__':
    main()
