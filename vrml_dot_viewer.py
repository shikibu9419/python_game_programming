""" 3D VRML dot viewer - Copyright 2016 Kenichiro Tanaka """
import sys
import re
from math import sqrt
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()

def main(verts):
    """ main routine """
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Paint vertices
        SURFACE.fill((0, 0, 0))
        for vert in verts:
            zpos = vert[2] + 3000
            xpos = int(vert[0] * 1600 / zpos + 300)
            ypos = int(-vert[1] * 1600 / zpos + 300)
            pygame.draw.line(SURFACE, (0, 225, 0), 
                             (xpos, ypos), (xpos, ypos), 1)

        pygame.display.update()
        FPSCLOCK.tick(5)

def read_file(file):
    """ read VRML (wrl) file """
    with open(file, "rt") as fin:
        content = fin.read()

    match = re.search(r"point\s+\[([^\]]+)", content)
    pts = re.split(r"[\s,]+", match.group(1).strip())

    verts = []
    for index in range(0, len(pts), 3):
        verts.append([float(pts[index]),
                      float(pts[index+1]),
                      float(pts[index+2])])
    verts = auto_scale(verts)
    return verts

def auto_scale(verts):
    """ change scale to fill the screen """
    max_dist = 0
    for vert in verts:
        dist = sqrt(vert[0]**2 + vert[1]**2 + vert[2]**2)
        max_dist = max(dist, max_dist)
        scale = 600 / max_dist
    return [(x[0]*scale, x[1]*scale, x[2]*scale) for x in verts]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        VERTS = read_file(sys.argv[1])
        main(VERTS)
    else:
        print("Usage: python {} VRML-FILE".format(sys.argv[0]))
