""" rotate_image testing """
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((500, 400))
FPSCLOCK = pygame.time.Clock()
BALL_IMAGE = pygame.image.load("pin0.png")
THETA = 0.05

def rot_center(image, xpos, ypos, theta, zoom):
    """ rotate image """
    rotate_sprite = pygame.transform.rotozoom(image, theta, zoom)
    rect = rotate_sprite.get_rect()
    SURFACE.blit(rotate_sprite, (xpos-(rect.width/2), ypos-(rect.height/2)))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    SURFACE.fill((0, 0, 0))
    THETA += 0.4

    rot_center(BALL_IMAGE, 200, 200, THETA, 0.6)

    pygame.display.update()
    FPSCLOCK.tick(30)
