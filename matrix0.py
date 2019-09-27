""" matrix0.py sample """
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_0, K_9

pygame.init()
SURFACE = pygame.display.set_mode([400, 150])
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
        SURFACE.blit(self.bitmaps[self.number], self.number_rect)
        if self.is_focused:
            pygame.draw.rect(SURFACE, (0, 0, 225),
                             self.focus_rect, 2)

def main():
    """ main routine """
    font = pygame.font.SysFont(None, 60)
    mess_cross = font.render("x", True, (0, 0, 0))
    mess_equal = font.render("=", True, (0, 0, 0))
    focus_index = 0
    positions = (
        (50, 50, 1), (100, 50, 2), (50, 100, 3), (100, 100, 4),
        (170, 50, 1), (220, 50, 0), (170, 100, 0), (220, 100, 1),
        (300, 50, 1), (350, 50, 2), (300, 100, 3), (350, 100, 4))

    boxes = []
    for pos in positions:
        boxes.append(Box((pos[0], pos[1]), pos[2], False))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and K_0 <= event.key <= K_9:
                boxes[focus_index].number = event.key - K_0
                focus_index = (focus_index + 1) % 8

        for index in range(8):
            boxes[index].is_focused = True \
                if index == focus_index else False

        val0 = boxes[0].number * boxes[4].number \
            + boxes[1].number * boxes[6].number
        val1 = boxes[0].number * boxes[5].number \
            + boxes[1].number * boxes[7].number
        val2 = boxes[2].number * boxes[4].number \
            + boxes[3].number * boxes[6].number
        val3 = boxes[2].number * boxes[5].number \
            + boxes[3].number * boxes[7].number
        boxes[8].number = val0
        boxes[9].number = val1
        boxes[10].number = val2
        boxes[11].number = val3

        # Paint
        SURFACE.fill((255, 255, 255))
        for box in boxes:
            box.draw()
        SURFACE.blit(mess_cross, (125, 50))
        SURFACE.blit(mess_equal, (250, 50))

        pygame.display.update()
        FPSCLOCK.tick(10)

if __name__ == '__main__':
    main()
