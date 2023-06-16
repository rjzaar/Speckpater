from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import range
import pygame
import random
import math
from .enemy import BaseEnemy
from pgu.tilevid import Sprite
from base import difficultyMul


# --------------- #
# Bat Enemy Class #
# --------------- #
class Bat(BaseEnemy):
    def __init__(self, g, pos):
        def hit_handler(g, s, a):
            if g.daveInTrouble(7):
                # todo, sound?
                print("Ouch! Rabid bat!")

        Sprite.__init__(self, g.images['bat_0_1'], pos)
        self.groups = g.string2groups('enemy')
        self.agroups = g.string2groups('player')
        self.anim_frame = random.choice(list(range(1, 4)))
        self.hit = hit_handler

        self.ycycle = 1  # How fast the bat should cycle vertically
        self.ymag = 3  # How dynamic the bat's vertical motion should be
        self.xcycle = 1  # How fast the bat should cycle horizontally
        self.xmag = 0  # How dynamic the bat's horizontal motion should be

        # randomize the frame position
        self.randFramePos = random.randint(0, 777)

        self.origin = pos

    ## Bat loop
    def loop(self, game, sprite):
        self.__animate(game)
        self.__move(game)

    def __animate(self, game):
        interval = 2  ## How fast the animation proceeds. Higher numbers = slower
        maxFrames = 3  ## How many frames are in the animation

        image_string = "bat_0"

        if ((game.frame % interval) == 0):
            self.anim_frame += 1
            if (self.anim_frame > maxFrames):
                self.anim_frame = 1
        image_string += "_" + str(self.anim_frame)

        ## Set image string
        self.setimage(game.images[image_string])

    def __move(self, game):
        f = game.frame * difficultyMul() + self.randFramePos
        self.rect.y = self.origin.y + 32 * self.ymag * math.sin((f % 360) * self.ycycle / 19.1)
        self.rect.x = self.origin.x + 32 * self.xmag * math.cos((f % 360) * self.xcycle / 19.1)
