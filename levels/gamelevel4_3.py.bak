import copy
import gamelevel4_x
from player import *
from pgu import tilevid

import base
from base import TILE_SIZE

from tilesets.templetiles import Tileset

from pygame import Rect

class GameLevel(gamelevel4_x.GameLevel, Tileset):
	level_maj = 4
	level_min = 3
	levelFileName = "level4_3"
	blocksToDestroy = [] # Create an empty list of blocks, this is populated in OnRunSpecial8
	clunkCounter = 0
	
	def OnRunSpecial1(self, g, t, a):
		g.player.lastTouchplate = 0 #When the level starts, initialize the player to have not touched any touchplates.
		g.player.correctOrder = 0 #When the level starts, the correct order is not being followed.
		g.player.puzzleFinished = 0 #When the level starts, the puzzle is not finished.
		def special_hit1(g, s, a):
			if (g.player.lastTouchplate <> 1) and (g.player.puzzleFinished <> 1):
				if (g.player.correctOrder == 1): ## If it was the correct order, then they just botched it, so clunk, then click.
					self.Clunk(g)

				g.player.lastTouchplate = 1
				g.player.correctOrder = 1
				self.Click(g)
		s = tilevid.Sprite(g.images['blank'],t.rect)
		s.rect.y = s.rect.y - 1 # Move the touchplate up a pixel so that the player can collide with it.
		g.sprites.append(s)
		s.agroups = g.string2groups('player')	## Set the 'player' group to collide with this object
		s.hit = special_hit1

	def OnRunSpecial2(self, g, t, a):
		def special_hit2(g, s, a):
			if (g.player.lastTouchplate <> 2) and (g.player.puzzleFinished <> 1):
				if (g.player.lastTouchplate == 1):
					self.Click(g)
				else:
					self.Clunk(g)
					g.player.correctOrder = 0
				g.player.lastTouchplate = 2
		s = tilevid.Sprite(g.images['blank'],t.rect)
		s.rect.y = s.rect.y - 1 # Move the touchplate up a pixel so that the player can collide with it.
		g.sprites.append(s)
		s.agroups = g.string2groups('player')	## Set the 'player' group to collide with this object
		s.hit = special_hit2

	def OnRunSpecial3(self, g, t, a):
		def special_hit3(g, s, a):
			if (g.player.lastTouchplate <> 3) and (g.player.puzzleFinished <> 1):
				if (g.player.lastTouchplate == 2):
					self.Click(g)
				else:
					self.Clunk(g)
					g.player.correctOrder = 0
				g.player.lastTouchplate = 3
		s = tilevid.Sprite(g.images['blank'],t.rect)
		s.rect.y = s.rect.y - 1 # Move the touchplate up a pixel so that the player can collide with it.
		g.sprites.append(s)
		s.agroups = g.string2groups('player')	## Set the 'player' group to collide with this object
		s.hit = special_hit3

	def OnRunSpecial4(self, g, t, a):
		def special_hit4(g, s, a):
			if (g.player.lastTouchplate <> 4) and (g.player.puzzleFinished <> 1):
				if (g.player.lastTouchplate == 3):
					g.player.puzzleFinished = 1
					if base.SOUND:
						base.sound.Play("click")
					g.hud.add_pending_dialog(_("*Interesting way to keep people from getting out."));
					g.quake = 75
					self.OnPuzzleSolved(g)
				else:
					self.Clunk(g)
					g.player.correctOrder = 0
				g.player.lastTouchplate = 4
		s = tilevid.Sprite(g.images['blank'],t.rect)
		s.rect.y = s.rect.y - 1 # Move the touchplate up a pixel so that the player can collide with it.
		g.sprites.append(s)
		s.agroups = g.string2groups('player')	## Set the 'player' group to collide with this object
		s.hit = special_hit4

	def OnRunSpecial7(self, g, t, a):
		def special_hit7(g, s, a):
			if (g.player.puzzleFinished == 0):
				g.hud.add_pending_dialog(_("""These blocks are in my way...\nthere's got to be some trick to getting past them."""));
			s.agroups = None	## Remove the groups from colliding with this object in the future
		
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')	## Set the 'player' group to collide with this object
		s.hit = special_hit7
	
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
			
	def OnRunSpecial8(self, g, t, a):
		self.appendTileFromTrigger(self.blocksToDestroy,t)
		
	def Click(self, g):
		if base.SOUND:
			base.sound.Play("click")
		g.hud.show_dialog(_("*Click*"))

	def Clunk(self, g):
		self.clunkCounter += 1

		if base.SOUND:
			base.sound.Play("clunk")
		if (self.clunkCounter == 7):
			g.hud.add_pending_dialog(_("*Clunk*\n\t""I can't help thinking that these clunks\nare messing things up."""))
		elif (self.clunkCounter == 14):
			g.hud.add_pending_dialog(_("*Clunk*\n\t""Maybe there's an order I should be\nstepping on these things in."""))
		elif (self.clunkCounter == 21):
			g.hud.add_pending_dialog(_("*Clunk*\n\t""I bet if I jumped over some plates and\nstepped on other ones instead, I could get\nmore to click into place."""))
		elif (self.clunkCounter == 28):
			g.hud.add_pending_dialog(_("*Clunk*\n\t""I think I should start with that first\none that clicks, and then try to find\nthe next one to step on to make it click."""))
		elif (self.clunkCounter == 35):
			g.hud.add_pending_dialog(_("*Clunk*\n\t""Those clunks are starting to get on my nerves. Maybe I need to get all clicks?"""))
		elif (self.clunkCounter == 42):
			g.hud.show_dialog(_("*Clunk*\n\t""Is this really getting me anywhere?"""))
		elif (self.clunkCounter == 49):
			g.hud.add_pending_dialog(_("*Clunk*\n\t""Okay Dave. Let's check our Fruit status...\n\tlove...\tgood.\n\tjoy...\tgood.\n\tpeace...\t...\tacceptable\n\tpatience...\t...\t...\t...\t...I think\nI've just about lost all my available patience."""))
		elif (self.clunkCounter == 56):
			g.hud.show_dialog(_("*Clunk*\n\t""Are we ever going to get out of here?"""))
			self.clunkCounter = 0
		else:
			g.hud.show_dialog(_("*Clunk*"))

	def OnPuzzleSolved(self, game):
		self.removeBlocks(self.blocksToDestroy)
		#for currTile in self.blocksToDestroy:
			# The upper-left-most tile in the map needs to be blank (or whatever tile you want each destroyed block to be a copy of)
			#game.tlayer[currTile.y / 32][currTile.x / TILE_SIZE] = copy.copy(game.tlayer[0][0])
			#game.tlayer[(currTile.x) / 32][(currTile.y) / TILE_SIZE] = copy.copy(game.tlayer[0][0])
	
	def OnExit(self):
		self.gotoNextLevel()
