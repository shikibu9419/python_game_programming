import cProfile
import re



import pygame, sys, math, random
from pygame.locals import *
from math import *

pygame.init()
SURFACE = pygame.display.set_mode([600,600])
FPSCLOCK = pygame.time.Clock()

class Vec3:
    def __init__(self, x, y, z):
        (self.x, self.y, self.z) = (x, y, z)

    def normalize(self):
        scale = 1 / sqrt(self.x**2 + self.y**2 + self.z**2)
        self.x *= scale
        self.y *= scale
        self.z *= scale
        return self

counter = 0
cameraY = 50
(W,H) = (13,13)
(xpos, xposNext) = (1, 1)
(zpos, zposNext) = (1, 1)
(dir, dirNext) = (1, 1)
light = Vec3(0.5, -0.8, -0.2).normalize()
FPS = 30
cubes = []

class Surface:
    def __init__(self, vertices, i, type):
        self.pos = vertices
        self.type = type
        p1 = vertices[0]
        p2 = vertices[1]
        p3 = vertices[2]
        p4 = vertices[3]
        p = Vec3(p1.x-p2.x, p1.y-p2.y, p1.z-p2.z)
        q = Vec3(p1.x-p3.x, p1.y-p3.y, p1.z-p3.z)
        n = Vec3(p.y*q.z - p.z*q.y, p.z*q.x - p.x*q.z, p.x*q.y - p.y*q.x)
        self.norm = n.normalize()
        self.cZ = (p1.z+p2.z+p3.z+p4.z) / 4
        if i == 0:
            self.cZ -= 1    # pull the top surface a bit to paint last

class Cube:
    pos = []
    polygons = [
        [2, 1, 5, 6], [0, 1, 2, 3], [4, 5, 1, 0],
        [2, 6, 7, 3], [7, 6, 5, 4], [0, 3, 7, 4]
    ]    

    def __init__(self, x, y, z, w, h, d, type):
        self.type = type
        self.vertices = [
            Vec3(x - w, y - h, z + d ),
            Vec3(x - w, y + h, z + d ),
            Vec3(x + w, y + h, z + d ),
            Vec3(x + w, y - h, z + d ),
            Vec3(x - w, y - h, z - d ),
            Vec3(x - w, y + h, z - d ),
            Vec3(x + w, y + h, z - d ),
            Vec3(x + w, y - h, z - d ),
        ]

    def getSurfaces(self):
        r = [] 
        for i in range(len(self.polygons)-1):
            indices = self.polygons[i]
            poly = []
            for index in indices:
                poly.append(self.pos[index])
            r.append(Surface(poly, i, self.type))
        return r

    def setCamera(self, cameraX, cameraY, cameraZ, mRotX, mRotY):
        self.pos = []
        for c in self.vertices:
            a = c.x - cameraX
            b = c.y - cameraY
            c = c.z - cameraZ

            # rotate around Y axis
            p = mRotY[0] * a + mRotY[1] * b + mRotY[2] * c
            q = mRotY[3] * a + mRotY[4] * b + mRotY[5] * c
            r = mRotY[6] * a + mRotY[7] * b + mRotY[8] * c

            # rotate around X axis
            a = mRotX[0] * p + mRotX[1] * q + mRotX[2] * r
            b = mRotX[3] * p + mRotX[4] * q + mRotX[5] * r
            c = mRotX[6] * p + mRotX[7] * q + mRotX[8] * r

            self.pos.append(Vec3(a, b, c))                

def createMaze(w, h):
    m = [[0 for i in range(w)] for j in range(h)]
    for z in range(0, h):
        for x in range(0, w):
            if x in (0, w-1) or z in (0, h-1):
                m[z][x] = 1 
            if z%2 == 0 and x%2 == 0 and z > 1 and x > 1 and z < h-1 and x < w-1:
                m[z][x] = 1
                dir = random.randint(0, 3 if z == 2 else 2)
                (px, pz) = (x, z)
                if dir == 0:
                    pz += 1
                elif dir == 1:
                    px -= 1
                elif dir == 2:
                    px += 1
                elif dir == 3:
                    pz -= 1
                m[pz][px] = 1
    return m

def tick():
    global xpos, xposNext, zpos, zposNext, dir, dirNext, light, counter, cameraY
    for event in pygame.event.get():
        (dx, dz) = (0, 0)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                dirNext = dir + 1
            elif event.key == K_RIGHT:
                dirNext = dir - 1
            elif event.key == K_UP:
                dx = round(cos(dir*pi/2))
                dz = round(sin(dir*pi/2))
            elif event.key == K_DOWN:
                dx = -round(cos(dir*pi/2))
                dz = -round(sin(dir*pi/2))
            elif event.key == K_SPACE:
                cProfile.run('paint()')
                
            if maze[zpos + dz][xpos + dx] == 0:
                (xposNext, zposNext) = (xpos + dx*2, zpos + dz*2)

        if dirNext != dir or xposNext != xpos or zposNext != zpos:
            counter = 1
        
    
    cameraRotY = dir * pi / 2 - pi / 2;
    (cameraX, cameraZ) = (xpos * 100, zpos * 100)
    if counter > 0:
        cameraRotY += ((dirNext - dir) * counter / 10) * (pi / 2)
        cameraX += ((xposNext - xpos) * counter / 10) * 100
        cameraZ += ((zposNext - zpos) * counter / 10) * 100
        counter += 1
        if counter >= 10:
            dir = dirNext = (dirNext + 4) % 4
            xpos = xposNext
            zpos = zposNext
            counter = 0
    
    (c, s) = (cos(cameraRotY), sin(cameraRotY))
    mRotY = [c, 0, s, 0, 1, 0, -s, 0, c]
    mRotX = [1, 0, 0, 0, 1, 0, 0, 0, 1]
    [c.setCamera(cameraX, cameraY, cameraZ, mRotX, mRotY) for c in cubes]

def paint():
    global cubes

    # Paint polygons
    SURFACE.fill((0,0,0))
    surfaces = []
    [[surfaces.append(s) for s in cube.getSurfaces()] for cube in cubes]
    surfaces = sorted(surfaces, key=lambda x: x.cZ, reverse=True)

    for s in surfaces:
        d = s.norm.x*light.x + s.norm.y*light.y + s.norm.z*light.z
        (r, g, b) = (255,255,255)
        if s.type == "dot":
            (r, g, b) = (0, 255, 128)
        ratio = (d + 1) / 2
        (r, g, b) = (floor(r*ratio), floor(g*ratio), floor(b*ratio))
        pts = []
        for p in s.pos:
            if p.z <= 10:
                continue
            x = p.x * 1000 / p.z + 300
            y = -p.y * 1000 / p.z + 300
            pts.append((int(x), int(y)))
        if len(pts) > 3:
            pygame.draw.polygon(SURFACE, (r,g,b), pts)    
    
    pygame.display.update()


def main():
    global W, H, maze, cubes, FPS
    global xpos, xposNext, zpos, zposNext, dir, dirNext, light
    global cameraY, cameraRotY, JUMPSPEED, counter

    maze = createMaze(W,H)
    
    for z in range(0, H):
        for x in range(0, W):
            if maze[z][x] == 1:
                cubes.append(Cube(x*100-25,0,z*100-25,25,25,25,"wall"))
                cubes.append(Cube(x*100+25,0,z*100-25,25,25,25,"wall"))
                cubes.append(Cube(x*100-25,0,z*100+25,25,25,25,"wall"))
                cubes.append(Cube(x*100+25,0,z*100+25,25,25,25,"wall"))
            else:
                cubes.append(Cube(x*100,0,z*100,10,10,10,"dot"))
    
    while True:
        tick()
        paint()
        FPSCLOCK.tick(60)

if __name__ == '__main__':
    main()
