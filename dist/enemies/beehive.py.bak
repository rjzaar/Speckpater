import base
import pygame
import random
from enemy import BaseEnemy
from beeswarm import BeeSwarm
from pgu.tilevid import Sprite

# -------------------- #
# Bee Hive Enemy Class #
# -------------------- #
class BeeHive(BaseEnemy):
	def __init__(self, g, pos):
		def on_collision(g, s, a):
			#Eventually it would be great that if Dave touches the nest, the nest falls over and the bees never stop following Dave because they have no home to go back to.			
			pass

		Sprite.__init__(self, g.images['beehive'], pos)

		self.groups = g.string2groups('enemy')
		self.agroups = g.string2groups('player')

		self.hit = on_collision

		self.beeswarm = 0


	def loop(self, g, sprite):

		if (self.beeswarm == 0):
			self.beeswarm = BeeSwarm(g, self.rect)
			g.sprites.append(self.beeswarm)

		pass

		