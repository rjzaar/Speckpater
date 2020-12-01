import copy
import gamelevel4_x
from player import *
from pgu import tilevid

import base
from base import TILE_SIZE

from tilesets.templetiles import Tileset
from enemies.rollingobject import *

from pygame import Rect

class GameLevel(gamelevel4_x.GameLevel, Tileset):
	level_maj = 4
	level_min = 4
	levelFileName = "level4_4"
	BlocksToDestroy2 = [] # Create an empty list of blocks, this is populated in OnRunSpecial8
	def launchStone(self,pos,xvel):
		s = RollingObject(self,'rollingstone', (pos[0]*TILE_SIZE,pos[1]*TILE_SIZE), xvel, True)
		self.sprites.append(s)
					
					
	def OnRunSpecial1(self, g, t, a):
		def special_hit1(g, s, a):
			g.quake = 25
			s.agroups = None        ## Remove the groups from colliding with this object in the future
			self.launchStone((0,14), 5)
			
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit1
		
	def OnRunSpecial3(self, g, t, a):
                self.appendTileFromTrigger(self.BlocksToDestroy2,t)
                self.removeBlocks(self.BlocksToDestroy2)
                self.addBlocks(self.BlocksToDestroy2)
	
	def OnRunSpecial4(self, g, t, a):
		def special_hit4(g, s, a):
			g.quake = 25
			self.FallingRoof2(g)
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit4	
	
	def addBlocks(self,blocks):
		for currTile in blocks:
			self.tlayer[currTile[0][1]][currTile[0][0]] = copy.copy(currTile[1])

	def removeBlocks(self,blocks):
		for currTile in blocks:
			self.tlayer[currTile[0][1]][currTile[0][0]] = 0	

	def appendTileFromTrigger(self,array,t):
		x = t.rect.x / TILE_SIZE
		y = t.rect.y / TILE_SIZE
		tile = copy.copy(self.tlayer[y][x])
		array.append(((x,y),tile))
			
	def OnRunSpecial8(self, g, t, a):
		self.appendTileFromTrigger(self.blocksToDestroy,t)
		self.removeBlocks(self.blocksToDestroy)
		self.addBlocks(self.blocksToDestroy)

	def FallingRoof(self, game):
		self.removeBlocks(self.blocksToDestroy)

	def FallingRoof2(self, game):
		self.removeBlocks(self.BlocksToDestroy2)
		
	def OnExit(self):
		self.gotoNextLevel()
