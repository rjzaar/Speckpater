import pygame
from pgu.tilevid import Sprite
from pygame import transform 
from base import MAX_VELOCITY, GRAVITY,TILE_SIZE
import random
		
# ----------------------------------------- #
# Class for non player controlled charactes #
# ----------------------------------------- #

class Human(Sprite):
	def __init__(self,g,sprname,pos):
		Sprite.__init__(self,g.images[sprname],pos)
		self.sprname = sprname
		
		self.groups = g.string2groups('colspr')

		#self.anim_frame = 1
		#self.image_string = ""
		self.dy = self.dx = 0
		self.curDir = random.choice((-1,1))

	def onClimbableTile(self, t): pass
	def onBottomLineContact(self, t): pass
	
	def onTopLineContact(self, t):
		self.rect.bottom = t.rect.top
		self.dy = 0
			
	def onLeftLineContact(self, t):	pass
	def onRightLineContact(self, t): pass
		
	def loop(self, game, sprite):
		self.__move(game)
		self.__animate(game)

	def __move(self, game):
		
		self.dy += GRAVITY
		if self.dy > MAX_VELOCITY:
			self.dy = MAX_VELOCITY
			
		self.rect.y += self.dy
		self.rect.x += self.dx
		
	def animate(self, game):
		
		if game.player.rect.x < self.rect.x and self.curDir == 1: 
			img = game.images[self.sprname][0]
			self.setimage(img)
			self.curDir *= -1
		if game.player.rect.x > self.rect.x and self.curDir != 1:
			img = transform.flip(game.images[self.sprname][0], True, False)
			self.setimage(img)
			self.curDir *= -1
			
			
			
			
MAX_PRAISE_FRAMES = 5		

			
class Villager(Human):
	def __init__(self,g,pos):
		Human.__init__(self,g,'villager_1',pos)
		#self.sprname = sprname
		
		self.groups = g.string2groups('colspr')

		
		self.animFrame = random.randint(1,MAX_PRAISE_FRAMES - 1)
		self.animDir = 1
		
	def onClimbableTile(self, t): pass
	def onBottomLineContact(self, t): pass
	
	def onTopLineContact(self, t):
		self.rect.bottom = t.rect.top
		self.dy = 0
			
	def onLeftLineContact(self, t):	pass
	def onRightLineContact(self, t): pass
		
	def loop(self, game, sprite):
		self.__move(game)
		self.animate(game)

	def __move(self, game):
		
		self.dy += GRAVITY
		if self.dy > MAX_VELOCITY:
			self.dy = MAX_VELOCITY
			
		self.rect.y += self.dy
		self.rect.x += self.dx
		
	def animate(self, game):
		if game.villagersPraising:
			interval = 5 					## How fast the villager is animated. Higher numbers = slower


			if ((game.frame % interval) == 0):
				self.animFrame += self.animDir
				if (self.animDir == 1 and self.animFrame == MAX_PRAISE_FRAMES) or (self.animDir == -1 and self.animFrame == 1):
					self.animDir *= -1
					
				image_string = "villager_" + str(self.animFrame)
			
				img = game.images[image_string][0]
				if self.curDir != 1:
					img = transform.flip(img, True, False)
				self.setimage(img)

		else:		
			Human.animate(self, game)

		# 
		# if game.player.rect.x < self.rect.x and self.curDir == 1: 
			# img = game.images[self.sprname][0]
			# self.setimage(img)
			# self.curDir *= -1
		# if game.player.rect.x > self.rect.x and self.curDir != 1:
			# img = transform.flip(game.images[self.sprname][0], True, False)
			# self.setimage(img)
			# self.curDir *= -1
	
