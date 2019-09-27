""" trig_function0.py """
import sys
from math import sin, cos, radians
import pygame
from pygame.locals import Rect, QUIT, \
    MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP

pygame.init()
SURFACE = pygame.display.set_mode((400, 450))
FPSCLOCK = pygame.time.Clock()

class Slider:
    "スライダウィジェット"
    def __init__(self, rect, min_value, max_value, value):
        self.rect = rect
        self.slider_rect = rect.copy()
        self.slider_rect.inflate_ip(-20, -20)
        self.knob_rect = rect.copy()
        self.knob_rect.move_ip(10, 0)
        self.knob_rect.width = 4
        self.min_value = min_value
        self.max_value = max_value
        self.value = value

    def draw(self):
        """ スライダを描画 """
        pygame.draw.rect(SURFACE, (225, 225, 225), self.rect)
        pygame.draw.rect(SURFACE, (64, 64, 128), self.slider_rect)
        pygame.draw.rect(SURFACE, (0, 0, 255), self.knob_rect)

    def set_pos(self, xpos):
        """ スライダ値を設定 """
        xpos = max(self.slider_rect.left,
                   min(self.slider_rect.right, xpos))
        ypos = self.knob_rect.center[1]
        self.knob_rect.center = (xpos, ypos)

    def get_value(self):
        """ スライダ値を取得 """
        ratio = (self.knob_rect.center[0] - self.slider_rect.left)\
                / self.slider_rect.width
        return (self.max_value - self.min_value) * ratio\
                + self.min_value

def main():
    """ メインルーチン """
    sysfont = pygame.font.SysFont(None, 24)
    slider = Slider(Rect(20, 410, 360, 35), 0, 360, 0)
    mouse_down = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                if mouse_down and \
                   slider.rect.collidepoint(event.pos):
                    slider.set_pos(event.pos[0])
            elif event.type == MOUSEBUTTONDOWN:
                mouse_down = True
            elif event.type == MOUSEBUTTONUP:
                mouse_down = False

        SURFACE.fill((255, 255, 255))
        slider.draw()

        for index in range(0, 400, 10):
            pygame.draw.line(SURFACE, (225, 225, 225),
                             (0, index), (400, index))
            pygame.draw.line(SURFACE, (225, 225, 225),
                             (index, 0), (index, 400))
        pygame.draw.line(SURFACE, (0, 0, 0), (0, 200), (400, 200))
        pygame.draw.line(SURFACE, (0, 0, 0), (200, 0), (200, 400))
        pygame.draw.circle(SURFACE, (255, 0, 0), (200, 200), 150, 2)

        theta = slider.get_value()
        cos_v = round(cos(radians(theta)), 3)
        sin_v = round(sin(radians(theta)), 3)
        xpos = cos_v * 150 + 200
        ypos = sin_v * -150 + 200
        pygame.draw.line(SURFACE, (0, 0, 192),
                         (xpos, ypos), (xpos, 200))
        pygame.draw.line(SURFACE, (0, 192, 0),
                         (xpos, ypos), (200, ypos))
        pygame.draw.line(SURFACE, (192, 0, 0),
                         (xpos, ypos), (200, 200))

        bmp = sysfont.render("cos:{}".format(cos_v),
                             True, (0, 0, 192))
        SURFACE.blit(bmp, (xpos, 200))
        bmp = sysfont.render("sin:{}".format(sin_v),
                             True, (0, 192, 0))
        SURFACE.blit(bmp, (200, ypos))

        pygame.display.update()
        FPSCLOCK.tick(10)

if __name__ == '__main__':
    main()
