import copy
import gamelevel3_x
from player import *
from pgu import tilevid

import base
from base import TILE_SIZE

from tilesets.templetiles import Tileset
from enemies.fallingblock import *

from pygame import Rect


class GameLevel(gamelevel3_x.GameLevel, Tileset):
	level_maj = 3
	level_min = 4 
	levelFileName = "level3_4"
	blocksToDestroy = [] # Create an empty list of blocks, this is populated in OnRunSpecial4
	
	def OnRunSpecial1(self, g, t, a):
		def special_hit1(g, s, a):
			g.hud.add_pending_dialog(_("""Hint: This mound is too high for Dave to jump up to. Why don't you jump on the other mound to the left and then
\tjump on the tree branch and onto the mound from there?"""))
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit1
		
	def OnRunSpecial2(self, g, t, a):
		def special_hit2(g, s, a):
			g.hud.add_pending_dialog(_("""\"Hrm. Maybe I should jump on that tree branch to the right so that I don't have to cross paths with this jaguar.\""""))
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit2
			
		
	def OnRunSpecial3(self, g, t, a):
		def special_hit3(g, s, a):
			self.disapearingBranch(g)
			self.hud.show_dialog(_("""*CRACK!* Oops! This branch wasn't strong enough to hold Dave!!"""))
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit3
		
	def OnRunSpecial4(self, g, t, a):
                self.appendTileFromTrigger(self.blocksToDestroy,t)
                self.removeBlocks(self.blocksToDestroy)
                self.addBlocks(self.blocksToDestroy)
		
	def OnRunSpecial5(self, g, t, a):
		def special_hit5(g, s, a):
			self.hud.show_dialog(_("""A tree snake! Maybe you should climb that other vine."""))		
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit5
		
	def OnRunSpecial6(self, g, t, a):
		def special_hit6(g, s, a):
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

	def appendTileFromTrigger(self,array,t):
		x = t.rect.x / TILE_SIZE
		y = t.rect.y / TILE_SIZE
		tile = copy.copy(self.tlayer[y][x])
		array.append(((x,y),tile))

	def disapearingBranch(self, game):
		self.removeBlocks(self.blocksToDestroy)
		
	def OnExit(self):
		self.gotoNextLevel()
