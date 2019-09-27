""" 3D VRML wireframe viewer - Copyright 2016 Kenichiro Tanaka """
import sys
import re
from math import sqrt
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((600, 600))
FPSCLOCK = pygame.time.Clock()

def main(verts, polygons):
    """ main routine """
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Paint vertices
        SURFACE.fill((0, 0, 0))
        for poly in polygons:
            pointlist = []
            for index in poly:
                pos = verts[index]
                zpos = pos[2] + 3000
                xpos = int(pos[0] * 1600 / zpos) + 300
                ypos = int(-pos[1] * 1600 / zpos) + 300
                pointlist.append((xpos, ypos))
            pygame.draw.lines(SURFACE, (0, 225, 0), True, pointlist)

        pygame.display.update()
        FPSCLOCK.tick(5)

def read_file(file):
    """ read VRML (wrl) file """
    with open(file, "rt") as fin:
        content = fin.read()

    # get points (vertices)
    match = re.search(r"point\s+\[([^\]]+)", content)
    pts = re.split(r"[\s,]+", match.group(1).strip())

    verts = []
    for index in range(0, len(pts), 3):
        verts.append([float(pts[index]),
                      float(pts[index+1]),
                      float(pts[index+2])])
    verts = auto_scale(verts)

    # get coordIndex (index of vertices, separated by -1)
    match = re.search(r"coordIndex\s+\[([^\]]+)", content)
    coords = re.split(r"[\s,]+", match.group(1).strip())

    temp = []
    polygon = []
    for index in coords:
        if index == "-1":
            polygon.append(temp)
            temp = []
        else:
            temp.append(int(index))

    return verts, polygon

def auto_scale(verts):
    """ change scale to fill the screen """
    max_dist = 0
    for vert in verts:
        dist = sqrt(vert[0]**2 + vert[1]**2 + vert[2]**2)
        max_dist = max(dist, max_dist)
        scale = 600 / max_dist
    return [[x[0]*scale, x[1]*scale, x[2]*scale] for x in verts]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        VERTS, POLYGONS = read_file(sys.argv[1])
        main(VERTS, POLYGONS)
    else:
        print("Usage: python {} VRML-FILE".format(sys.argv[0]))
