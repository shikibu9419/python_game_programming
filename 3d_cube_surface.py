""" 3D Cube Surface - Copyright 2016 Kenichiro Tanaka """
import sys
from math import sin, cos, sqrt, floor
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
        scale = 1 / sqrt(self.xpos**2 + self.ypos**2 + self.zpos**2)
        self.xpos *= scale
        self.ypos *= scale
        self.zpos *= scale
        return self

class Surface:
    """ object for each surface """
    def __init__(self, vertices):
        self.pos = vertices
        pos1 = vertices[0]
        pos2 = vertices[1]
        pos3 = vertices[2]
        pos4 = vertices[3]

        vec1 = Vec3(pos1["x"]-pos2["x"], pos1["y"]-pos2["y"], pos1["z"]-pos2["z"])
        vec2 = Vec3(pos1["x"]-pos3["x"], pos1["y"]-pos3["y"], pos1["z"]-pos3["z"])
        norm = Vec3(vec1.ypos*vec2.zpos - vec1.zpos*vec2.ypos, \
                    vec1.zpos*vec2.xpos - vec1.xpos*vec2.zpos, \
                    vec1.xpos*vec2.ypos - vec1.ypos*vec2.xpos)

        self.norm = norm.normalize()
        self.zpos = (pos1["z"] + pos2["z"] + pos3["z"] + pos4["z"]) / 4

class Cube:
    """ 3D Cube model """
    polygons = [
        [2, 1, 5, 6], [0, 1, 2, 3], [4, 5, 1, 0],
        [2, 6, 7, 3], [7, 6, 5, 4], [0, 3, 7, 4]
    ]

    def __init__(self, x, y, z, w, h, d):
        self.pos = []
        self.vertices = [
            {"x": x - w, "y": y - h, "z": z + d},
            {"x": x - w, "y": y + h, "z": z + d},
            {"x": x + w, "y": y + h, "z": z + d},
            {"x": x + w, "y": y - h, "z": z + d},
            {"x": x - w, "y": y - h, "z": z - d},
            {"x": x - w, "y": y + h, "z": z - d},
            {"x": x + w, "y": y + h, "z": z - d},
            {"x": x + w, "y": y - h, "z": z - d},
        ]

    def set_camera(self, camera_z, mrot_x, mrot_y):
        """ set camera location and update vertices positions """

        self.pos.clear()
        for vert in self.vertices:
            xpos = vert["x"]
            ypos = vert["y"]
            zpos = vert["z"]

            # rotate around Y axis
            ppos = mrot_y[0] * xpos + mrot_y[1] * ypos + mrot_y[2] * zpos
            qpos = mrot_y[3] * xpos + mrot_y[4] * ypos + mrot_y[5] * zpos
            rpos = mrot_y[6] * xpos + mrot_y[7] * ypos + mrot_y[8] * zpos

            # rotate around X axis
            xpos = mrot_x[0] * ppos + mrot_x[1] * qpos + mrot_x[2] * rpos
            ypos = mrot_x[3] * ppos + mrot_x[4] * qpos + mrot_x[5] * rpos
            zpos = mrot_x[6] * ppos + mrot_x[7] * qpos + mrot_x[8] * rpos

            self.pos.append({"x": xpos, "y": ypos, "z": zpos - camera_z})

    def get_surfaces(self):
        """ return all surfaces of the cube """
        surfaces = []
        for indices in self.polygons:
            poly = []
            for index in indices:
                poly.append(self.pos[index])
            surfaces.append(Surface(poly))
        return surfaces

def main():
    """ main routine """
    rot_x = 0
    rot_y = 0
    cube = Cube(0, 0, 0, 50, 50, 50)
    light = Vec3(0.5, -0.8, -0.2).normalize()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Rotate the Cube
        rot_y += 0.07
        rot_x += 0.1

        (cval, sval) = (cos(rot_y), sin(rot_y))
        mrot_y = [cval, 0, sval, 0, 1, 0, -sval, 0, cval]
        (cval, sval) = (cos(rot_x), sin(rot_x))
        mrot_x = [1, 0, 0, 0, cval, -sval, 0, sval, cval]

        cube.set_camera(1000, mrot_x, mrot_y)

        # Paint polygons
        SURFACE.fill((0, 0, 0))
        surfaces = sorted(cube.get_surfaces(), key=lambda x: x.zpos)
        for surf in surfaces:
            ratio = surf.norm.xpos * light.xpos + \
                    surf.norm.ypos * light.ypos + \
                    surf.norm.zpos * light.zpos
            col = floor((ratio + 1) / 2 * 255)
            pts = []
            for pos in surf.pos:
                zpos = pos["z"] + 500
                xpos = pos["x"] * 1000 / zpos + 300
                ypos = -pos["y"] * 1000 / zpos + 300
                pts.append((xpos, ypos))
            pygame.draw.polygon(SURFACE, (col, col, col), pts)

        pygame.display.update()
        FPSCLOCK.tick(30)

if __name__ == '__main__':
    main()
