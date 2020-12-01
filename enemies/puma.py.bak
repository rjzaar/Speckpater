from groundenemy import GroundEnemy
from pgu.tilevid import Sprite
import random
import math
from groundenemy import getSpriteTileCoord
from base import FPS
from base import difficultyMul

class Puma(GroundEnemy):
	def __init__(self, g, pos, wd, maxSpeed, maxAccel):
		def onDaveReached(g, s, a):
			pass

		GroundEnemy.__init__(self, g, g.images['puma_1_1'], pos, wd, maxSpeed, maxAccel)

		#self.groups = g.string2groups('enemy,genemy')
		#self.agroups = g.string2groups('player')
		self.hit = onDaveReached
		
		self.anim_frame = 1
		self.customState = 0

	def animate(self, game):
		interval = 2

		if (((self.dx) >= self.wanderSpeed) or ((self.dx) <= -self.wanderSpeed)):
			interval = 2
		else:
			interval = 3
			
		maxFrames = 6					## How many frames are in the animation

		direction = 1
		if (self.dx > 0):
			direction = 2

		image_string = "puma_" + str(direction)

		if (self.dx != 0):
			if ((game.frame % interval) == 0):
				self.anim_frame += 1
				if (self.anim_frame > maxFrames):
					self.anim_frame = 1
				if (self.anim_frame <= 0):
					self.anim_frame = maxFrames
		else:
			self.anim_frame = 1

		image_string += "_" + str(self.anim_frame)

		## Set image string
		self.setimage(game.images[image_string])
		