from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from past.utils import old_div
from .groundenemy import GroundEnemy
from pgu.tilevid import Sprite
import random
import math
from items import Banana
from .groundenemy import getSpriteTileCoord
from base import FPS
from base import difficultyMulStep
from pygame import transform

EATING_TIME = FPS * 7

STATE_HUNGRY = 0
STATE_FOUNDFOOD = 1
STATE_EATING = 2
STATE_FULL = 3


class HungyMonkey(GroundEnemy):
    def __init__(self, g, pos, wd, maxSpeed, maxAccel):
        def onDaveReached(g, s, a):
            if self.customState != STATE_HUNGRY:
                return

            if g.daveInTrouble(4):
                print("Hey stop! Bad monkey took my stuff!")
                self.beginEating()

        # Sprite.__init__(self, g.images['monkey_0_1'], pos)
        # GroundEnemy.__init__(self, g, pos, 12, 8, 2.2)
        GroundEnemy.__init__(self, g, g.images['monkey_sit_1'], pos, wd, maxSpeed, maxAccel)

        # self.groups = g.string2groups('enemy,genemy')
        # self.agroups = g.string2groups('player')
        self.hit = onDaveReached

        self.customState = STATE_HUNGRY
        self.eatingTimer = 0
        self.food = None
        self.fullnessTimer = 0

        self.fetchSpeed = 7.0
        # max speed might be low in some difficulty levels
        if self.fetchSpeed > self.maxSpeed:
            self.fetchSpeed = self.maxSpeed

        self.animFrame = 1

    def beginEating(self):
        self.customState = STATE_EATING
        self.eatingTimer = old_div(EATING_TIME, difficultyMulStep(0.2))

        self.dbgMsg("eating")

    def customBehaviour(self, game):

        if self.customState == STATE_HUNGRY:

            for spr in game.sprites:
                if isinstance(spr, Banana):
                    if self.isStraightPathFreeTo(game, getSpriteTileCoord(spr)):
                        self.dbgMsg("found food!")
                        self.customState = STATE_FOUNDFOOD
                        self.food = spr
                        break
                    else:
                        self.food = None

        if self.customState == STATE_FOUNDFOOD:

            dist = self.food.rect.x - (self.rect.x + self.dx)
            dir = -1
            if dist > 0:
                dir = 1

            if not self.food in game.sprites:
                self.food = None
                self.customState = STATE_HUNGRY

            elif abs(dist) > (self.rect.width):

                if self.canMoveToDir(game, dir):
                    self.move(dir * min(abs(dist), self.xWanderAccel), self.fetchSpeed)
                else:
                    # todo, maybe in this case the banana should be put to ignore list
                    self.food = None
                    self.customState = STATE_HUNGRY

            else:
                if (self.food.rect.y + self.food.rect.height) == (self.rect.y + self.rect.height):
                    game.sprites.remove(self.food)
                    self.food = None
                    self.beginEating()

        elif self.customState == STATE_EATING:
            # todo eat animation
            if self.eatingTimer > 0:
                self.eatingTimer -= 1
            else:
                # now it's full for a while
                self.customState = STATE_FULL
                self.fullnessTimer = old_div(FPS * 10, difficultyMulStep(0.1))
                self.dbgMsg("done eating")

        elif self.customState == STATE_FULL:
            if self.fullnessTimer > 0:
                self.fullnessTimer -= 1
                if self.fullnessTimer == 0:
                    self.customState = STATE_HUNGRY
                    self.dbgMsg("hungry again")
                else:
                    # rest about half of the time before wandering
                    if self.fullnessTimer > (FPS * 5):
                        self.stop()
                    else:
                        self.wander(game)

        return self.customState != STATE_HUNGRY

    def animate(self, game):

        interval = 5

        if ((game.frame % interval) == 0):
            self.animFrame += 1
            if self.animFrame > 3:
                self.animFrame = 1

        if self.customState == STATE_EATING:

            image_string = "monkey_banana_" + str(self.animFrame)
            # print image_string

            self.setimage(game.images[image_string])

        # elif self.customState == STATE_FULL:
        #	self.setimage(game.images['monkey_sit'])
        else:

            if abs(self.dx) > 0:

                image_string = "monkey_walk_" + str(self.animFrame)
                img = game.images[image_string][0]
                if self.dx < 0:
                    img = transform.flip(img, True, False)

                self.setimage(img)
            else:
                # use the animFrame to randomly select image
                img = game.images['monkey_sit_' + str(int((game.frame % 500) < 250) + 1)][0]
                # movingDir is not accurate but it works well in here
                if self.movingDir == 1:
                    img = transform.flip(img, True, False)
                self.setimage(img)

# def animate(self, game):
# if self.customState == STATE_EATING:
# self.setimage(game.images['monkey_1_1'])
# else:
# self.setimage(game.images['monkey_0_1'])
