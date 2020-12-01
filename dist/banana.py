# Sprite.__init__(self, transform.rotate(g.images['monkey_0_1'][0], 90) , pos)

import pygame
from pgu.tilevid import Sprite
from pygame import transform
import math

NUMROTATIONS = 8


class Banana(Sprite):
    def __init__(self, g, pos):
        Sprite.__init__(self, g.images['banana'], pos)
        self.rotation = 0.0
        self.dy = self.dx = 0

        self.go_down = 0

    # sourceimg = g.images['banana'][0]
    #
    # if not g.images.has_key('banana_0'):
    # for i in range(0,NUMROTATIONS):
    #
    # k = 'banana_' + str(i)
    # print k
    # g.images[k] = transform.rotate(sourceimg,i * (360 / NUMROTATIONS))

    def throw(self, angle, power):
        self.dx = math.sin(angle) * power
        self.dy = -math.cos(angle) * power

    def loop(self, game, sprite):
        self.dy += 0.2

        self.rect.y += self.dy
        self.rect.x += self.dx

        img = transform.rotate(game.images['banana'][0], self.rotation)
        self.rotation += 4
        self.setimage(img)
