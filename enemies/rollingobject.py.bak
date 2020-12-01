import base
import pygame
import random
from enemy import BaseEnemy
from pgu.tilevid import Sprite
from pygame import transform
import copy
from pygame import Rect
import math

from base import MAX_VELOCITY, GRAVITY,TILE_SIZE

class RollingObject(BaseEnemy):
	def __init__(self, g, sprname, pos, initialXVel, hasFriction):
		def onCollision(g, s, a):
			velMul = int(math.sqrt(self.dx*self.dx+self.dy*self.dy)) / 3

			if g.daveInTrouble(velMul * 15):
				if base.SOUND:
					base.sound.Play("Thud")
				print "Ouch!"

		BaseEnemy.__init__(self,g, g.images[sprname][0], pos)
		self.groups += g.string2groups('genemy')
		self.hit = onCollision
		
		self.sprname = sprname
		
		self.dy = self.dx = 0.0
		self.rotation = 0.0
		
		self.hasFriction = hasFriction
		self.dx = initialXVel
		
		self.yrc = 0
		
		self.orgRect = copy.copy(self.rect)
		
	def applyFriction(self):
		if not self.hasFriction:
			return
		
		self.dx /= 1.02
		if(abs(self.dx) < 1.0): 
			self.dx = 0.0

		
	def onClimbableTile(self, t):
		pass
	def onTopLineContact(self, t):
		self.applyFriction()
		self.rect.bottom = t.rect.top
		# bounce only if enough velocity, dy wont ever be zero because of gravity
		if abs(self.dy) >= 2.0:
			self.dy = -self.dy / 5.0
		else:
			self.dy = 0
	def onBottomLineContact(self, t):
		self.dy /= 2.0
		self.dy = -a.dy
	def onLeftLineContact(self, t):
		self.rect.right = t.rect.left
		if self.hasFriction:
			self.dx /= 1.2
		self.dx = -self.dx
	def onRightLineContact(self, t):
		self.rect.left = t.rect.right
		if self.hasFriction:
			self.dx /= 1.2
		self.dx = -self.dx
		

	def loop(self, g, sprite):
		self.__move(g)
		self.__animate(g)

	def __move(self, g):
			
		self.dy += GRAVITY
		if self.dy > MAX_VELOCITY:
			self.dy = MAX_VELOCITY
		
		self.rect.y += self.dy
		self.rect.x += self.dx

		#if abs(self.dx) >= 1.0: 
		# applyFriction should make sure that dx isnt left between zero and one
		
		self.rotation -= self.dx
		
		# remove this object if it goes off the screen
		if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.top >= (len(g.tlayer) * TILE_SIZE) or self.rect.left >= (len(g.tlayer[0]) * TILE_SIZE):
			#print "out of map"
			g.sprites.remove(self)
			
	def __animate(self, g):
		
		#rotate the image (creates new surface)
		img = transform.rotate(g.images[self.sprname][0], self.rotation)
		
		# now since the surface is rotated it is also bigger so we need to clip it so
		# that the size is same as the original surface's size, this is really slow
		rect = img.get_rect()
		ydif = (rect.height - self.orgRect.height) / 2
		xdif = (rect.width - self.orgRect.width) / 2
		
		img = transform.chop(img,Rect(0,rect.height - ydif,0,ydif))
		img = transform.chop(img,Rect(0,0,0,ydif))

		img = transform.chop(img,Rect(rect.width - xdif,0,xdif,0))
		img = transform.chop(img,Rect(0,0,xdif,0))
		
		self.setimage(img)

		