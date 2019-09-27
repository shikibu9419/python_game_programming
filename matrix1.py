""" matrix1.py sample """
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_0, K_9, K_MINUS

pygame.init()
SURFACE = pygame.display.set_mode((500, 600))
FPSCLOCK = pygame.time.Clock()

class Box:
    "number input field"
    myfont = pygame.font.SysFont(None, 40)
    bitmaps = []
    for num in range(100):
        bitmaps.append(myfont.render(str(num), True, (64, 64, 64)))

    def __init__(self, pos, value, is_focused):
        self.is_focused = is_focused
        self.number = value
        self.number_rect = self.bitmaps[value].get_rect(center=pos)
        self.focus_rect = self.number_rect.copy()
        self.focus_rect.inflate_ip(10, 0)

    def draw(self):
        """ draw number and focus """
        if self.number > 99:
            return
        if self.number < 0:
            posx, posy = self.number_rect.center
            pygame.draw.line(SURFACE, (64, 64, 64),
                             (posx-20, posy), (posx-10, posy), 2)
        SURFACE.blit(self.bitmaps[abs(self.number)],
                     self.number_rect)
        if self.is_focused:
            pygame.draw.rect(SURFACE, (0, 0, 225),
                             self.focus_rect, 2)

def main():
    """ main routine """
    focus_index = 0
    positions = ((220, 520, 1), (280, 520, 0),
                 (220, 560, 0), (280, 560, 1))

    boxes = []
    for pos in positions:
        boxes.append(Box((pos[0], pos[1]), pos[2], False))

    src = ((1, 1), (2, 1), (1, 3))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if K_0 <= event.key <= K_9:
                    boxes[focus_index].number = event.key - K_0
                elif event.key == K_MINUS:
                    boxes[focus_index].number *= -1
                focus_index = (focus_index + 1) % 4


        for index in range(4):
            boxes[index].is_focused = True \
                if index == focus_index else False

        # Paint
        SURFACE.fill((255, 255, 255))

        pygame.draw.line(SURFACE, (255, 0, 0),
                         (0, 250), (500, 250), 3)
        pygame.draw.line(SURFACE, (255, 0, 0),
                         (250, 0), (250, 500), 3)

        dst = [(boxes[0].number * p[0] + boxes[1].number * p[1],
                boxes[2].number * p[0] + \
                    boxes[3].number * p[1]) for p in src]
        src_pts = [(p[0]*25+250, -p[1]*25+250) for p in src]
        dst_pts = [(p[0]*25+250, -p[1]*25+250) for p in dst]
        pygame.draw.polygon(SURFACE, (0, 255, 0), src_pts)
        pygame.draw.polygon(SURFACE, (0, 0, 255), dst_pts)

        for index in range(0, 501, +25):
            pygame.draw.line(SURFACE, (64, 64, 64),
                             (0, index), (500, index))
            pygame.draw.line(SURFACE, (64, 64, 64),
                             (index, 0), (index, 500))

        for box in boxes:
            box.draw()

        pygame.display.update()
        FPSCLOCK.tick(10)

if __name__ == '__main__':
    main()
