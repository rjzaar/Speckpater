import copy
import gamelevel3_x
from player import *
from pgu import tilevid

import base
from base import TILE_SIZE

from tilesets.templetiles import Tileset
from enemies.fallingblock import *

from pygame import Rect

fallingBrick = False

class GameLevel(gamelevel3_x.GameLevel, Tileset):
	level_maj = 3
	level_min = 3
	levelFileName = "level3_3"
	BlocksToDestroy2 = []
	blocksToDestroy = [] # Create an empty list of blocks, this is populated in OnRunSpecial2 and 4
	BlocksToDestroy3 = []
	useSouthernBridge = False
	fallingBridgeGroup = 1
	
	def fallingBridge(self, pos, xvel):
		s = FallingBlock(self, pos, xvel)
		#g.sprites.append(s)
		self.sprites.append(s)
		
	def OnStart(self):
		self.hud.show_dialog(_("""This is the northern bridge. It is very old, but it is not in as bad a condition as the southern bridge.
\tYou should use the northern bridge as much as possible."""))
	
	def OnRunSpecial1(self, g, t, a):
		def special_hit1(g, s, a):
			g.quake = 5
			if self.fallingBridgeGroup == 1:
				#First group of blocks
				self.disapearingBridge(g)
				self.fallingBridge((224, 352), 5)
				self.fallingBridge((256, 384), 5)
			
				#Second group of blocks
				self.fallingBridge((416, 352), 5)
				self.fallingBridge((480, 352), 5)
				self.fallingBridge((384, 384), 5)
				self.fallingBridge((448, 384), 5)
				self.fallingBridgeGroup = 2
			
			elif self.fallingBridgeGroup == 2:
				#Third group of blocks
				self.fallingBridge((2376, 672), 5)
				self.fallingBridge((2400, 608), 5)
				self.fallingBridge((2464, 640), 5)
				self.fallingBridge((2560, 576), 5)
				self.fallingBridgeGroup = 3
			
			elif self.fallingBridgeGroup == 3:
				#Fourth group of blocks
				self.fallingBridge((2944, 768), 5)
				self.fallingBridge((3040, 736), 5)
				self.fallingBridge((2944, 608), 5)
				self.fallingBridgeGroup = 4
			
			elif self.fallingBridgeGroup == 4:
				#Fifth group of blocks
				self.fallingBridge((3424, 704), 5)
				self.fallingBridge((3488, 672), 5)
				self.fallingBridge((3392, 608), 5)
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit1
		
	def OnRunSpecial2(self, g, t, a):
		def special_hit2(g, s, a):
			if self.useSouthernBridge == False:
				self.hud.show_dialog(_("""Well, it looks like you'll have to use the southern bridge... or what's left of it."""))
				self.useSouthernBridge = True
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit2
			
		self.appendTileFromTrigger(self.blocksToDestroy,t)
		self.removeBlocks(self.blocksToDestroy)
		self.addBlocks(self.blocksToDestroy)
		
	def OnRunSpecial3(self, g, t, a):
		def special_hit3(g, s, a):
			g.quake = 10
			self.disapearingBridge2(g)
			#self.fallingBridge((3872, 1088), 5)
			#self.fallingBridge((3936, 1088), 5)
			#self.fallingBridge((3968, 1056), 5)
			#self.fallingBridge((4000, 1088), 5)
			self.fallingBridge((4032, 1056), 5)
			self.fallingBridge((4160, 1056), 5)
			self.fallingBridge((4224, 1056), 5)
			self.fallingBridge((4352, 1056), 5)
			self.fallingBridge((4384, 1088), 5)
			
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit3
		
	def OnRunSpecial4(self, g, t, a):
                self.appendTileFromTrigger(self.BlocksToDestroy2,t)
                self.removeBlocks(self.BlocksToDestroy2)
                self.addBlocks(self.BlocksToDestroy2)
		
	def OnRunSpecial5(self, g, t, a):
		def special_hit5(g, s, a):
			self.hud.show_dialog(_("""This is the southern bridge. Be careful, it's not in good condition."""))			
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit5
		
	def OnRunSpecial6(self, g, t, a):
		def special_hit6(g, s, a):
			self.hud.show_dialog(_("""Step back!! The southern bridge is collapsing!
\tHint: Quickly! Run to the ledge on the far left. Get as close to the edge as you can."""))
			self.fallingBridge((4224, 992), 5)
			self.fallingBridge((4288, 992), 5)
			self.fallingBridge((4416, 1056), 5)
			self.fallingBridge((4544, 1184), 5)
			self.fallingBridge((4800, 1440), 5)
			
			self.fallingBridge((4288, 1120), 5)
			self.fallingBridge((4384, 1152), 5)
			self.fallingBridge((4480, 1248), 5)
			self.fallingBridge((4320, 736), 5)
			self.fallingBridge((4448, 928), 5)
			self.fallingBridge((4224, 1024), 5)
			self.fallingBridge((4384, 960), 5)
			self.fallingBridge((4480, 1216), 5)
			
			#self.fallingBridge((4324, 992), 5)
			#self.fallingBridge((4388, 992), 5)
			#self.fallingBridge((4316, 1056), 5)
			#self.fallingBridge((4344, 1184), 5)
			#self.fallingBridge((4400, 1440), 5)
			
			self.fallingBridge((4588, 920), 5)
			self.fallingBridge((4384, 1052), 5)
			self.fallingBridge((4280, 1148), 5)
			self.fallingBridge((4320, 836), 5)
			self.fallingBridge((4648, 1228), 5)
			self.fallingBridge((4527, 1024), 5)
			self.fallingBridge((4304, 1060), 5)
			self.fallingBridge((4460, 1116), 5)
			#self.collapsingBridge(g)
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit6
		
	def OnRunSpecial7(self, g, t, a):
                self.appendTileFromTrigger(self.BlocksToDestroy3,t)
                self.removeBlocks2(self.BlocksToDestroy3)
                self.addBlocks(self.BlocksToDestroy3)
	
	def addBlocks(self,blocks):
		for currTile in blocks:
			self.tlayer[currTile[0][1]][currTile[0][0]] = copy.copy(currTile[1])

	def removeBlocks(self,blocks):
		for currTile in blocks:
			self.tlayer[currTile[0][1]][currTile[0][0]] = 0
			self.tlayer[currTile[0][1]][currTile[0][0]] = 7
	
	def removeBlocks2(self,blocks):
		for currTile in blocks:
			self.tlayer[currTile[0][1]][currTile[0][0]] = 0
			self.tlayer[currTile[0][1]][currTile[0][0]] = 80
	
	def removeBlocks(self,blocks):
		for currTile in blocks:
			self.tlayer[currTile[0][1]][currTile[0][0]] = 0
			self.tlayer[currTile[0][1]][currTile[0][0]] = 7

	def appendTileFromTrigger(self,array,t):
		x = t.rect.x / TILE_SIZE
		y = t.rect.y / TILE_SIZE
		tile = copy.copy(self.tlayer[y][x])
		array.append(((x,y),tile))

	def disapearingBridge(self, game):
		self.removeBlocks(self.blocksToDestroy)

	def disapearingBridge2(self, game):
		self.removeBlocks(self.BlocksToDestroy2)
		
	def collapsingBridge(self, game):
		self.removeBlocks2(self.BlocksToDestroy3)
	
		
	def OnExit(self):
		self.gotoNextLevel()
