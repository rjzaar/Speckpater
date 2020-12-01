# Sprite.__init__(self, transform.rotate(g.images['monkey_0_1'][0], 90) , pos)

import pygame
from pgu.tilevid import Sprite
from pygame import transform
import math

NUMROTATIONS = 8


class Item(Sprite):
    def __init__(self, g, ishape, pos):
        Sprite.__init__(self, ishape, pos)
        self.groups = g.string2groups('item,colspr')
        self.dy = self.dx = 0.0

    def applyFriction(self):
        self.dx /= 1.2
        if (abs(self.dx) < 0.5): self.dx = 0.0

    def onClimbableTile(self, t):
        pass

    def onTopLineContact(self, t):
        self.applyFriction()
        self.rect.bottom = t.rect.top
        self.dy = 0

    def onBottomLineContact(self, t):
        self.dy /= 2.0
        self.dy = -self.dy

    def onLeftLineContact(self, t):
        self.rect.right = t.rect.left
        self.dx /= 2.5
        self.dx = -self.dx

    def onRightLineContact(self, t):
        self.rect.left = t.rect.right
        self.dx /= 2.5
        self.dx = -self.dx


class Banana(Item):
    def __init__(self, g, pos):
        Item.__init__(self, g, g.images['banana'], pos)

        self.rotation = 0.0

    def throw(self, angle, power):
        self.dx = math.sin(angle) * power
        self.dy = -math.cos(angle) * power

    def loop(self, game, sprite):

        self.dy += 0.3

        self.rect.y += self.dy
        self.rect.x += self.dx

        rectCenter = self.rect.center
        img = transform.rotate(game.images['banana'][0], self.rotation)
        if self.dx > 0:
            self.rotation -= min(4.0, self.dx)
        elif self.dx < 0:
            self.rotation += min(4.0, -self.dx)
        self.setimage(img)
        self.rect.center = rectCenter
