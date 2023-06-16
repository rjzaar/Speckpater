from __future__ import print_function
from __future__ import absolute_import
import base
import pygame
import random
from .enemy import BaseEnemy
from pgu.tilevid import Sprite
from pygame import transform


# ------------------------- #
# Falling Block Enemy Class #
# ------------------------- #
class FallingBlock(BaseEnemy):
    def __init__(self, g, pos, firstColTileY):
        def on_collision(g, s, a):
            if s.dy > 2.0:  # consider this harmful only when falling down fast enough
                if g.daveInTrouble(15):
                    if base.SOUND:
                        base.sound.Play("Thud")
                    print("Ouch! Bricks aren't soft!")

        Sprite.__init__(self, g.images['block'][0], pos)
        self.groups = g.string2groups('genemy')
        self.groups += g.string2groups('enemy')
        self.agroups = g.string2groups('player')

        self.game = g

        self.dy = 0.0
        self.dx = 0.0

        self.x = self.rect.x
        self.y = self.rect.y

        self.hit = on_collision

        self.state = None
        self.on_ground = 0

        self.firstColY = firstColTileY * base.TILE_SIZE

    def onClimbableTile(self, t):
        pass

    def onBottomLineContact(self, t):
        pass

    def onTopLineContact(self, t):
        # dont collide with the tiles above this limit
        if t.rect.top < self.firstColY:
            return

        print("Bottom line contact")
        self.groups = self.game.string2groups('enemy')  # -= self.game.string2groups('genemy')
        self.dy = -4  # 0 - self.dy # Kick the block up as it bounces on the ground
        if base.SOUND:
            base.sound.Play("Thud")

    def onLeftLineContact(self, t):
        pass

    def onRightLineContact(self, t):
        pass

    def loop(self, g, sprite):
        self.__move(g)

    def __move(self, g):
        maxYVel = 8
        gravity = 0.4

        self.dy += gravity
        if (self.dy > maxYVel):
            self.dy = maxYVel

        self.y += self.dy
        self.x += self.dx

        if (self.y >= ((len(g.tlayer) - 1) * 32)):
            g.sprites.remove(self)
        else:
            self.rect.y = self.y
            self.rect.x = self.x
