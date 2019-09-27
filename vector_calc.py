""" vector_calc.py sample """
import sys
from math import floor
import pygame
from pygame.locals import MOUSEBUTTONDOWN,\
    MOUSEBUTTONUP, MOUSEMOTION, QUIT

pygame.init()
SURFACE = pygame.display.set_mode((500, 800))
FPSCLOCK = pygame.time.Clock()

def cross(vec1, vec2):
    """ ベクトルの外積を返す """
    return vec1[0]*vec2[1] - vec1[1]*vec2[0]

def dot(vec1, vec2):
    """ ベクトルの内積を返す """
    return vec1[0]*vec2[0] + vec1[1]*vec2[1]

def coord(pos):
    """ マス目の座標を画面上のx,y座標値へ変換 """
    return (pos[0] * 50 + 250, -pos[1] * 50 + 250)

def vec(pos0, pos1):
    """ 2点間を結ぶベクトルを返す """
    return (pos1[0] - pos0[0], pos1[1] - pos0[1])

def main():
    """ main routine """
    click_count = 0
    click_pos = None
    focus_pos = None
    seg1 = ((0, 0), (0, 0))
    seg2 = ((0, 0), (0, 0))
    sysfont = pygame.font.SysFont(None, 24)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                xpos = floor((event.pos[0] - 225) / 50)
                ypos = floor((event.pos[1] - 225) / 50)
                click_pos = (xpos, -ypos)
                focus_pos = (xpos, -ypos)
            elif event.type == MOUSEMOTION:
                xpos = floor((event.pos[0] - 225) / 50)
                ypos = floor((event.pos[1] - 225) / 50)
                if click_pos:
                    focus_pos = (xpos, -ypos)
            elif event.type == MOUSEBUTTONUP:
                if click_count % 2 == 0:
                    seg1 = (click_pos, focus_pos)
                else:
                    seg2 = (click_pos, focus_pos)
                click_count += 1
                click_pos = None

        # グラフ領域描画
        SURFACE.fill((0, 0, 0))
        for ypos in range(0, 500, 50):
            for xpos in range(0, 500, 50):
                pygame.draw.ellipse(SURFACE, (64, 64, 64),
                                    (xpos-2, ypos-2, 4, 4))

        pygame.draw.line(SURFACE, (0, 0, 255),
                         (250, 0), (250, 500), 3)
        pygame.draw.line(SURFACE, (0, 0, 255),
                         (0, 250), (500, 250), 3)

        pygame.draw.line(SURFACE, (0, 255, 0),
                         coord(seg1[0]), coord(seg1[1]))
        pygame.draw.line(SURFACE, (255, 0, 255),
                         coord(seg2[0]), coord(seg2[1]))

        if click_pos and focus_pos:
            pygame.draw.line(SURFACE, (255, 255, 255), \
                coord(click_pos), coord(focus_pos))

        # 情報領域描画
        pygame.draw.rect(SURFACE, (255, 255, 255),
                         (0, 500, 500, 800))

        vec1 = vec(seg1[0], seg1[1])
        vec2 = vec(seg2[0], seg2[1])
        vec0 = vec(seg1[0], seg2[0])
        cv1v2 = cross(vec1, vec2)
        crossed = False
        ratio1 = 0
        ratio2 = 0
        if cv1v2 != 0:
            ratio1 = cross(vec0, vec1) / cv1v2
            ratio2 = cross(vec0, vec2) / cv1v2
            crossed = (0 <= ratio1 <= 1) and (0 <= ratio2 <= 1)

        strings = [
            "V1: {},{}  vector:{}".format(seg1[0], seg1[1], vec1),
            "V2: {},{}  vector:{}".format(seg2[0], seg2[1], vec2),
            "V0: vector:{}".format(vec0),
            "",
            "cross of V1 and V2:{}".format(cross(vec1, vec2)),
            "cross of V0 and V1:{}".format(cross(vec0, vec1)),
            "cross of V0 and V2:{}".format(cross(vec0, vec2)),
            "T  ={}".format(cv1v2),
            "T1 ={}".format(ratio1),
            "T2 ={}".format(ratio2),
            "Is V1 and V2 crossed:{}".format(crossed)
        ]

        colors = [(0, 128, 0), (255, 0, 255), (255, 0, 0)]
        for index, bitmap_str in enumerate(strings):
            color = colors[index] if index < 3 else (0, 0, 0)
            bmp = sysfont.render(bitmap_str, True, color)
            SURFACE.blit(bmp, (20, index*25+510))
        pygame.display.update()
        FPSCLOCK.tick(10)

if __name__ == '__main__':
    main()
