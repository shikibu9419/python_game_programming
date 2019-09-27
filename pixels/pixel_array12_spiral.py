""" pixel_array12_spiral.py """
import sys
from math import radians, cos, sin, floor, hypot
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((250, 250))
FPSCLOCK = pygame.time.Clock()

def process_pixels(src_data, dst_data):
    """ process pixels """
    distance = hypot(250, 250)
    scale = radians(360) / distance

    for ypos in range(250):
        for xpos in range(250):
            pos_x = xpos - 125
            pos_y = ypos - 125
            angle = hypot(pos_x, pos_y) * scale
            sin_v, cos_v = sin(angle), cos(angle)

            x_src = floor((pos_x*cos_v - pos_y*sin_v) + 125)
            y_src = floor((pos_x*sin_v + pos_y*cos_v) + 125)

            if 0 <= x_src < 250 and 0 <= y_src < 250:
                val = src_data[x_src][y_src]
                rval, gval, bval, _ = SURFACE.unmap_rgb(val)
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
