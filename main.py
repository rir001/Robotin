import pygame
from pygame.locals import *
from parametros import *

from robotin import Robotin

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)


    robotin = Robotin()

    clock = pygame.time.Clock()

    run = 1
    while run:
        clock.tick(FRAMERATE)
        for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run = 0

                elif event.type == QUIT:
                    run = 0

        screen.fill(COLOR_CARA)

        robotin.update()
        robotin.draw(screen)

        pygame.display.flip()