""" vector_dot.py sample """
import sys
from math import floor, hypot, acos, degrees
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

pygame.init()
SURFACE = pygame.display.set_mode((500, 700))
FPSCLOCK = pygame.time.Clock()

def dot(vec1, vec2):
    """ ベクトルの内積を返す """
    return vec1[0]*vec2[0] + vec1[1]*vec2[1]

def main():
    """ main routine """
    count = 0
    pos0 = (0, 0)
    pos1 = (0, 0)
    sysfont = pygame.font.SysFont(None, 24)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                xpos = floor((event.pos[0] - 240) / 25)
                ypos = -floor((event.pos[1] - 240) / 25)
                if count % 2 == 0:
                    pos0 = (xpos, ypos)
                    pos1 = (0, 0)
                else:
                    pos1 = (xpos, ypos)
                count += 1

        # Paint
        SURFACE.fill((0, 0, 0))
        for ypos in range(0, 500, 25):
            for xpos in range(0, 500, 25):
                pygame.draw.ellipse(SURFACE, (64, 64, 64),
                                    (xpos, ypos, 2, 2))
        pygame.draw.line(SURFACE, (255, 0, 0),
                         (250, 0), (250, 500), 3)
        pygame.draw.line(SURFACE, (255, 0, 0),
                         (0, 250), (500, 250), 3)

        coord0 = pos0[0] * 25 + 250, pos0[1] * -25 + 250
        pygame.draw.line(SURFACE, (0, 255, 0),
                         (250, 250), coord0, 2)

        coord1 = pos1[0] * 25 + 250, pos1[1] * -25 + 250
        pygame.draw.line(SURFACE, (0, 255, 255),
                         (250, 250), coord1, 2)


        # 情報領域描画
        pygame.draw.rect(SURFACE, (255, 255, 255),
                         (0, 500, 500, 200))
        len0 = hypot(pos0[0], pos0[1])
        len1 = hypot(pos1[0], pos1[1])
        len2 = len0 * len1
        if len2 == 0:
            len2 = 0.000001
        strings = [
            "V1=({}, {})".format(pos0[0], pos0[1]),
            "V2=({}, {})".format(pos1[0], pos1[1]),
            "dot of V1 & V2 ={}".format(dot(pos0, pos1)),
            "|V1|={}".format(len0),
            "|V2|={}".format(len1),
            "cos(theta)={}".format(dot(pos0, pos1) / len2),
            "theta={}".format(degrees(acos(dot(pos0, pos1) / len2)))
        ]
        for index, bitmap_str in enumerate(strings):
            bmp = sysfont.render(bitmap_str, True, (0, 0, 0))
            SURFACE.blit(bmp, (20, index*25+510))
        pygame.display.update()
        FPSCLOCK.tick(10)

if __name__ == '__main__':
    main()
