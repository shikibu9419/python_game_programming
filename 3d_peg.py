""" 3D Peg - Copyright 2016 Kenichiro Tanaka """
import sys
from math import sin, cos, floor, sqrt, degrees
from random import randint
import types
import pygame
from pygame.locals import QUIT, KEYDOWN,\
    K_LEFT, K_RIGHT, K_UP, K_DOWN
from tiny_2d import Engine, RectangleEntity, CircleEntity

def normalize(vec):
    """ normalize the vector tuple (make the length to 1) """
    scale = 1 / sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
    return (vec[0]*scale, vec[1]*scale, vec[2]*scale)

def get_norm_vec(pos1, pos2, pos3):
    """ get the normal vector from 3 vertices (tuples) """
    pvec = (pos1[0] - pos2[0], pos1[1] - pos2[1], pos1[2] - pos2[2])
    qvec = (pos1[0] - pos3[0], pos1[1] - pos3[1], pos1[2] - pos3[2])
    norm = (pvec[1]*qvec[2] - pvec[2]*qvec[1],
            pvec[2]*qvec[0] - pvec[0]*qvec[2],
            pvec[0]*qvec[1] - pvec[1]*qvec[0])
    return normalize(norm)

class Surface():
    """ object for each surface """
    def __init__(self, v0, v1, v2, v3):
        self.vert = (v0, v1, v2, v3)
        self.norm = (0, 0, 0)
        self.zpos = 0

    def update(self):
        """ update the normal vector of the surface """
        self.norm = get_norm_vec(self.vert[0],
                                 self.vert[1], self.vert[2])
        self.zpos = (self.vert[0][2] + self.vert[1][2] \
                     + self.vert[2][2] + self.vert[3][2]) / 4

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
        self.tag = tag
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
            self.surfaces.append(Surface(pos0, pos1, pos2, pos3))

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
            self.pos[i][0] = mrot_x[0] * ppos + mrot_x[1] * qpos\
                + mrot_x[2] * rpos
            self.pos[i][1] = mrot_x[3] * ppos + mrot_x[4] * qpos\
                + mrot_x[5] * rpos
            self.pos[i][2] = mrot_x[6] * ppos + mrot_x[7] * qpos\
                + mrot_x[8] * rpos  - camera_z

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
        CAMERA_THETA[0] = max(1.0, min(1.3, CAMERA_THETA[0]))
        CAMERA_THETA[1] = max(-0.5, min(0.5, CAMERA_THETA[1]))

def tick():
    """ called periodically from the main loop """
    eventloop()

    cval, sval = cos(CAMERA_THETA[1]), sin(CAMERA_THETA[1])
    mrot_y = [cval, 0, sval, 0, 1, 0, -sval, 0, cval]
    cval, sval = cos(CAMERA_THETA[0]), sin(CAMERA_THETA[0])
    mrot_x = [1, 0, 0, 0, cval, -sval, 0, sval, cval]

    ENGINE.set_gravity(-CAMERA_THETA[1] * 20, -CAMERA_THETA[0] * 5)
    ENGINE.step(0.01)

    if BALL.ypos < 0 or BALL.ypos > 1200:
        BALL.xpos = randint(0, 300) + 100
        BALL.ypos = 1000

    IMAGES[0] = Cube(BALL.xpos, BALL.ypos, 0, 10, 10, 10, "ball")
    for cube in CUBES:
        cube.set_camera(300, 300, -1500, mrot_x, mrot_y)
    for pin in IMAGES:
        pin.set_camera(300, 300, -1500, mrot_x, mrot_y)

def paint():
    """ update the surface """
    SURFACE.fill((0, 0, 0))

    # draw bars on both sides
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
            xpos = int(xpos * 1200 / zpos + 300)
            ypos = int(-ypos * 1200 / zpos + 300)
            pts.append((xpos, ypos))

        if len(pts) > 3:
            pygame.draw.polygon(SURFACE, (rval, gval, bval), pts)

    # draw pins
    surfaces = []
    for pin in IMAGES:
        surf = pin.surfaces[1]
        surf.tag = pin.tag
        surfaces.append(surf)
    surfaces = sorted(surfaces, key=lambda x: x.zpos, reverse=True)

    for surf in surfaces:
        (xpos, ypos, zpos) = (surf.vert[0][0],
                              surf.vert[0][1], surf.vert[0][2])
        if zpos < 10:
            continue
        xpos = int(xpos * 1200 / zpos + 300)
        ypos = int(-ypos * 1200 / zpos + 300)
        scale = (4000-zpos)/20000
        if surf.tag == "ball":
            draw_rotate_center(PNGS[2], xpos, ypos, 0, scale)
        elif surf.tag == "pin0":
            draw_rotate_center(PNGS[0], xpos, ypos,
                               degrees(CAMERA_THETA[1]), scale)
        elif surf.tag == "pin1":
            draw_rotate_center(PNGS[1], xpos, ypos,
                               degrees(CAMERA_THETA[1]), scale)

    pygame.display.update()

def draw_rotate_center(image, xpos, ypos, theta, zoom):
    """ rotate image """
    rotate_sprite = pygame.transform.rotozoom(image, theta, zoom)
    rect = rotate_sprite.get_rect()
    SURFACE.blit(rotate_sprite, (xpos-(rect.width/2),
                 ypos-(rect.height/2)))

def onhit(self, peer):
    """ callback function when a pin is hit by the ball """
    self.pin.tag = "pin1"

def main():
    """ main routine """
    cubedata = [
        {"xpos": 25, "ypos": 600, "width": 25, "height": 600},
        {"xpos": 575, "ypos": 600, "width": 25, "height": 600},
    ]

    for cube in cubedata:
        xpos, ypos, width, height = cube["xpos"], cube["ypos"],\
            cube["width"], cube["height"]
        CUBES.append(Cube(xpos, ypos, 0, width, height, 25, "cube"))
        cube_obj = RectangleEntity(xpos - width, ypos - height,
                                   width * 2, height * 2)
        ENGINE.entities.append(cube_obj)

    ENGINE.entities.append(BALL)
    IMAGES.append(Cube(0, 0, 0, 15, 15, 15, "ball"))

    for yindex in range(5):
        for xindex in range(7 + yindex%2):
            xpos = xindex * 60 + (95 if yindex % 2 == 1 else 120)
            ypos = yindex * 150 + 100
            pin = Cube(xpos, ypos, 0, 10, 10, 10, "pin0")
            IMAGES.append(pin)
            pin_obj = CircleEntity(xpos, ypos, 10, True, 0.8)
            pin_obj.pin = pin
            pin_obj.onhit = types.MethodType(onhit, pin_obj)
            ENGINE.entities.append(pin_obj)

    while True:
        tick()
        paint()
        FPSCLOCK.tick(30)

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()
ENGINE = Engine(-100, -100, 800, 1400, 0, 0)
BALL = CircleEntity(randint(0, 300) + 100, 1000, 15, False, 0.9)
CUBES = []
IMAGES = []
CAMERA_THETA = [1.2, 0]
LIGHT = normalize([0.5, -0.8, -0.2])
PNGS = (pygame.image.load("pin0.png"),
        pygame.image.load("pin1.png"),
        pygame.image.load("ball.png"))

if __name__ == '__main__':
    main()
