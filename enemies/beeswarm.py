from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import range
import pygame
import random
import math
from copy import copy

from .enemy import BaseEnemy
from .groundenemy import distance
from .groundenemy import clamp
from .groundenemy import getSpriteTileCoord
from pgu.tilevid import Sprite
import base
from base import *

STATE_WANDER = 0
STATE_CHASE = 1


# --------------------- #
# Bee Swarm Enemy Class #
# --------------------- #
class BeeSwarm(BaseEnemy):
    def __init__(self, g, pos):
        def hit_handler(g, s, a):
            print("Ouch! Killer bees!")
            g.daveInTrouble(3)

        Sprite.__init__(self, g.images['beeswarm_0_1'], pos)
        self.groups = g.string2groups('enemy')
        self.agroups = g.string2groups('player')
        self.anim_frame = random.choice(list(range(1, 4)))
        self.hit = hit_handler

        self.sensitivity = 8 * 32  # How sensitive the bees are to giving chase to Dave (in pixels)

        self.speed = 2  # How fast the bees are (in pixels)

        self.ycycle = 2  # How fast the swarm should cycle vertically
        self.ymag = .75  # How dynamic the swarm's vertical motion should be
        self.xcycle = 3  # How fast the swarm should cycle horizontally
        self.xmag = .5  # How dynamic the swarm's horizontal motion should be

        self.home = pos

        self.loc = copy(self.home)

        self.state = STATE_WANDER

    ## Swarm loop
    def loop(self, game, sprite):
        self.find_target(game)
        self.__animate(game)
        self.__move(game)

    def find_target(self, game):
        # If Dave is in range, set the target to be Dave and move towards him.
        d = self.distanceToDave(game)

        # print "Distance to Dave is " + str(d)

        if (d <= self.sensitivity * difficultyMul()):
            self.target = copy(game.player.rect)
            self.target.y += 16  # Kludge to make them fly at Dave a little bit lower to help him jump over the bees easier
            if (self.state != STATE_CHASE):
                if base.SOUND:
                    base.sound.Play("angrybuzz")
            self.state = STATE_CHASE

        # Otherwise, if we haven't seen Dave in a while, set the target to be home.
        else:
            # TODO: Make a timeout so that they wander around for a little while after losing Dave.
            self.target = self.home
            if (self.state != STATE_WANDER):
                if base.SOUND:
                    base.sound.Play("buzz1")
            self.state = STATE_WANDER

    def distanceToDave(self, game):
        return distance(game.player.rect, self.loc)

    def __animate(self, game):
        interval = 2  ## How fast the animation proceeds. Higher numbers = slower
        maxFrames = 4  ## How many frames are in the animation

        image_string = "beeswarm_0"

        if ((game.frame % interval) == 0):
            self.anim_frame += 1
            if (self.anim_frame > maxFrames):
                self.anim_frame = 1
        image_string += "_" + str(self.anim_frame)

        ## Set image string
        self.setimage(game.images[image_string])

    def __move(self, game):
        self.loc.x += self.getXDirection() * self.speed * difficultyMul()
        self.loc.y += self.getYDirection() * self.speed * difficultyMul()

        angle = game.frame % 360
        self.rect.y = self.loc.y + 32 * self.ymag * difficultyMul() * math.sin((angle) * self.ycycle / 19.1)
        self.rect.x = self.loc.x + 32 * self.xmag * difficultyMul() * math.cos((angle) * self.xcycle / 19.1)

    def getXDirection(self):
        if (self.loc.x < self.target.x):
            return 1
        else:
            if (self.loc.x > self.target.x):
                return -1
            else:
                return 0

    def getYDirection(self):
        if (self.loc.y < self.target.y):
            return 1
        else:
            if (self.loc.y > self.target.y):
                return -1
            else:
                return 0
