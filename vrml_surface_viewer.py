""" 3D VRML surface viewer - Copyright 2016 Kenichiro Tanaka """
import sys
import re
from math import sqrt, sin, cos, floor
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()

class Vec3:
    """ 3D vector """
    def __init__(self, xpos, ypos, zpos):
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos

    def normalize(self):
        """ normalize this vector """
        length = sqrt(self.xpos**2 + self.ypos**2 + self.zpos**2)
        scale = 1 / length if length != 0 else 0
        self.xpos *= scale
        self.ypos *= scale
        self.zpos *= scale
        return self

class Surface:
    """ object for each surface """
    def __init__(self, indices):
        self.indices = indices
        self.norm = Vec3(1, 0, 0)
        self.zpos = 1
        self.pos = []

    def update(self, verts):
        """ update normal vector and zposition with vertices """
        self.pos = []
        ztotal = 0
        for index in self.indices:
            self.pos.append(verts[index])
            ztotal += verts[index][2]
        self.zpos = ztotal / len(self.indices)

        pos0 = verts[self.indices[0]]
        pos1 = verts[self.indices[1]]
        pos2 = verts[self.indices[2]]

        vec1 = Vec3(pos0[0]-pos1[0], pos0[1]-pos1[1],
                    pos0[2]-pos1[2])
        vec2 = Vec3(pos0[0]-pos2[0], pos0[1]-pos2[1],
                    pos0[2]-pos2[2])
        norm = Vec3(vec1.ypos*vec2.zpos - vec1.zpos*vec2.ypos, \
                    vec1.zpos*vec2.xpos - vec1.xpos*vec2.zpos, \
                    vec1.xpos*vec2.ypos - vec1.ypos*vec2.xpos)
        self.norm = norm.normalize()

def main(verts, polygons):
    """ main routine """
    light = Vec3(0.5, -0.8, -0.2).normalize()
    rot_x = 0.01
    rot_y = 0.03
    surfaces = []
    for poly in polygons:
        surfaces.append(Surface(poly))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # rotate vertices
        cval, sval = cos(rot_y), sin(rot_y)
        mrot_y = [cval, 0, sval, 0, 1, 0, -sval, 0, cval]
        cval, sval = cos(rot_x), sin(rot_x)
        mrot_x = [1, 0, 0, 0, cval, -sval, 0, sval, cval]
        rotate(verts, mrot_x, mrot_y)

        surfaces = sorted(surfaces, key=lambda x: x.zpos)
        for surface in surfaces:
            surface.update(verts)

        # Paint vertices
        SURFACE.fill((0, 0, 0))
        for surf in surfaces:
            ratio = surf.norm.xpos * light.xpos + \
                    surf.norm.ypos * light.ypos + \
                    surf.norm.zpos * light.zpos
            col = floor((ratio + 1) / 2 * 255)

            pts = []
            for pos in surf.pos:
                zpos = pos[2] + 5000
                xpos = pos[0] * 2500 / zpos + 300
                ypos = -pos[1] * 2500 / zpos + 300
                pts.append((xpos, ypos))
            pygame.draw.polygon(SURFACE, (col, col, col), pts)

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
    pts = re.split(r"[\s,]+",
                   match.group(1).strip('\t\n\x0b\x0c\r ,'))

    verts = []
    for index in range(0, len(pts), 3):
        verts.append([float(pts[index]),
                      float(pts[index+1]),
                      float(pts[index+2])])
    verts = auto_scale(verts)

    # get coordIndex (index of vertices, separated by -1)
    match = re.search(r"coordIndex\s+\[([^\]]+)", content)
    coords = re.split(r"[\s,]+",
                      match.group(1).strip('\t\n\x0b\x0c\r ,'))

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
