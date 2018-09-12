from enemy import BaseEnemy
from pgu.tilevid import Sprite
import random
import math
from base import TILE_SIZE
from base import difficultyMul

X_MAX_SPEED = 6.0
X_ACCEL = 2.5
X_WANDER_SPEED = X_MAX_SPEED / 2
X_WANDER_ACCEL = X_ACCEL / 2

class Snake(BaseEnemy):
	def __init__(self, g, pos):
		def onCollision(g, s, a):
			
			if g.daveInTrouble(5):
				print "Ouch! Tree vipers are poisonous!"
				#todo, some snake sound in here perhaps?

		Sprite.__init__(self, g.images['snake_0_1'], pos)

		# Center the snake in the middle of the current tile. This centers it on the vine.
		self.rect.x += (TILE_SIZE - self.rect.width) / 2
		self.rect.y += TILE_SIZE - self.rect.height / 2
		
		# have to setup a float variable for the position to allow different moving speeds
		self.posY = float(self.rect.y)

		self.groups = g.string2groups('enemy')
		self.agroups = g.string2groups('player')
		self.anim_frame = random.randrange(1, 4)

		self.state = None
		self.can_climb = 1

		self.hit = onCollision

		self.direction = -1 # Default to climbing up
		self.speed = difficultyMul()

		self.anim_interval = int(4 / self.speed) 		## How fast the animation proceeds. Higher numbers = slower

		self.on_vine = 0

		self.cdbgmsg = ""
		
	def dbgMsg(self,msg):
		if msg != self.cdbgmsg:
			print msg
			self.cdbgmsg = msg
			
	def loop(self, game, sprite):
		self.__move(game)
		self.__animate(game)

#		self.rect.y += self.dy
#		self.rect.x += self.dx

	def __animate(self, game):
		interval = self.anim_interval
		maxFrames = 3					## How many frames are in the animation

		image_string = "snake_0"

		if ((game.frame % interval) == 0):
			self.anim_frame -= self.direction
			if (self.anim_frame > maxFrames):
				self.anim_frame = 1
			if (self.anim_frame <= 0):
				self.anim_frame = maxFrames

		image_string += "_" + str(self.anim_frame)

		## Set image string
		self.setimage(game.images[image_string])


	def	canMoveToDir(self,game):
		try:
			y_inx = 0
			if self.direction > 0:
				y_inx = (self.rect.y) / TILE_SIZE
			else:
				y_inx = (self.rect.y + self.rect.height) / TILE_SIZE
			x_inx = self.rect.x / TILE_SIZE

			y_inx += self.direction

			tile_type = game.tlayer[y_inx][x_inx]
			tile_info = game.tdata.get(tile_type)

			if (tile_info == None):
				return False
			else:
				#self.dbgMsg("Tile info is " + str(tile_info[2]['can_climb']))
				return tile_info[2]['can_climb']

		except IndexError:
			print "tile index out of range in canMoveToDir()"
			return False


	def __move(self, game):
		if (not self.canMoveToDir(game)):
			self.direction = -self.direction
			#self.dbgMsg("Snake is changing directions...")
		
		self.posY += self.direction * self.speed
		self.rect.y = self.posY

#		self.can_climb = 0