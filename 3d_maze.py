""" 3D MAZE - Copyright 2016 Kenichiro Tanaka """
import sys
import random
from math import sin, cos, pi, sqrt, floor
import pygame
from pygame.locals import QUIT, KEYDOWN, \
    K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE

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

def create_maze(width, height):
    """ create maze data (0:empty 1:wall) """
    maze = [[0 for i in range(width)] for j in range(height)]
    for zpos in range(0, height):
        for xpos in range(0, width):
            if xpos in (0, width-1) or zpos in (0, height-1):
                maze[zpos][xpos] = 1
            if zpos%2 == 1 or xpos%2 == 1:
                continue
            if zpos > 1 and xpos > 1 and zpos < height-1 and \
               xpos < width-1:
                maze[zpos][xpos] = 1
                direction = random.randint(0, 3 if zpos == 2 else 2)
                (nextx, nextz) = (xpos, zpos)
                if direction == 0:
                    nextz += 1
                elif direction == 1:
                    nextx -= 1
                elif direction == 2:
                    nextx += 1
                elif direction == 3:
                    nextz -= 1
                maze[nextz][nextx] = 1
    return maze

class Surface():
    """ object for each surface """
    def __init__(self, v0, v1, v2, v3, tag, index):
        self.vert = (v0, v1, v2, v3)
        self.tag = tag
        self.index = index
        self.norm = (0, 0, 0)
        self.zpos = 0

    def update(self):
        """ update the normal vector of the surface """
        self.norm = get_norm_vec(self.vert[0],
                                 self.vert[1],
                                 self.vert[2])
        self.zpos = (self.vert[0][2] + self.vert[1][2] + \
                     self.vert[2][2] + self.vert[3][2]) / 4
        if self.index == 0:
            self.zpos -= 1

class Cube():
    """ 3D Cube model """
    polygons = (
        (2, 1, 5, 6), (0, 1, 2, 3), (4, 5, 1, 0),
        (2, 6, 7, 3), (7, 6, 5, 4), (0, 3, 7, 4)
    )

    def __init__(self, x, y, z, w, h, d, tag):
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

        for i in range(5):
            indices = self.polygons[i]
            pos0 = self.pos[indices[0]]
            pos1 = self.pos[indices[1]]
            pos2 = self.pos[indices[2]]
            pos3 = self.pos[indices[3]]
            self.surfaces.append(
                Surface(pos0, pos1, pos2, pos3, tag, i))

    def set_camera(self, camera_x, camera_y, camera_z,
                   mrot_x, mrot_y):
        """ set camera location and update vertices positions """
        for i in range(len(self.vertices)):
            vert = self.vertices[i]
            xpos = vert[0] - camera_x
            ypos = vert[1] - camera_y
            zpos = vert[2] - camera_z

            # rotate around Y axis
            ppos = mrot_y[0] * xpos + mrot_y[1] * ypos \
                + mrot_y[2] * zpos
            qpos = mrot_y[3] * xpos + mrot_y[4] * ypos \
                + mrot_y[5] * zpos
            rpos = mrot_y[6] * xpos + mrot_y[7] * ypos \
                + mrot_y[8] * zpos

            # rotate around X axis
            self.pos[i][0] = mrot_x[0] * ppos \
                + mrot_x[1] * qpos + mrot_x[2] * rpos
            self.pos[i][1] = mrot_x[3] * ppos \
                + mrot_x[4] * qpos + mrot_x[5] * rpos
            self.pos[i][2] = mrot_x[6] * ppos \
                + mrot_x[7] * qpos + mrot_x[8] * rpos

        for surface in self.surfaces:
            surface.update()

def eventloop():
    """ handle events in eventloop """
    global COUNTER, JUMPSPEED, CUBES
    (diffx, diffz) = (0, 0)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                TURN[1] = TURN[0] + 1
            elif event.key == K_RIGHT:
                TURN[1] = TURN[0] - 1
            elif event.key == K_UP:
                diffx = round(cos(TURN[0]*pi/2))
                diffz = round(sin(TURN[0]*pi/2))
            elif event.key == K_DOWN:
                diffx = -round(cos(TURN[0]*pi/2))
                diffz = -round(sin(TURN[0]*pi/2))
            elif event.key == K_SPACE and JUMPSPEED == 0:
                JUMPSPEED = 150

        if COUNTER != 0:
            continue

        if not (diffx == 0 and diffz == 0) and \
           (MAZE[ZPOS[0] + diffz][XPOS[0] + diffx] == 0):
            CUBES = [c for c in CUBES if not \
                (c.xpos/100 == XPOS[0]+diffx and \
                 c.zpos/100 == ZPOS[0]+diffz)]
            CUBES = [c for c in CUBES if not \
                (c.xpos/100 == XPOS[0]+diffx*2 and \
                 c.zpos/100 == ZPOS[0]+diffz*2)]
            (XPOS[1], ZPOS[1]) = (XPOS[0] + diffx*2,
                                  ZPOS[0] + diffz*2)

        if TURN[1] != TURN[0] or XPOS[1] != XPOS[0] or \
           ZPOS[1] != ZPOS[0]:
            COUNTER = 1

def tick():
    """ called periodically from the main loop """
    global COUNTER, CAMERAY, JUMPSPEED
    eventloop()

    camera_rot_y = TURN[0] * pi / 2 - pi / 2
    (camera_x, camera_z) = (XPOS[0] * 100, ZPOS[0] * 100)
    if COUNTER > 0:
        camera_rot_y += ((TURN[1] - TURN[0]) * COUNTER / 10) \
            * (pi / 2)
        camera_x += ((XPOS[1] - XPOS[0]) * COUNTER / 10) * 100
        camera_z += ((ZPOS[1] - ZPOS[0]) * COUNTER / 10) * 100
        COUNTER += 1
        if COUNTER >= 10:
            TURN[0] = TURN[1] = (TURN[1] + 4) % 4
            (XPOS[0], ZPOS[0]) = (XPOS[1], ZPOS[1])
            COUNTER = 0

    JUMPSPEED -= 4
    CAMERAY += JUMPSPEED
    if CAMERAY < 50:
        JUMPSPEED = 0
        CAMERAY = 50

    (cval, sval) = (cos(camera_rot_y), sin(camera_rot_y))
    mrot_y = [cval, 0, sval, 0, 1, 0, -sval, 0, cval]
    mrot_x = [1, 0, 0, 0, 1, 0, 0, 0, 1]
    if CAMERAY != 50:
        camera_rot_x = min(90, (CAMERAY - 50) / 20) * pi / 180
        (cval, sval) = (cos(-camera_rot_x), sin(-camera_rot_x))
        mrot_x = [1, 0, 0, 0, cval, -sval, 0, sval, cval]
    for cube in CUBES:
        cube.set_camera(camera_x, CAMERAY, camera_z,
                        mrot_x, mrot_y)

def paint():
    """ update the surface """
    # Paint polygons
    SURFACE.fill((0, 0, 0))
    surfaces = []
    for cube in CUBES:
        surfaces.extend(cube.surfaces)
    surfaces = sorted(surfaces, key=lambda x: x.zpos, reverse=True)

    for surf in surfaces:
        dot = surf.norm[0]*LIGHT[0] + surf.norm[1]*LIGHT[1] \
            + surf.norm[2]*LIGHT[2]
        ratio = (dot + 1) / 2
        (rval, gval, bval) = (0, 255, 128) \
            if surf.tag == "dot" else (255, 255, 255)
        (rval, gval, bval) = (floor(rval*ratio),
                              floor(gval*ratio), floor(bval*ratio))

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

    pygame.display.update()

def main():
    """ main routine """
    for zpos in range(0, H):
        for xpos in range(0, W):
            if MAZE[zpos][xpos] == 1:
                CUBES.append(Cube(xpos*100-25, 0, zpos*100-25,
                                  25, 25, 25, "wall"))
                CUBES.append(Cube(xpos*100+25, 0, zpos*100-25,
                                  25, 25, 25, "wall"))
                CUBES.append(Cube(xpos*100-25, 0, zpos*100+25,
                                  25, 25, 25, "wall"))
                CUBES.append(Cube(xpos*100+25, 0, zpos*100+25,
                                  25, 25, 25, "wall"))
            else:
                CUBES.append(Cube(xpos*100, 0, zpos*100,
                                  10, 10, 10, "dot"))

    while True:
        tick()
        paint()
        FPSCLOCK.tick(FPS)

pygame.init()
SURFACE = pygame.display.set_mode([600, 600])
SURFACE.convert()
FPSCLOCK = pygame.time.Clock()
(W, H) = (13, 13)
XPOS = [1, 1]
ZPOS = [1, 1]
TURN = [1, 1]
COUNTER = 0
CAMERAY = 50
JUMPSPEED = 0
LIGHT = normalize([0.5, -0.8, -0.2])
FPS = 30
CUBES = []
MAZE = create_maze(W, H)

if __name__ == '__main__':
    main()
