""" trig_boat.py """
import sys
from math import sin, radians
import pygame
from pygame.locals import QUIT, Rect

pygame.init()
SURFACE = pygame.display.set_mode((600, 600))
FPSCLOCK = pygame.time.Clock()

def paint_wave(surface, theta, amplitude, color):
    """ paint the wave and returns the ypos of the boat """
    boat_y = 0
    points = [(0, 600)]
    for x_pos in range(0, 620, 20):
        y_pos = sin(radians(x_pos + theta)) * amplitude + 300
        points.append((x_pos, y_pos))
        if x_pos == 300:
            boat_y = y_pos
    points.append((600, 600))
    surface.fill((255, 255, 255))
    pygame.draw.polygon(surface, color, points)
    SURFACE.blit(surface, (0, 0))
    return boat_y

def main():
    """ メインルーチン """
    theta = 0
    surfaces = [pygame.Surface((800, 800)) for _ in range(3)]
    for surface in surfaces:
        surface.set_alpha(96)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((255, 255, 255))
        theta += 1
        ypos_0 = paint_wave(surfaces[0], theta,
                            40, (0, 0, 255))
        ypos_1 = paint_wave(surfaces[1], theta * 2.5,
                            30, (0, 0, 225))
        ypos_2 = paint_wave(surfaces[2], theta * 3.0,
                            20, (30, 0, 200))
        y_pos = min(ypos_0, min(ypos_1, ypos_2))

        pygame.draw.rect(SURFACE, (0, 128, 0),
                         Rect(275, y_pos-20, 50, 20))
        pygame.display.update()
        FPSCLOCK.tick(30)

if __name__ == '__main__':
    main()
