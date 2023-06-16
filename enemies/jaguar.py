from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from .groundenemy import GroundEnemy
from pgu.tilevid import Sprite
import random
import math
from .groundenemy import getSpriteTileCoord
from .groundenemy import *
from base import FPS
from base import difficultyMul


class Jaguar(GroundEnemy):
    def __init__(self, g, pos, wd, maxSpeed, maxAccel):
        def onDaveReached(g, s, a):
            if g.daveInTrouble(8):
                print("Hey look! Mincayani is kissing the jaguar!")

        GroundEnemy.__init__(self, g, g.images['jaguar_1_1'], pos, wd, maxSpeed, maxAccel)

        # self.groups = g.string2groups('enemy,genemy')
        # self.agroups = g.string2groups('player')
        self.hit = onDaveReached

        self.anim_frame = 1
        self.customState = 0

    def animate(self, game):
        interval = 2
        maxFrames = 5  ## How many frames are in the animation

        #		if (((self.dx) >= self.wanderSpeed) or ((self.dx) <= -self.wanderSpeed)):
        #			interval = 3
        #		else:
        #			interval = 5

        direction = 1
        if (self.dx > 0):
            direction = 2

        # Walking is the default image
        image_string = "jag_walk_" + str(direction)

        # Unless we're chasing, in that case, run
        if (self.chaseState == STATE_CHASING):
            maxFrames = 6  # The chasing animation has 6 frames, while the walking anim has 5
            image_string = "jaguar_" + str(direction)

        if (self.dx != 0):
            if ((game.frame % interval) == 0):
                self.anim_frame += 1
                if (self.anim_frame > maxFrames):
                    self.anim_frame = 1
                if (self.anim_frame <= 0):
                    self.anim_frame = maxFrames
        else:
            image_string = "jag_walk_" + str(direction)
            self.anim_frame = 1

        image_string += "_" + str(self.anim_frame)

        ## Set image string
        self.setimage(game.images[image_string])
