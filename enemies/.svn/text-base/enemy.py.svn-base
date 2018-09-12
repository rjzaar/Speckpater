import pygame
from pgu.tilevid import Sprite

# ---------------- #
# Base Enemy Class #
# ---------------- #
class BaseEnemy(Sprite):
	def __init__(self,g,ishape,pos):
		
		Sprite.__init__(self,ishape,pos)

		self.groups = g.string2groups('enemy')
		self.agroups = g.string2groups('player')
		#self.state = STAND
		#self.direction = RIGHT
		self.anim_frame = 1
		self.image_string = ""
		self.dy = self.dx = 0
		self.can_climb = 0
		self.on_ground = 1

    ## Enemy Loop
	def loop(self, game, sprite):
		self.__move(game)
		self.__animate(game)

	def __move(self, game): pass
	def __animate(self, game): pass
