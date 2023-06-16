import gamelevel4_x
from player import *
from pgu import tilevid
from base import TILE_SIZE

import random

from enemies.enemy import *
from enemies.rollingobject import *
from enemies.fallingblock import *

from tilesets.templetiles import Tileset

class GameLevel(gamelevel4_x.GameLevel, Tileset):
	level_maj = 4
	level_min = 2
	levelFileName = "level4_2"
	
	def OnRunSpecial1(self, g, t, a):
		def special_hit1(g, s, a):
			#g.hud.show_dialog(_("\"Wow, a hidden passage!\""));
			s.agroups = None	## Remove the groups from colliding with this object in the future
		
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')	## Set the 'player' group to collide with this object
		s.hit = special_hit1
		
	def launchStone(self,pos,xvel):
		s = RollingObject(self,'rollingstone', (pos[0]*TILE_SIZE,pos[1]*TILE_SIZE), xvel, True)
		self.sprites.append(s)
		
  # first stone trap
	def OnRunSpecial2(self, g, t, a):
		def trigger(g, s, a):
			g.quake = 25
			g.hud.add_pending_dialog(_("\"What's that noise? Sounds like a huge rolling stone.\""));
			s.agroups = None	## Remove the groups from colliding with this object in the future
			self.launchStone((29,7), -5)

		self.addTriggerCallback(t.rect,trigger)

  # stone trap
	def OnRunSpecial3(self, g, t, a):
		def trig(g, s, a):
			s.agroups = None	## Remove the groups from colliding with this object in the future
			g.quake = 20
			self.launchStone((119,11), -4)
			
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = trig
		
	def OnRunSpecial4(self, g, t, a):
		def trig(g, s, a):
			s.agroups = None	## Remove the groups from colliding with this object in the future
			g.quake = 25
			self.launchStone((80,3), -8)
			
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = trig
		
		
	## falling stone block traps 
	# this script needs following import statement:
	# from enemies.rollingobject import *
		
	def dropBlock(self,pos):
		s = FallingBlock(self, (pos[0]*TILE_SIZE,pos[1]*TILE_SIZE), 1)
		self.sprites.append(s)
		
	def OnRunSpecial6(self, g, t, a):
		def trigger(g, s, a):
			s.agroups = None  ## Remove the groups from colliding with this object in the future
			print "dropping blocks!"

			for i in range(0,32):
				g.dropBlock((80 + random.randint(-10, 15), -random.randint(1, 50)))
			
			g.quake = base.FPS * 7

		self.addTriggerCallback(t.rect,trigger) # add a callback to above function
		
		
	def OnExit(self):
		self.gotoNextLevel()