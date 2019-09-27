""" 3D Cube Wireframe - Copyright 2016 Kenichiro Tanaka """
import sys
from math import sin, cos
import pygame
from pygame import QUIT

pygame.init()
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()

class Cube:
    """ 3D Cube model """
    pos = []
    polygons = [
        [2, 1, 5, 6], [0, 1, 2, 3], [4, 5, 1, 0],
        [2, 6, 7, 3], [7, 6, 5, 4], [0, 3, 7, 4]
    ]

    def __init__(self, x, y, z, w, h, d):
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

        self.pos = []
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

def main():
    """ main routine """
    rot_x = 0
    rot_y = 0
    cube = Cube(0, 0, 0, 50, 50, 50)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Rotate the Cube
        rot_y += 0.05
        rot_x += 0.1

        (cval, sval) = (cos(rot_y), sin(rot_y))
        mrot_y = [cval, 0, sval, 0, 1, 0, -sval, 0, cval]
        (cval, sval) = (cos(rot_x), sin(rot_x))
        mrot_x = [1, 0, 0, 0, cval, -sval, 0, sval, cval]

        cube.set_camera(1000, mrot_x, mrot_y)

        # Paint polygons
        SURFACE.fill((0, 0, 0))
        for indices in cube.polygons:
            poly = []
            for index in indices:
                pos = cube.pos[index]
                zpos = pos["z"] + 500
                xpos = pos["x"] * 1000 / zpos + 300
                ypos = -pos["y"] * 1000 / zpos + 300
                poly.append((xpos, ypos))
            pygame.draw.lines(SURFACE, (255, 255, 0), True, poly)

        pygame.display.update()
        FPSCLOCK.tick(30)

if __name__ == '__main__':
    main()
