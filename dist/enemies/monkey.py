from __future__ import absolute_import
from builtins import str
import pygame
import random
from .enemy import BaseEnemy
from .guava import Guava
from pgu.tilevid import Sprite

from base import difficultyMul


# ------------------ #
# Monkey Enemy Class #
# ------------------ #
class Monkey(BaseEnemy):
    def __init__(self, g, pos):
        def hit_handler(g, s, a):
            pass

        Sprite.__init__(self, g.images['monkey_0_1'], pos)
        self.groups = g.string2groups('enemy')
        self.agroups = g.string2groups('player')
        self.anim_frame = random.randrange(1, 5)
        self.hit = hit_handler

        ## How often the monkey should attack. Higher numbers = more infrequent
        self.nextAttackFrame = random.randrange(0, 10)
        random.jumpahead(1)

    ## Monkey loop
    def loop(self, game, sprite):
        self.__animate(game)
        self.__attack(game)

    def __animate(self, game):
        interval = 4  ## How fast the monkey is animated. Higher numbers = slower
        maxFrames = 4  ## How many frames are in the monkey's animation

        image_string = "monkey_0"

        if ((game.frame % interval) == 0):
            self.anim_frame += 1
            if (self.anim_frame > maxFrames):
                self.anim_frame = 1
        image_string += "_" + str(self.anim_frame)

        ## Set image string
        self.setimage(game.images[image_string])

    def __attack(self, game):
        if (game.frame > self.nextAttackFrame):
            ## Spawn a new fruit at the monkey's location and let 'er fall!
            guava = Guava(game, self.rect)
            game.sprites.append(guava)

            ## Set the new time that the monkey should attack
            self.nextAttackFrame = game.frame + (1.0 / difficultyMul()) * random.randrange(15, 40)
            random.jumpahead(1)
