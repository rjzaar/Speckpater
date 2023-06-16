from enemy import BaseEnemy
from pgu.tilevid import Sprite
import random
import math
from base import TILE_SIZE
from base import FPS
from base import difficultyMul, difficultyMulStep

# state times

MAX_SECS_WANDER = 12
MIN_SECS_WANDER = 3

MAX_SECS_IDLE = 7
MIN_SECS_IDLE = 3

# distances

CHASE_DIST = 12 # in tiles

# states

STATE_IDLE = 0
STATE_CHASING = 1
STATE_WILD = 2

STATE_WANDERING = 3
STATE_RESTING = 4

def	distance(p1,p2):
	x = p1.x - p2.x
	y = p1.y - p2.y
	return math.sqrt(x*x+y*y)	
	
def clamp(val,min,max):
	if val < min: return min
	if val > max: return max
	return val
	
def getSpriteTileCoord(s):
	from pygame import Rect
	return Rect((s.rect.x / TILE_SIZE, s.rect.y / TILE_SIZE),(int((s.rect.width-1) / TILE_SIZE) + 1,int((s.rect.height-1) / TILE_SIZE) + 1))
	

class GroundEnemy(BaseEnemy):
	"""
	pos = starting position
	wd = wandering distance in tiles from starting position
	maxSpeed = how fast this one can move, wandering speed is half of maxSpeed
	maxAccel = determines how long it takes to reach the maxium speed
	"""
	def __init__(self, g, ishape, pos, wd, maxSpeed, maxAccel):
		def onDaveReached(g, s, a):
			pass

		self.dy = self.dx = 0
		BaseEnemy.__init__(self,g, ishape, pos)
		self.groups += g.string2groups('genemy')
		self.hit = onDaveReached
		
		self.state = None	
		self.on_ground = 0
		
		self.wayBlocked = False
		self.movingDir = 1
		
		# used in wander()
		self.origin = pos
		self.wanderState = STATE_IDLE
		self.wanderDistance = wd * TILE_SIZE
		
		# used in chase()
		self.chaseState = STATE_CHASING
		self.goneWild = 0
		
		if(maxSpeed >= TILE_SIZE): 
			raise Exception("maxSpeed must be less than TILE_SIZE")
		
		maxSpeed *= difficultyMulStep(0.15)
		maxAccel *= difficultyMulStep(0.1)
		self.maxSpeed = maxSpeed
		self.xChaseAccel = maxAccel
		self.wanderSpeed = self.maxSpeed / 2
		self.xWanderAccel = self.xChaseAccel / 3
		
		self.stateTimer = 0
		
		self.cdbgmsg = ""
		
		self.numTilesTall = self.rect.height / TILE_SIZE
		
		self.hasMoveCommand = False
		
	def onClimbableTile(self, t):
		pass
	def onTopLineContact(self, t):
		self.rect.bottom = t.rect.top
		self.on_ground = 1
		self.dy = 0
	def onBottomLineContact(self, t):
		self.dy = 0
	def onLeftLineContact(self, t):
		self.rect.right = t.rect.left
		self.dx = 0
		#self.wayBlocked = True
	def onRightLineContact(self, t):
		self.rect.left = t.rect.right
		self.dx = 0
		#self.wayBlocked = True
		
	def dbgMsg(self,msg):
		if msg != self.cdbgmsg:
			#print msg
			self.cdbgmsg = msg

	def move(self,dx,max):
		if self.on_ground == 0:
			raise "cant move ground enemy in air"
		if dx == 0.0:
			raise "no move amount in ground enemy move"
			
		self.dx += dx
		self.dx = clamp(self.dx,-max,max)
		self.hasMoveCommand = True
			
	def customBehaviour(self,game):
		return False
			
	def wander(self,game):
		if self.wanderState == STATE_IDLE:
			self.dbgMsg("starting wander")
			self.movingDir = -self.movingDir
			self.wayBlocked = False
			self.wanderState = STATE_WANDERING
			self.stateTimer = FPS * random.randrange(MIN_SECS_WANDER, MAX_SECS_WANDER)
				
		# if we are supposed to move but dx is zero it means we have hit to a wall		
		elif self.wanderState == STATE_WANDERING:
			if self.wayBlocked == True: #self.dx == 0:
				self.movingDir = -self.movingDir
				self.wayBlocked = False
				self.dbgMsg("end of road, turning")

			if self.movingDir == 1:
				if (self.rect.x - self.origin.x) > self.wanderDistance:
					self.dbgMsg("turning west")
					self.movingDir = -1
			else:
				if (self.origin.x - self.rect.x) > self.wanderDistance:
					self.dbgMsg("turning east")
					self.movingDir = 1
				
			if not self.canMoveToDir(game,self.movingDir):
				self.dbgMsg("whoa, almost fell")
				self.stop()
				self.wayBlocked = True
				#dont turn yet, above code does that
			else:
				self.dbgMsg("wandering...")
				self.move(self.movingDir * self.xWanderAccel, self.wanderSpeed)
			
			if self.stateTimer == 0:
				self.dbgMsg("tired of wandering, taking a break")
				self.wanderState = STATE_RESTING
				self.stateTimer = FPS * random.randrange(MIN_SECS_IDLE, MAX_SECS_IDLE)
				
		elif self.wanderState == STATE_RESTING:
			self.dx = 0
			if self.stateTimer == 0:
				self.dbgMsg("end of break")
				self.wanderState = STATE_IDLE
		
	def chase(self,game):
		disttod = game.player.rect.x - (self.rect.x + self.dx)

		dir = 1
		if disttod < 0: dir = -1
		
		# do state specific movement
		
		if self.chaseState == STATE_IDLE:
			#print "STATE_IDLE"
			self.stop()
		elif self.chaseState == STATE_CHASING:
			#print "STATE_CHASING"
				
			if self.canMoveToDir(game,dir):
				self.dbgMsg("chasing!")
				
				if abs(disttod) > 0:
					self.move(dir * min(abs(disttod),self.xChaseAccel),self.maxSpeed)
				else:
					self.stop()
				#self.movingDir = dir
			else:
				self.dbgMsg("cant follow " + str(self.stateTimer))
				# can't reach so just stop, the state will changed to STATE_WILD
				self.stop()
				self.wayBlocked = True
				
				# set this so we look litle cunfused for a while before going wild
				if self.stateTimer == 0:
					# if we just returned from wild state dont get confused any more
						self.stateTimer = FPS * (self.goneWild == 0) + 1
				
		# move to other direction, away from the player since he cant be reached
		elif self.chaseState == STATE_WILD:
			#print "STATE_WILD"
			
			# just move back and forward for a while
			# but dont go too far
			# if self.movingDir != dir and abs(disttod) > TILE_SIZE * 2:
				 # # only if we could move to the other direction
				 # if self.canMoveToDir(game, -self.movingDir):
					 # self.dbgMsg("changin wild dir")
					 # self.movingDir = -self.movingDir
				
			if self.canMoveToDir(game,self.movingDir):
				self.move(self.xChaseAccel * self.movingDir,self.maxSpeed)
			else:
				# this would mean that we are in a very narrow land
				self.stop()
				#self.wayBlocked = True
				self.movingDir = -self.movingDir

				
		# make the state change decisions
		
					
		if self.chaseState == STATE_IDLE:
			# need to reset some vars this way
			self.chaseState = STATE_CHASING 
			self.goneWild = 0
			self.stateTimer = 0
		 
		if self.chaseState == STATE_CHASING and self.wayBlocked == True and self.stateTimer == 1:
			self.dbgMsg("he got away!")
			self.chaseState = STATE_WILD
			self.stateTimer = FPS * 0.8
			self.wayBlocked = False
			# goto opposite direction
			self.movingDir = -dir
			self.goneWild = 1
			
			# try to chase the player again, in case he can be reached now
			# even couldnt this creates back and forward movement
		if self.chaseState == STATE_WILD and self.stateTimer == 0:
			self.dbgMsg("from wild back to chase")
			self.chaseState = STATE_CHASING
	
	def stop(self):
		self.dx = 0

	def	canMoveToDir(self,game, dir):
		try:
			feetY = (self.rect.y + self.rect.height) / TILE_SIZE
			headY = (self.rect.y) / TILE_SIZE
			
			tileX = 0
			tileColKeyName = ''

			if dir == -1:
				tileX = (self.rect.x - 1) / TILE_SIZE 
				#tileType = game.tlayer[feetY][tileX] # get the next ground tile
				#if(tileType == 0): return False # if no ground tile
				# set this so that we will check tiles that block from right
				# since we are moving left
				tileColKeyName = 'right'
				
			elif dir == 1:
				tileX = (self.rect.x + self.rect.width) / TILE_SIZE
				#tileType = game.tlayer[feetY][tileX] 
				#if(tileType == 0): return False
				tileColKeyName = 'left'
				
			else:
				Except("unknown dir in canMoveToDir() : " + str(dir))
				
			tileType = game.tlayer[feetY][tileX] # get the next ground tile
			tileInfo = game.tdata.get(tileType)
			if tileInfo == None or tileInfo[2]['top'] == 0: 
				return False # not a solid ground
				
			# now check the all tiles that are between head and feet
			for tileY in range(feetY - 1,headY):
				tileType = game.tlayer[tileY][tileX]
				tileInfo = game.tdata.get(tileType)
				if tileInfo != None and tileInfo[2][tileColKeyName] == 1:
					return False
			
				# looks clear
			return True

		except IndexError:
			print "tile index out of range in canMoveToDir()"
			return False
			
			
	def	canMoveToPos(self,game, pos):
		try:
			dir = 1
			if(pos.x < self.rect.x): dir = -1
			
			tileColKeyName = ''

			if dir == -1:
				# set this so that we will check tiles that block from right
				# since we are moving left
				tileColKeyName = 'right'
			elif dir == 1:
				tileColKeyName = 'left'
				
			tileType = game.tlayer[pos.y+pos.height][pos.x] # get the next ground tile
			tileInfo = game.tdata.get(tileType)
			if tileInfo == None or tileInfo[2]['top'] == 0: 
				return False # not a solid ground
				
			# now check the all tiles that are between head and feet
			for tileY in range(pos.y, pos.y + self.numTilesTall):
				tileType = game.tlayer[tileY][pos.x]
				tileInfo = game.tdata.get(tileType)
				if tileInfo != None and tileInfo[2][tileColKeyName] == 1:
					return False
			
				# looks clear
			return True

		except IndexError:
			print "tile index out of range in canMoveToPos()"
			return False
		return True
		
	def isStraightPathFreeTo(self,game,dest):
		ctpos = getSpriteTileCoord(self)
		tpos = ctpos

		if not (ctpos.y <= (dest.y+dest.height) and dest.y <= (ctpos.y + ctpos.height)):
			return False
			
		#if ctpos.y > (dest.y+dest.height) or (ctpos.y + ctpos.height) < dest.y:
		#	return False
		
		while True:
			
			if not self.canMoveToPos(game,tpos):
				return False
				
			if tpos.x == dest.x: break		
			
			if(dest.x < tpos.x):
				tpos.x -= 1
			else:
				tpos.x += 1	
				
		return True
		
		# this makes more accurate check for the y than above function
	def isStraightPathFreeToSpr(self, game, spr):
		
		if self.rect.y >= (spr.rect.bottom) or (self.rect.bottom) < spr.rect.y:
			return False
			
		return self.isStraightPathFreeTo(game, getSpriteTileCoord(spr))
		
		
			
	def loop(self, game, sprite):
		
		if self.on_ground: 
	
			self.hasMoveCommand = False

			if not self.customBehaviour(game):
				disttod = distance(game.player.rect,self.rect)
				ydist = abs(game.player.rect.y - self.rect.y)
		
				if disttod < TILE_SIZE * CHASE_DIST and self.isStraightPathFreeToSpr(game, game.player):
				#and (ydist <= (self.rect.height + TILE_SIZE * 2)): 
					#self.dbgMsg("player in range")
					self.wanderState = STATE_IDLE #reset
					self.chase(game)
					#print "end chase"
				else:
					#keep the chase state reset
					self.chaseState = STATE_IDLE
					self.wander(game)
					#print "end of wander"
				
			if not self.hasMoveCommand:
				self.stop()
			
		#print self.dx, self.movingDir
			if abs(self.dx) > 0:
				d = 1
				if(self.dx < 0): d = -1
				if not self.canMoveToDir(game, d):
					#self.stop()
					print "cant move ", d
		
		self.animate(game)

		self.dy += 0.8
		if self.dy > 8: self.dy = 8

		self.rect.y += self.dy
		self.rect.x += self.dx
		
		if self.stateTimer > 0: self.stateTimer -= 1

	def animate(self, game):
		pass