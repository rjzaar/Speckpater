from enemy import BaseEnemy
from pgu.tilevid import Sprite
from pygame import transform
from pygame import Rect
import random
import math
from base import TILE_SIZE
from base import difficultyMulStep
import copy

POPUP_SPEED = 0.1

class PopupEnemy(BaseEnemy):
	"""
	sprname = sprite key name in game.images array
	numFrames = number of sprite keys. the key is built like this: sprname + "_x"
	rotation = angle in degrees this sprite is rotated on each time before drawing
	flips = tuple of booleans indication whether or not the image/moving 
	 direction should be flipped/reversed
	area = the area in tiles around pos which triggers attack. like: (x_offset, y_offset, width, height)
	speed = defines attack speed and pulling back speed which is 1/4 of it
	"""
	def __init__(self, g, sprname,numFrames,animInterval, pos, rotation, flips, area, trouble, speed = POPUP_SPEED):
		def onCollision(g, s, a):
			self.hitDave = 1
			
			if g.daveInTrouble(self.trouble):
				print "Ouch!"
				#todo, sound
				
		BaseEnemy.__init__(self,g, g.images[sprname + "_1"], pos)

		self.sprname = sprname
		self.animInterval = animInterval
		self.maxFrames = numFrames
		self.rotation, self.flips = rotation, flips
		
		self.orgRect = copy.copy(self.rect)
		self.area = Rect(self.orgRect.x + area[0] * TILE_SIZE, self.orgRect.y + area[1] * TILE_SIZE, 
											area[2] * TILE_SIZE, area[3] * TILE_SIZE)
			
		self.hit = onCollision
		
		self.trouble = trouble
		self.popupSpeed = speed * difficultyMulStep(0.2)
		self.backupSpeed = self.popupSpeed / 4
		
		self.posPercent = 1.0 #1.0 * random.random()
		self.moveDir = 0 #1
		
		self.hitDave = 0

		self.cdbgmsg = ""
		
		
	def dbgMsg(self,msg):
		if msg != self.cdbgmsg:
			print msg
			self.cdbgmsg = msg
			
	def loop(self, game, sprite):
		self.__move(game)
		self.__animate(game)


	def __animate(self, game):

		if ((game.frame % self.animInterval) == 0):
			self.anim_frame += 1
		
			if (self.anim_frame > self.maxFrames):
				self.anim_frame = 1
			if (self.anim_frame <= 0):
				self.anim_frame = self.maxFrames

				
		imageString = self.sprname + "_" + str(self.anim_frame)
		
		# if we flip the y then we must move adjust the rect.x
		if self.flips[1]:
			self.rect.x = self.orgRect.x + self.posPercent * self.orgRect.height - self.orgRect.height + TILE_SIZE
		else:
			self.rect.x = self.orgRect.x
			
		# clip part of the image
		img = transform.chop(game.images[imageString][0], Rect(0,0,0,self.posPercent * self.orgRect.height))
		
		# apply flipping and rotation if required
		if self.flips[0] or self.flips[1]:
			img = transform.flip(img, self.flips[0], self.flips[1])
		if self.rotation != 0:
			img = transform.rotate(img, self.rotation)
			
		self.setimage(img)


	def __move(self, game):
		
		if game.player == None: return
		
		if (self.moveDir == 0 or (self.moveDir == -1 and self.hitDave == 0)) and self.area.colliderect(game.player.rect):
			self.moveDir = 1
				
		if self.moveDir == 1:	
				
			self.posPercent -= self.popupSpeed
			if self.posPercent <= 0.0:
				self.posPercent = 0.0
				self.moveDir = -1
						
		elif self.moveDir == -1:
				
			self.posPercent += self.backupSpeed
			if self.posPercent >= 1.0:
				self.posPercent = 1.0
				self.moveDir = 0
				self.hitDave = 0
					
				
				
		# self.posPercent -= self.moveDir * AVERAGE_SPEED
		# if self.posPercent < 0.0 or self.posPercent >= 1.0:
			# self.moveDir = -self.moveDir
			# self.posPercent = 1.0 * self.moveDir == 1
			

