""" 2d_paintdrops_mini.py - Copyright 2016 Kenichiro Tanaka """
import sys
from math import floor
from random import randint
import pygame
from pygame.locals import QUIT, Rect, \
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from tiny_2d import Engine, CircleEntity, \
    LineEntity, SHAPE_CIRCLE, SHAPE_LINE

pygame.init()
SURFACE = pygame.display.set_mode((800, 500))
FPSCLOCK = pygame.time.Clock()

def main():
    """ メインルーチン """
    colors = [(255, 0, 0), (255, 64, 0), (255, 201, 38),
              (35, 140, 0), (0, 128, 255), (163, 0, 217),
              (255, 77, 255), (255, 255, 255)]
    color = colors[0]
    background_image \
        = pygame.image.load("images/background/wall0.png")
    ball_image = pygame.image.load("ball.png")
    ball_image = pygame.transform.scale(ball_image, (30, 30))
    palette_image = pygame.image.load("images/bg_palette.png")
    palette_image = pygame.transform.scale(palette_image,
                                           (800, 54))
    palette_rect = Rect(0, 0, 800, 54)

    button_images = []
    for index in range(8):
        path = "images/button/color" + str(index) + ".png"
        button_images.append(pygame.image.load(path))

    current_line = None
    mouse_pos = (0, 0)
    mousedown = False
    count = 0

    engine = Engine(0, 0, 800, 500, 0, 9.8)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if palette_rect.collidepoint(event.pos):
                    pindex = floor(event.pos[0] / 72)
                    if 0 <= pindex < 8:
                        color = colors[pindex]
                else:
                    mousedown = True
                    mouse_pos = event.pos
            elif event.type == MOUSEMOTION:
                if mousedown:
                    current_line = (mouse_pos, event.pos, color)
                else:
                    current_line = None
            elif event.type == MOUSEBUTTONUP:
                if mousedown and not \
                   (mouse_pos[0] == event.pos[0] and \
                    mouse_pos[1] == event.pos[1]):
                    line_entity = LineEntity(mouse_pos[0],
                                             mouse_pos[1],
                                             event.pos[0],
                                             event.pos[1])
                    line_entity.color = color
                    engine.entities.append(line_entity)
                mousedown = False
                current_line = None

        # 100カウント毎にボールを落とす
        if count % 100 == 0:
            circle = CircleEntity(randint(0, 600)+100, 0, 10)
            circle.color = color
            engine.entities.append(circle)
        count += 1
        engine.step(0.01)

        # パレットと未確定の線の描画
        for ypos in range(0, 500, 150):
            for xpos in range(0, 800, 150):
                SURFACE.blit(background_image, (xpos, ypos))
        SURFACE.blit(palette_image, (0, 0))
        for index in range(8):
            SURFACE.blit(button_images[index], (index*72, 0))

        if current_line:
            pygame.draw.line(SURFACE, current_line[2], 
                             current_line[0], current_line[1], 3)

        # ボールと線の描画
        for entity in engine.entities:
            if entity.shape == SHAPE_CIRCLE:
                pos = (int(entity.xpos), int(entity.ypos))
                rect = ball_image.get_rect()
                rect.center = pos
                SURFACE.blit(ball_image, rect.topleft)
            elif entity.shape == SHAPE_LINE:
                pos0 = (int(entity.pos0[0]), int(entity.pos0[1]))
                pos1 = (int(entity.pos1[0]), int(entity.pos1[1]))
                pygame.draw.line(SURFACE, entity.color,
                                 pos0, pos1, 3)

        pygame.display.update()
        FPSCLOCK.tick(20)

if __name__ == '__main__':
    main()
