import base
import pygame
import random
from enemy import BaseEnemy
from pgu.tilevid import Sprite
from pygame import transform

# ----------------- #
# Guava Enemy Class #
# ----------------- #
class Guava(BaseEnemy):
	def __init__(self, g, pos):
		def on_collision(g, s, a):
			if g.daveInTrouble(10):
				if base.SOUND:
					base.sound.Play("Thud")
				print "Ouch! Unripened guava!"
				g.sprites.remove(self)

		Sprite.__init__(self, transform.rotate(g.images['guava'][0], random.randrange(0, 360)) , pos)
		self.groups = g.string2groups('enemy')
		self.agroups = g.string2groups('player')
		self.anim_frame = 1
		self.dy = 0.0
		self.dx = random.randrange(-10, 11) / 10.0
		self.x = self.rect.x
		self.y = self.rect.y

		self.hit = on_collision

	def loop(self, g, sprite):
		self.__move(g)

	def __move(self, g):
		maxYVel = 12
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
		
