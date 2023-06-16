import copy
import gamelevel3_x
from player import *
from pgu import tilevid

import base
from base import TILE_SIZE

from tilesets.templetiles import Tileset

from pygame import Rect

class GameLevel(gamelevel3_x.GameLevel, Tileset):
	level_maj = 4
	level_min = 1
	levelFileName = "level4_1"
	blocksToDestroy = [] # Create an empty list of blocks, this is populated in OnRunSpecial8
	puzzleFinished = 0

		
	def OnRunSpecial1(self, g, t, a):
		def trigger(g, s, a):
			g.hud.add_pending_dialog(_("\"Hmm I wonder how I'm going to get across from here.\nMaybe I should climb to that tree branch.\""))
			s.agroups = None	## Remove the groups from colliding with this object in the future	

		self.addTriggerCallback(t.rect,trigger)
		
	def OnRunSpecial2(self, g, t, a):
		def trigger(g, s, a):
			if not g.isSaid:
				self.hud.show_dialog(_("\"The jump is too long!\""))
				g.isSaid = True
			s.agroups = None

		self.isSaid = False
		self.addTriggerCallback(t.rect,trigger)
		

	
	def OnRunSpecial3(self, g, t, a):
		def trigger(g, s, a):
			if self.puzzleFinished != 1:
				g.hud.add_pending_dialog(_("\"This wall is in the way. How am I going to get around it?\"\n\"I wonder if I need to move something or flip a switch?\""))
			s.agroups = None	## Remove the groups from colliding with this object in the future	
		self.addTriggerCallback(t.rect,trigger)

	def OnRunSpecial4(self, g, t, a):
		self.appendTileFromTrigger(self.blocksToDestroy,t)
		def special_hit4(g, s, a):
			if (self.puzzleFinished == 1):
				g.hud.add_pending_dialog(_("\"It looks like someone doesn't want people going in here."));
				g.quake = 50
				

		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')	## Set the 'player' group to collide with this object
		s.hit = special_hit4

	def OnRunSpecial5(self, g, t, a):
		def special_hit5(g, s, a):
			self.puzzleFinished = 1
			self.OnPuzzleSolved(g)
			if base.SOUND:
					base.sound.Play("click")
			g.hud.add_pending_dialog(_("""Aha! So that's how you get through!"""));
			s.agroups = None	## Remove the groups from colliding with this object in the future
		
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')	## Set the 'player' group to collide with this object
		s.hit = special_hit5
		
	def OnRunSpecial6(self, g, t, a):
		def trigger(g, s, a):
			g.hud.add_pending_dialog(_("\"It looks like someone doesn't want people going in here."));
			g.quake = 50
			s.agroups = None	## Remove the groups from colliding with this object in the future	

		self.addTriggerCallback(t.rect,trigger)
	
	def addBlocks(self,blocks):
		for currTile in blocks:
			self.tlayer[currTile[0][1]][currTile[0][0]] = copy.copy(currTile[1])
		self.created_buffer = 0

	def removeBlocks(self,blocks):
		for currTile in blocks:
			self.tlayer[currTile[0][1]][currTile[0][0]] = 0
		self.created_buffer = 0

	def appendTileFromTrigger(self,array,t):
		x = t.rect.x / TILE_SIZE
		y = t.rect.y / TILE_SIZE
		tile = copy.copy(self.tlayer[y][x])
		array.append(((x,y),tile))
			
	
		
	def Click(self, g):
		if base.SOUND:
			base.sound.Play("click")
		g.hud.show_dialog(_("*Click*"))

	def Clunk(self, g):
		self.clunkCounter += 1

		if base.SOUND:
			base.sound.Play("clunk")

	def OnPuzzleSolved(self, game):
		self.removeBlocks(self.blocksToDestroy)
		#for currTile in self.blocksToDestroy:
			# The upper-left-most tile in the map needs to be blank (or whatever tile you want each destroyed block to be a copy of)
			#game.tlayer[currTile.y / 32][currTile.x / TILE_SIZE] = copy.copy(game.tlayer[0][0])
			#game.tlayer[(currTile.x) / 32][(currTile.y) / TILE_SIZE] = copy.copy(game.tlayer[0][0])
	
	def OnExit(self):
		self.gotoNextLevel()
