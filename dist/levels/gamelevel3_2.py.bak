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
	level_min = 2
	levelFileName = "level3_2"
	BlocksToDestroy2 = []
	blocksToDestroy = [] # Create an empty list of blocks, this is populated in OnRunSpecial2 and 4
	
	def fallingBridge(self, pos, xvel):
		s = FallingBlock(self, pos, xvel)
		#g.sprites.append(s)
		self.sprites.append(s)
		
	def OnStart(self):
		self.hud.show_dialog(_("""Watch out for falling bridge pieces!"""))
	
	def OnRunSpecial1(self, g, t, a):
		def special_hit1(g, s, a):
			g.quake = 5
			self.fallingBridge((1632, 640), 1)
			self.fallingBridge((1856, 576), 5)
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit1
		
	def OnRunSpecial2(self, g, t, a):
		def special_hit2(g, s, a):
			g.quake = 5
			self.fallingBridge((1952, 668), 5)
			#self.fallingBridge((2080, 668), 5)
			self.fallingBridge((2272, 448), 5)
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit2
		
	def OnRunSpecial3(self, g, t, a):
		def special_hit3(g, s, a):
			g.quake = 5
			self.disapearingBridge(g, 2)
			self.fallingBridge((2624, 1088), 5)
			#self.fallingBridge((2720, 1024), 5)
			self.fallingBridge((2656, 800), 5)
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit3
		
	def OnRunSpecial4(self, g, t, a):
                self.appendTileFromTrigger(self.BlocksToDestroy2,t)
                self.removeBlocks(self.BlocksToDestroy2)
                self.addBlocks(self.BlocksToDestroy2)
	
	def addBlocks(self,blocks):
		for currTile in blocks:
			self.tlayer[currTile[0][1]][currTile[0][0]] = copy.copy(currTile[1])

	def removeBlocks(self,blocks):
		for currTile in blocks:
			self.tlayer[currTile[0][1]][currTile[0][0]] = 0
			self.tlayer[currTile[0][1]][currTile[0][0]] = 7

	def appendTileFromTrigger(self,array,t):
		x = t.rect.x / TILE_SIZE
		y = t.rect.y / TILE_SIZE
		tile = copy.copy(self.tlayer[y][x])
		array.append(((x,y),tile))
			
	def OnRunSpecial8(self, g, t, a):
		self.appendTileFromTrigger(self.blocksToDestroy,t)
		self.removeBlocks(self.blocksToDestroy)
		self.addBlocks(self.blocksToDestroy)

	def disapearingBridge(self, game, chunk):
		if chunk == 1:
			self.removeBlocks(self.blocksToDestroy)
		elif chunk == 2:
			self.removeBlocks(self.BlocksToDestroy2)
		
		#for currTile in self.blocksToDestroy:
		# The upper-left-most tile in the map needs to be blank (or whatever tile you want each destroyed block to be a copy of)
			#game.tlayer[currTile[0][1] / 32][currTile[0][0] / TILE_SIZE] = copy.copy(game.tlayer[0][1])
			#game.tlayer[(currTile[0][0]) / 32][(currTile[0][1]) / TILE_SIZE] = copy.copy(game.tlayer[0][0])
			
		
		

	def FallingRoof2(self, game):
		self.removeBlocks(self.BlocksToDestroy2)
		
	def OnExit(self):
		self.gotoNextLevel()
