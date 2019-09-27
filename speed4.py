""" speed4.py """
import sys
from math import sin, radians
import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE, Rect

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((600, 600))
FPSCLOCK = pygame.time.Clock()

def main():
    """ メインルーチン """
    rect = Rect(0, 300, 10, 10)
    speed = 10
    velocity = -20
    accel = 5
    offset = 0
    game_over = False
    font = pygame.font.SysFont(None, 30)

    while True:
        is_flying = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    is_flying = True

        if not game_over:
            velocity += -accel if is_flying else accel
            rect.y += velocity
            offset += speed
            if offset % 100 == 0:
                speed += 2

        SURFACE.fill((0, 255, 0))

        # draw ceiling
        points = [(0, 0)]
        for pos_x in range(0, 610, 10):
            pos_y = 200 + sin(radians(pos_x + offset) / 2) * 80
            points.append((pos_x, pos_y))
            if pos_x == 10 and rect.y < pos_y:
                game_over = True
        points.append([600, 0])
        pygame.draw.polygon(SURFACE, (165, 42, 42), points)

        # draw floor
        points = [(0, 600)]
        for pos_x in range(0, 610, 10):
            pos_y = 400 + sin(radians(pos_x + offset) / 3) * 60
            points.append((pos_x, pos_y))
            if pos_x == 10 and rect.bottom > pos_y:
                game_over = True
        points.append([600, 600])
        pygame.draw.polygon(SURFACE, (165, 42, 42), points)

        pygame.draw.rect(SURFACE, (255, 255, 255), rect)

        score = font.render(str(offset), True, (255, 255, 255))
        SURFACE.blit(score, (500, 50))

        pygame.display.update()
        FPSCLOCK.tick(10)

if __name__ == '__main__':
    main()
