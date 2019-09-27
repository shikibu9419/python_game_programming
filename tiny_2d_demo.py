""" tiny_2d_demo.py - Copyright 2016 Kenichiro Tanaka """
import sys
from random import randint
import pygame
from pygame.locals import QUIT, Rect
from tiny_2d import Engine, RectangleEntity, CircleEntity,\
    LineEntity, SHAPE_CIRCLE, SHAPE_RECTANGLE, SHAPE_LINE

pygame.init()
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()

def main():
    """ main routine """
    colors = [(255, 0, 0), (255, 165, 0), (242, 242, 0),
              (0, 128, 0), (128, 0, 128), (0, 0, 250)]
    engine = Engine(0, 0, 600, 800, 0, 9.8)

    rect = RectangleEntity(500, 50, 50, 400)
    rect.color = (0, 255, 0)
    engine.entities.append(rect)

    rect = RectangleEntity(0, 50, 50, 400)
    rect.color = (255, 255, 0)
    engine.entities.append(rect)

    line = LineEntity(50, 300, 400, 350)
    line.color = (255, 128, 0)
    engine.entities.append(line)

    line = LineEntity(500, 400, 100, 450)
    line.color = (255, 128, 0)
    engine.entities.append(line)

    for xpos in range(7):
        for ypos in range(3):
            circle = CircleEntity(xpos * 60 + 100,
                                  ypos * 60 + 100, 5, True)
            circle.color = colors[ypos]
            engine.entities.append(circle)

    for _ in range(20):
        circle = CircleEntity(randint(0, 400) + 50,
                              randint(0, 200), 10, False)
        circle.color = colors[randint(0, 5)]
        circle.velocity.xpos = randint(0, 10) - 5
        circle.velocity.ypos = randint(0, 10) - 5
        engine.entities.append(circle)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        engine.step(0.01)

        SURFACE.fill((0, 0, 0))
        for entity in engine.entities:
            if entity.shape == SHAPE_RECTANGLE:
                rect = Rect(entity.xpos, entity.ypos,
                            entity.width, entity.height)
                pygame.draw.rect(SURFACE, entity.color, rect)
            elif entity.shape == SHAPE_CIRCLE:
                pos = (int(entity.xpos), int(entity.ypos))
                pygame.draw.circle(SURFACE, entity.color,
                                   pos, entity.radius)
            elif entity.shape == SHAPE_LINE:
                pos0 = (int(entity.pos0[0]),
                        int(entity.pos0[1]))
                pos1 = (int(entity.pos1[0]),
                        int(entity.pos1[1]))
                pygame.draw.line(SURFACE, entity.color, pos0, pos1)

        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()
