import cProfile
import re

import pygame, sys, math, random
from pygame.locals import *
from math import *

def normalize(p):
    scale = 1 / sqrt(p[0]**2 + p[1]**2 + p[2]**2)
    return (p[0]*scale, p[1]*scale, p[2]*scale)

def getNormVec(p1, p2, p3):
    p = (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])
    q = (p1[0] - p3[0], p1[1] - p3[1], p1[2] - p3[2])
    n = (p[1]*q[2] - p[2]*q[1], p[2]*q[0] - p[0]*q[2], p[0]*q[1] - p[1]*q[0]) 
    return normalize(n)

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
 
pygame.init()
SURFACE = pygame.display.set_mode([600,600])
SURFACE.convert()
FPSCLOCK = pygame.time.Clock()
(W,H) = (13,13)
(xpos, xposNext) = (1,1)
(zpos, zposNext) = (1,1)
(dir, dirNext) = (1,1)
counter = 0
cameraY = 50
light = normalize([0.5, -0.8, -0.2])
FPS = 30
cubes = []
maze = createMaze(W,H)
JUMPSPEED = 0

class Cube:
    pos = []
    polygons = (
        (2, 1, 5, 6), (0, 1, 2, 3), (4, 5, 1, 0),
        (2, 6, 7, 3), (7, 6, 5, 4), (0, 3, 7, 4)
    )

    def __init__(self, x, y, z, w, h, d, type):
        self.type = type
        self.vertices = (
            (x - w, y - h, z + d ),
            (x - w, y + h, z + d ),
            (x + w, y + h, z + d ),
            (x + w, y - h, z + d ),
            (x - w, y - h, z - d ),
            (x - w, y + h, z - d ),
            (x + w, y + h, z - d ),
            (x + w, y - h, z - d ),
        )

    def getSurfaces(self):
        # (p0x,p0y,p0z),(p1x,p1y,p1z),(p2x,p2y,p2z),(p3x,p3y,p3z),(i,(nx,ny,nz),cZ,type))
        r = []
        for i in range(5):
            s = []
            for index in self.polygons[i]:
                s.append(self.pos[index])
            norm = getNormVec(s[0], s[1], s[2])
            cZ = (s[0][2]+s[1][2]+s[2][2]+s[3][2]) / 4
            if i == 0:
                cZ -= 1
            s.append((i, norm, cZ, self.type))
            r.append(s)
        return r
                    
    def setCamera(self, cameraX, cameraY, cameraZ, mRotX, mRotY):
        self.pos = []
        for v in self.vertices:
            a = v[0] - cameraX
            b = v[1] - cameraY
            c = v[2] - cameraZ

            # rotate around Y axis
            p = mRotY[0] * a + mRotY[1] * b + mRotY[2] * c
            q = mRotY[3] * a + mRotY[4] * b + mRotY[5] * c
            r = mRotY[6] * a + mRotY[7] * b + mRotY[8] * c

            # rotate around X axis
            a = mRotX[0] * p + mRotX[1] * q + mRotX[2] * r
            b = mRotX[3] * p + mRotX[4] * q + mRotX[5] * r
            c = mRotX[6] * p + mRotX[7] * q + mRotX[8] * r

            self.pos.append((a, b, c))                

def tick():
    global xpos, xposNext, zpos, zposNext, dir, dirNext, counter, cameraY, JUMPSPEED, maze
    (dx, dz) = (0, 0)
    keydown = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and counter == 0:
            keydown = True
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
            elif event.key == K_SPACE and JUMPSPEED == 0:
                JUMPSPEED = 150
                #cProfile.run('paint()')
                
    if keydown and maze[zpos + dz][xpos + dx] == 0:
        (xposNext, zposNext) = (xpos + dx*2, zpos + dz*2)

    if keydown and dirNext != dir or xposNext != xpos or zposNext != zpos:
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
    
    JUMPSPEED -= 4;
    cameraY += JUMPSPEED;
    if cameraY < 50:
        JUMPSPEED = 0
        cameraY = 50
    
    (c, s) = (cos(cameraRotY), sin(cameraRotY))
    mRotY = [c, 0, s, 0, 1, 0, -s, 0, c]
    mRotX = [1, 0, 0, 0, 1, 0, 0, 0, 1]
    if cameraY != 50:
        cameraRotX = min(90, (cameraY - 50) / 20) * pi / 180
        (c, s) = (cos(-cameraRotX), sin(-cameraRotX))
        mRotX = [1, 0, 0, 0, c, -s, 0, s, c]
    [c.setCamera(cameraX, cameraY, cameraZ, mRotX, mRotY) for c in cubes]

def paint():
    # Paint polygons
    SURFACE.fill((0,0,0))
    surfaces = []
    [[surfaces.append(s) for s in cube.getSurfaces()] for cube in cubes]

    # ((p0x,p0y,p0z),(p1x,p1y,p1z),(p2x,p2y,p2z),(p3x,p3y,p3z),（i,(nx,ny,nz),cZ,type)）
    surfaces = sorted(surfaces, key=lambda x: x[4][2], reverse=True)

    for s in surfaces:
        norm = s[4][1]
        d = norm[0]*light[0] + norm[1]*light[1] + norm[2]*light[2]
        ratio = (d + 1) / 2
        (r, g, b) = (0, 255, 128) if s[4][3] == "dot" else (255,255,255)
        (r, g, b) = (floor(r*ratio), floor(g*ratio), floor(b*ratio))

        pts = []
        for i in range(4):
            (x, y, z) = (s[i][0],s[i][1],s[i][2])
            if z <= 10:
                continue
            x = x * 1000 / z + 300
            y = -y * 1000 / z + 300
            pts.append((int(x), int(y)))

        if len(pts) > 3:
            pygame.draw.polygon(SURFACE, (r,g,b), pts)    
    
    pygame.display.update()

def main():
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
