""" 3D Tank - Copyright 2016 Kenichiro Tanaka """
import sys
from random import randint
from math import sin, cos, atan2, pi
import pygame
from pygame.locals import Rect, QUIT, \
    KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((1000, 600))
RADAR = pygame.Surface((400, 400))
FPSCLOCK = pygame.time.Clock()
SHAPES = []
SHOTS = []
TANKS = []
CAMERA_THETA = 0
CAMERA = [0, 0]

def create_rotate_matrix(theta):
    """ create rotate matrix around Y-axis """
    cos_v = cos(theta)
    sin_v = sin(theta)
    return (cos_v, 0, sin_v, 0, 1, 0, -sin_v, 0, cos_v)

class Shape:
    """ Super class of all shape objects (Tank, Shot, Bang) """
    def __init__(self):
        self.model = None

    def set_camera(self, camera_x, camera_z, camera_matrix):
        """ set camera and updates the each vertex """
        self.model.translate(-camera_x, 0, -camera_z)
        self.model.apply(camera_matrix)

    def is_valid(self):
        """ return this shape is still valid or not """
        return True

    def get_color(self):
        """ get the color of this shape """
        return (255, 255, 255)

class Model:
    """ Class to hold original and current pos of vertices """
    def __init__(self, polygons):
        self.polygons = polygons
        self.work = []
        for vertices in polygons:
            tmp = []
            for vertex in vertices:
                tmp.append([vertex[0], vertex[1], vertex[2]])
            self.work.append(tmp)

    def reset(self):
        """ reset all coordinates of current positions """
        for ipos, vertices in enumerate(self.polygons):
            for jpos in range(len(vertices)):
                self.work[ipos][jpos][0] \
                    = self.polygons[ipos][jpos][0]
                self.work[ipos][jpos][1] \
                    = self.polygons[ipos][jpos][1]
                self.work[ipos][jpos][2] \
                    = self.polygons[ipos][jpos][2]

    def apply(self, matrix):
        """ apply a matrix and update coordinates """
        for vertices in self.work:
            for vertex in vertices:
                xpos = matrix[0] * vertex[0] + \
                    matrix[1] * vertex[1] + matrix[2] * vertex[2]
                ypos = matrix[3] * vertex[0] + \
                    matrix[4] * vertex[1] + matrix[5] * vertex[2]
                zpos = matrix[6] * vertex[0] + \
                    matrix[7] * vertex[1] + matrix[8] * vertex[2]
                vertex[0], vertex[1], vertex[2] = xpos, ypos, zpos

    def translate(self, move_x, move_y, move_z):
        """ move all coordinates """
        for vertices in self.work:
            for vertex in vertices:
                vertex[0] += move_x
                vertex[1] += move_y
                vertex[2] += move_z

class Shot(Shape):
    """ Bullet object shot by you """
    def __init__(self, xpos, zpos, theta):
        super().__init__()
        self.xpos = xpos
        self.zpos = zpos
        self.step = (-sin(theta) * 5, cos(theta) * 5)
        self.count = 0
        polygons = []
        polygons.append(((xpos, -5, zpos),
                         (xpos+self.step[0], -5, zpos+self.step[1])))
        self.model = Model(polygons)

    def update(self):
        """ move the model """
        self.model.reset()
        self.count += 1
        self.model.translate(self.step[0] * self.count, 0,
                             self.step[1] * self.count)

    def is_valid(self):
        """ return if this shot is still valid or not """
        return self.count < 30

    def get_x(self):
        """ return the x position of this bullet """
        return self.xpos + self.step[0] * self.count

    def get_z(self):
        """ return the z position of this bullet """
        return self.zpos + self.step[1] * self.count

class Tile(Shape):
    """ Tile object on the floor """
    def __init__(self):
        super().__init__()

        polygons = []
        for xpos in range(-200, 200, 10):
            for zpos in range(-200, 200, 10):
                polygons.append((
                    (xpos, -5, zpos),
                    (xpos + 10, -5, zpos),
                    (xpos + 10, -5, zpos + 10),
                    (xpos, -5, zpos + 10)))
        self.model = Model(polygons)

    def update(self):
        """ reset the coordinate of each vertex """
        self.model.reset()

    def get_color(self):
        """ return the color of the floor """
        return (255, 0, 0)

class Tank(Shape):
    """ Tank object """
    vert = [(-10, -5, -5), (-10, -5, +5), (10, -5, 0), (-8, 2, 0)]
    polygons = ((vert[0], vert[1], vert[2]),
                (vert[0], vert[1], vert[3]),
                (vert[1], vert[2], vert[3]),
                (vert[2], vert[0], vert[3]))

    def __init__(self):
        super().__init__()

        self.model = Model(self.polygons)
        self.valid = True
        self.xpos = 0
        self.zpos = 0
        self.theta = 0
        self.next_x = 0
        self.next_z = 0
        self.next_t = 0
        self.count = 0
        self.rotating = False
        self.matrix = None
        self.set_destination(randint(0, 400) - 200,
                             randint(0, 400) - 200, 0)

    def set_destination(self, xpos, zpos, theta):
        """ set the next destination to move to """
        self.xpos = xpos
        self.zpos = zpos
        self.theta = theta
        self.next_x = randint(0, 400) - 200
        self.next_z = randint(0, 400) - 200
        self.next_t = -atan2(self.next_z - self.zpos,
                             self.next_x - self.xpos)
        self.count = 0
        self.rotating = True
        self.matrix = create_rotate_matrix(self.next_t)

    def get_x(self):
        """ return the current x position """
        return self.xpos + (0 if self.rotating \
            else (self.next_x - self.xpos) * self.count / 100)

    def get_z(self):
        """ return the current z position """
        return self.zpos + (0 if self.rotating \
            else (self.next_z - self.zpos) * self.count / 100)

    def get_color(self):
        """ return the color of the tank """
        return (00, 255, 00)

    def is_valid(self):
        """ return if this tank is still alive """
        return self.valid

    def update(self):
        """ move the tank and check if this tank is shoot """
        self.model.reset()
        self.count += 1
        if self.rotating:
            direction = (self.next_t - self.theta) * self.count / 20\
                + self.theta
            self.matrix = create_rotate_matrix(direction)
            if self.count > 20:
                self.rotating = False
                self.count = 0

        self.model.apply(self.matrix)
        self.model.translate(self.get_x(), 0, self.get_z())

        if self.count > 100:
            self.set_destination(self.next_x,
                                 self.next_z, self.next_t)

        for shot in SHOTS:
            diffx = abs(self.get_x() - shot.get_x())
            diffz = abs(self.get_z() - shot.get_z())
            if diffx < 10 and diffz < 10:
                SHAPES.append(Bang(self))
                self.valid = False
                add_tank()

class Bang(Shape):
    """ Explosion object """
    def __init__(self, tank):
        super().__init__()
        pos0 = tank.model.work[0][0]
        pos1 = tank.model.work[0][1]
        pos2 = tank.model.work[0][2]
        pos3 = tank.model.work[1][2]
        polygons = (
            ((pos0[0], pos0[1], pos0[2]),
             (pos1[0], pos1[1], pos1[2])),
            ((pos1[0], pos1[1], pos1[2]),
             (pos2[0], pos2[1], pos2[2])),
            ((pos2[0], pos2[1], pos2[2]),
             (pos0[0], pos0[1], pos0[2])),
            ((pos0[0], pos0[1], pos0[2]),
             (pos3[0], pos3[1], pos3[2])),
            ((pos1[0], pos1[1], pos1[2]),
             (pos3[0], pos3[1], pos3[2])),
            ((pos2[0], pos2[1], pos2[2]),
             (pos3[0], pos3[1], pos3[2])))

        self.model = Model(polygons)
        self.count = 0
        self.colors = []
        for col in range(255, 0, -15):
            self.colors.append((0, col, 0))
        self.bangs = []
        for _ in range(12):
            self.bangs.append((randint(0, 20) - 10,
                               randint(0, 20) - 10, randint(0, 20) - 10))

    def update(self):
        """ update positions of explosion """
        self.model.reset()
        self.count += 1
        for num in range(12):
            vertex = self.model.work[num//2][num%2]
            vertex[0] += self.bangs[num][0] * self.count / 16
            vertex[1] += self.bangs[num][1] * self.count / 16
            vertex[2] += self.bangs[num][2] * self.count / 16

    def is_valid(self):
        """ return if still in the middle of the explosion """
        return self.count < 16

    def get_color(self):
        """ return the color of this explosion """
        return self.colors[self.count]

def tick():
    """ called periodically from the main loop """
    global CAMERA_THETA, SHAPES, SHOTS, TANKS
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                CAMERA_THETA += 0.1
            elif event.key == K_RIGHT:
                CAMERA_THETA -= 0.1
            elif event.key == K_UP:
                CAMERA[0] -= sin(CAMERA_THETA) * 3
                CAMERA[1] += cos(CAMERA_THETA) * 3
            elif event.key == K_DOWN:
                CAMERA[0] += sin(CAMERA_THETA) * 3
                CAMERA[1] -= cos(CAMERA_THETA) * 3
            elif event.key == K_SPACE:
                shot = Shot(CAMERA[0], CAMERA[1], CAMERA_THETA)
                SHOTS.append(shot)
                SHAPES.append(shot)

    camera_matrix = create_rotate_matrix(CAMERA_THETA)
    for shape in SHAPES:
        shape.update()
        shape.set_camera(CAMERA[0], CAMERA[1], camera_matrix)

    SHAPES = [x for x in SHAPES if x.is_valid()]
    SHOTS = [x for x in SHOTS if x.is_valid()]
    TANKS = [x for x in TANKS if x.is_valid()]

def add_tank():
    """ add a tank at random position """
    tank = Tank()
    TANKS.append(tank)
    SHAPES.append(tank)

def paint():
    "update the screen"
    SURFACE.fill((0, 0, 0))

    # Paint polygons
    for shape in SHAPES:
        polygons = shape.model.work
        for vertices in polygons:
            poly = []
            for vertex in vertices:
                zpos = vertex[2]
                if zpos <= 1:
                    continue
                poly.append((vertex[0] / zpos * 1000 + 300,
                             -vertex[1] / zpos * 1000 + 300))

            if len(poly) > 1:
                pygame.draw.lines(SURFACE, 
                                  shape.get_color(), True, poly)

    # Paint radar map
    xpos, zpos, theta = CAMERA[0], CAMERA[1], CAMERA_THETA
    RADAR.set_alpha(128)
    RADAR.fill((128, 128, 128))
    pygame.draw.arc(RADAR, (0, 0, 225),
                    Rect(xpos+100, -zpos+100, 200, 200),
                    theta-0.6+pi/2, theta+0.6+pi/2, 100)
    pygame.draw.rect(RADAR, (225, 0, 0),
                     Rect(xpos+200, -zpos+200, 5, 5))
    for tank in TANKS:
        pygame.draw.rect(RADAR, (0, 255, 0),
                         Rect(tank.get_x()+200, -tank.get_z()+200, 5, 5))
    for shot in SHOTS:
        pygame.draw.rect(RADAR, (225, 225, 225),
                         Rect(shot.get_x()+200, -shot.get_z()+200, 5, 5))
    scaled_radar = pygame.transform.scale(RADAR, (300, 300))
    SURFACE.blit(scaled_radar, (650, 50))
    pygame.display.update()

def main():
    """ main routine """
    SHAPES.append(Tile())
    for _ in range(6):
        add_tank()

    while True:
        tick()
        paint()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()
