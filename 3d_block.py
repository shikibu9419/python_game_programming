""" 3D Blocks - Copyright 2016 Kenichiro Tanaka """
import sys
import random
from math import sin, cos, floor, radians
import pygame
from pygame.locals import QUIT, K_LEFT, K_RIGHT, KEYDOWN

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()

class Cube:
    """ Cube for blocks and paddle """
    polygons = [
        [2, 1, 5, 6], [0, 1, 2, 3], [4, 5, 1, 0],
        [2, 6, 7, 3], [7, 6, 5, 4], [0, 3, 7, 4]
    ]

    def __init__(self, x, y, z, w, h, d, color):
        self.xpos = x
        self.ypos = y
        self.width = w
        self.height = h
        self.color = color
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

    def set_camera(self, rad_x, rad_y):
        "update vertice positions depending on camera location"
        self.pos.clear()
        for vert in self.vertices:
            p0x = vert["x"]
            p0y = vert["y"]
            p0z = vert["z"]

            # rotate around X axis
            p1x = p0x
            p1y = p0y * cos(rad_x) - p0z * sin(rad_x)
            p1z = p0y * sin(rad_x) + p0z * cos(rad_x)

            # rotate around Y axis
            p2x = p1x * cos(rad_y) + p1z * sin(rad_y)
            p2y = p1y
            p2z = -p1x * sin(rad_y) + p1z * cos(rad_y)

            self.pos.append({"x": p2x, "y": p2y, "z": p2z})

    def ishit(self, xpos, ypos):
        "return if (x,y) hits the block"
        return self.xpos-self.width < xpos < self.xpos+self.width \
            and self.ypos-self.height < ypos < self.ypos+self.height

    def translate(self, diffx, diffy):
        "move the block"
        self.xpos += diffx
        self.ypos += diffy
        for vert in self.vertices:
            vert["x"] += diffx
            vert["y"] += diffy

def tick():
    """ called periodically from the main loop """
    global SPEED, THETA, BLOCKS, MESSAGE
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                PADDLE.translate(-10, 0)
            elif event.key == K_RIGHT:
                PADDLE.translate(+10, 0)

    if not MESSAGE is None:
        return

    # move the ball
    diffx = cos(radians(THETA)) * SPEED
    diffy = sin(radians(THETA)) * SPEED
    BALL.translate(diffx, diffy)

    # hit any blocks?
    count = len(BLOCKS)
    BLOCKS = [x for x in BLOCKS if x == BALL or x == PADDLE \
        or not x.ishit(BALL.xpos, BALL.ypos)]

    if len(BLOCKS) != count:
        THETA = -THETA

    # hit ceiling, wall or paddle?
    if BALL.ypos > 800:
        THETA = -THETA
        SPEED = 10
    if BALL.xpos < -250 or BALL.xpos > 250:
        THETA = 180 - THETA
    if PADDLE.ishit(BALL.xpos, BALL.ypos):
        THETA = 90 + ((PADDLE.xpos - BALL.xpos) / PADDLE.width) * 80
    if BALL.ypos < -1200 and len(BLOCKS) > 2:
        MESSAGE = MESS1
    if len(BLOCKS) == 2:
        MESSAGE = MESS0

    # Rotate the Cube
    rad_y = PADDLE.xpos / 1000
    rad_x = 0.5 + BALL.ypos / 2000
    for block in BLOCKS:
        block.set_camera(rad_x, rad_y)

def paint():
    "update the screen"
    SURFACE.fill((0, 0, 0))

    # Paint polygons
    for block in BLOCKS:
        for indices in block.polygons:
            poly = []
            for index in indices:
                pos = block.pos[index]
                zpos = pos["z"] + 500
                xpos = pos["x"] * 500 / zpos + 300
                ypos = -pos["y"] * 500 / zpos + 500
                poly.append((xpos, ypos))
            pygame.draw.lines(SURFACE, block.color, True, poly)

    if not MESSAGE is None:
        SURFACE.blit(MESSAGE, (150, 400))
    pygame.display.update()

FPS = 40
SPEED = 5
THETA = 270 + floor(random.randint(-10, 10))
BLOCKS = []
BALL = Cube(0, 400, 0, 5, 5, 5, (255, 255, 0))
PADDLE = Cube(0, 0, 0, 30, 10, 5, (255, 255, 255))
MESSAGE = None
MYFONT = pygame.font.SysFont(None, 80)
MESS0 = MYFONT.render("Cleared!!!", True, (255, 255, 0))
MESS1 = MYFONT.render("Game Over!", True, (255, 255, 0))

def main():
    """ main routine """
    colors = [(255, 0, 0), (255, 165, 0), (242, 242, 0),
              (0, 128, 0), (128, 0, 128), (0, 0, 250)]

    for ypos in range(0, len(colors)):
        for xpos in range(-3, 4):
            block = Cube(xpos * 70, ypos * 50 + 450, 0,
                         30, 10, 5, colors[ypos])
            BLOCKS.append(block)

    BLOCKS.append(PADDLE)
    BLOCKS.append(BALL)

    while True:
        tick()
        paint()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
