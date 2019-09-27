""" 3D Tilt - Copyright 2016 Kenichiro Tanaka """
import sys
from math import sin, cos, floor, sqrt, hypot
import pygame
from pygame.locals import QUIT, KEYDOWN, \
    K_LEFT, K_RIGHT, K_UP, K_DOWN
from tiny_2d import Engine, RectangleEntity, CircleEntity

def normalize(vec):
    """ normalize the vector (make the length 1) """
    scale = 1 / sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
    return (vec[0]*scale, vec[1]*scale, vec[2]*scale)

def get_norm_vec(pos1, pos2, pos3):
    """ get the normal vector from 3 vertices """
    pvec = (pos1[0] - pos2[0], pos1[1] - pos2[1], pos1[2] - pos2[2])
    qvec = (pos1[0] - pos3[0], pos1[1] - pos3[1], pos1[2] - pos3[2])
    norm = (pvec[1]*qvec[2] - pvec[2]*qvec[1],
            pvec[2]*qvec[0] - pvec[0]*qvec[2],
            pvec[0]*qvec[1] - pvec[1]*qvec[0])
    return normalize(norm)

class Surface():
    """ object for each surface """
    def __init__(self, v0, v1, v2, v3, near):
        self.vert = (v0, v1, v2, v3)
        self.norm = (0, 0, 0)
        self.near = near
        self.zpos = 0

    def update(self):
        """ update the normal vector of the surface """
        self.norm = get_norm_vec(self.vert[0],
                                 self.vert[1], self.vert[2])
        zpos = (self.vert[0][2] + self.vert[1][2] + \
                     self.vert[2][2] + self.vert[3][2]) / 4
        xpos = (self.vert[0][0] + self.vert[1][0] + \
                     self.vert[2][0] + self.vert[3][0]) / 4
        ypos = (self.vert[0][1] + self.vert[1][1] + \
                    self.vert[2][1] + self.vert[3][1]) / 4
        self.zpos = zpos + hypot(xpos, ypos)
        if self.near:
            self.zpos -= 100

class Cube():
    """ 3D Cube model """
    polygons = (
        (2, 1, 5, 6), (0, 1, 2, 3), (4, 5, 1, 0),
        (2, 6, 7, 3), (7, 6, 5, 4), (0, 3, 7, 4)
    )

    def __init__(self, x, y, z, w, h, d, near):
        self.xpos = x
        self.zpos = z
        self.pos = []
        self.surfaces = []
        self.vertices = (
            (x - w, y - h, z + d),
            (x - w, y + h, z + d),
            (x + w, y + h, z + d),
            (x + w, y - h, z + d),
            (x - w, y - h, z - d),
            (x - w, y + h, z - d),
            (x + w, y + h, z - d),
            (x + w, y - h, z - d),
        )

        for vert in self.vertices:
            self.pos.append([vert[0], vert[1], vert[2]])

        for i in range(6):
            indices = self.polygons[i]
            pos0 = self.pos[indices[0]]
            pos1 = self.pos[indices[1]]
            pos2 = self.pos[indices[2]]
            pos3 = self.pos[indices[3]]
            self.surfaces.append(Surface(pos0, pos1,
                                         pos2, pos3, near))

    def set_camera(self, camera_x, camera_y, camera_z,
                   mrot_x, mrot_y):
        """ set camera location and update vertices positions """
        for i in range(len(self.vertices)):
            vert = self.vertices[i]
            xpos = vert[0] - camera_x
            ypos = vert[1] - camera_y
            zpos = vert[2]

            # rotate around Y axis
            ppos = mrot_y[0] * xpos + mrot_y[1] * ypos \
                + mrot_y[2] * zpos
            qpos = mrot_y[3] * xpos + mrot_y[4] * ypos \
                + mrot_y[5] * zpos
            rpos = mrot_y[6] * xpos + mrot_y[7] * ypos \
                + mrot_y[8] * zpos

            # rotate around X axis
            self.pos[i][0] = mrot_x[0] * ppos + mrot_x[1] * qpos \
                + mrot_x[2] * rpos
            self.pos[i][1] = mrot_x[3] * ppos + mrot_x[4] * qpos \
                + mrot_x[5] * rpos
            self.pos[i][2] = mrot_x[6] * ppos + mrot_x[7] * qpos \
                + mrot_x[8] * rpos - camera_z

        for surface in self.surfaces:
            surface.update()

def eventloop():
    """ handle events in eventloop """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                CAMERA_THETA[1] -= 0.01
            elif event.key == K_RIGHT:
                CAMERA_THETA[1] += 0.01
            elif event.key == K_UP:
                CAMERA_THETA[0] += 0.01
            elif event.key == K_DOWN:
                CAMERA_THETA[0] -= 0.01
        CAMERA_THETA[0] = max(-0.1, min(0.1, CAMERA_THETA[0]))
        CAMERA_THETA[1] = max(-0.1, min(0.1, CAMERA_THETA[1]))

def tick():
    """ called periodically from the main loop """
    eventloop()

    cval, sval = cos(CAMERA_THETA[1]), sin(CAMERA_THETA[1])
    mrot_y = [cval, 0, sval, 0, 1, 0, -sval, 0, cval]
    cval, sval = cos(-CAMERA_THETA[0]), sin(-CAMERA_THETA[0])
    mrot_x = [1, 0, 0, 0, cval, -sval, 0, sval, cval]

    ENGINE.set_gravity(-CAMERA_THETA[1] * 20, CAMERA_THETA[0] * 20)
    ENGINE.step(0.01)

    for cube in CUBES:
        cube.set_camera(300, 300, -1000, mrot_x, mrot_y)

def paint():
    """ update the surface """
    SURFACE.fill((0, 0, 0))

    surfaces = []
    for cube in CUBES:
        surfaces.extend(cube.surfaces)
    surfaces = sorted(surfaces, key=lambda x: x.zpos, reverse=True)

    for surf in surfaces:
        dot = surf.norm[0]*LIGHT[0] + surf.norm[1]*LIGHT[1] \
            + surf.norm[2]*LIGHT[2]
        ratio = (dot + 1) / 2
        (rval, gval, bval) = (floor(255*ratio),
                              floor(255*ratio), floor(255*ratio))

        pts = []
        for i in range(4):
            (xpos, ypos, zpos) = (surf.vert[i][0],
                                  surf.vert[i][1], surf.vert[i][2])
            if zpos <= 10:
                continue
            xpos = int(xpos * 1000 / zpos + 300)
            ypos = int(-ypos * 1000 / zpos + 300)
            pts.append((xpos, ypos))

        if len(pts) > 3:
            pygame.draw.polygon(SURFACE, (rval, gval, bval), pts)

    SURFACE.blit(BALL_IMAGE, (BALL.xpos - 30, BALL.ypos - 30))
    pygame.display.update()

def main():
    """ main routine """
    cubedata = [
        {"x":25, "y":300, "w":25, "h":300, "near":0},
        {"x":575, "y":300, "w":25, "h":300, "near":0},
        {"x":300, "y":25, "w":250, "h":25, "near":1},
        {"x":300, "y":575, "w":250, "h":25, "near":1},
        {"x":250, "y":150, "w":200, "h":25, "near":1},
        {"x":350, "y":300, "w":200, "h":25, "near":1},
        {"x":250, "y":450, "w":200, "h":25, "near":1},
    ]

    for cube in cubedata:
        xpos, ypos, width, height = \
            cube["x"], cube["y"], cube["w"], cube["h"]
        CUBES.append(Cube(xpos, ypos, 0, width, height,
                          25, cube["near"]))
        cube_object = RectangleEntity(xpos-width,
                                      ypos-height, width*2, height*2)
        ENGINE.entities.append(cube_object)

    ENGINE.entities.append(BALL)

    while True:
        tick()
        paint()
        FPSCLOCK.tick(30)

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()
ENGINE = Engine(0, 0, 600, 600, 0, 0)
BALL = CircleEntity(100, 100, 30, False, 0.2)
CUBES = []
CAMERA_THETA = [0, 0]
LIGHT = normalize([0.5, -0.8, -0.2])
BALL_IMAGE = pygame.image.load("ball.png")
BALL_IMAGE = pygame.transform.scale(BALL_IMAGE, (60, 60))

if __name__ == '__main__':
    main()
