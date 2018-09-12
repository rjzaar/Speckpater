import pygame
import random
import math
from enemy import BaseEnemy
from pgu.tilevid import Sprite
from base import difficultyMul
from pygame import transform

MAX_FRAMES = 5

# --------------- #
# Eagle Enemy Class #
# --------------- #
class Eagle(BaseEnemy):
	def __init__(self, g, pos):
		def hit_handler(g, s, a):
			
			if g.daveInTrouble(9):
				#todo, sound?
				print "Ouch!"

		Sprite.__init__(self, g.images['eagle_0_1'], pos)
		self.groups = g.string2groups('enemy')
		self.agroups = g.string2groups('player')
		self.animFrame = 1 # random.choice(range(1, MAX_FRAMES))
		self.animDir = 1
		self.hit = hit_handler
		
		self.ycycle = 1 # How fast the eagle should cycle vertically
		self.ymag   = 3 # How dynamic the eagle's vertical motion should be
		self.xcycle = 1 # How fast the eagle should cycle horizontally
		self.xmag   = 0 # How dynamic the eagle's horizontal motion should be

		self.origin = pos
		self.prevXoffset = 0
		self.moveDir = 0

	## Eagle loop
	def loop(self, game, sprite):
		self.__animate(game)
		self.__move(game)

	def __animate(self, game):
		interval = 3 					## How fast the animation proceeds. Higher numbers = slower

		image_string = "eagle_0"

		if ((game.frame % interval) == 0):
			
			self.animFrame += self.animDir
			if (self.animDir == 1 and self.animFrame == MAX_FRAMES) or (self.animDir == -1 and self.animFrame == 1):
				self.animDir *= -1
			
		image_string += "_" + str(self.animFrame)

		# set the image, first get the surface from the tuple
		img = game.images[image_string][0]
		 # flip the sprite according to horizontal velocity, but only when needed to
		if self.moveDir == 1:
			img = transform.flip(img, True, False)
		self.setimage(img)

	def __move(self, game):
		f = game.frame * difficultyMul()
		self.rect.y = self.origin.y + 32 * self.ymag * math.sin((f % 360) * self.ycycle / 19.1)
		# save dx for later use
		xoff = 32 * self.xmag * math.cos((f % 360) * self.xcycle / 19.1)
		
		dx = self.prevXoffset - xoff # count the move delta
		if dx < 0:
			self.moveDir = 0
		else:
			self.moveDir = 1
		
		self.rect.x = self.origin.x + xoff
		self.prevXoffset = xoff
