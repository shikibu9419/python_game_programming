""" 3D VRML wireframe viewer (rotate) - Copyright 2016 Kenichiro Tanaka """
import sys
import re
from math import sqrt, sin, cos
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((600, 600))
FPSCLOCK = pygame.time.Clock()

def main(verts, polygons):
    """ main routine """
    rot_x = 0.01
    rot_y = 0.03

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # rotate vertices
        (cval, sval) = (cos(rot_y), sin(rot_y))
        mrot_y = [cval, 0, sval, 0, 1, 0, -sval, 0, cval]
        (cval, sval) = (cos(rot_x), sin(rot_x))
        mrot_x = [1, 0, 0, 0, cval, -sval, 0, sval, cval]
        rotate(verts, mrot_x, mrot_y)

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
        FPSCLOCK.tick(15)

def rotate(vertices, mrot_x, mrot_y):
    """ rotate all vertices """
    for vert in vertices:
        xpos = vert[0]
        ypos = vert[1]
        zpos = vert[2]

        # rotate around Y axis
        ppos = mrot_y[0] * xpos + mrot_y[1] * ypos \
            + mrot_y[2] * zpos
        qpos = mrot_y[3] * xpos + mrot_y[4] * ypos \
            + mrot_y[5] * zpos
        rpos = mrot_y[6] * xpos + mrot_y[7] * ypos \
            + mrot_y[8] * zpos

        # rotate around X axis
        vert[0] = mrot_x[0] * ppos + mrot_x[1] * qpos \
            + mrot_x[2] * rpos
        vert[1] = mrot_x[3] * ppos + mrot_x[4] * qpos \
            + mrot_x[5] * rpos
        vert[2] = mrot_x[6] * ppos + mrot_x[7] * qpos \
            + mrot_x[8] * rpos

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
