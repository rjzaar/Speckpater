import gamelevel6_x
from player import *
from pgu import tilevid
import os, sys
from human import Villager
from random import randrange

# don't set the tileset yet
#from tilesets.templetiles import Tileset
from tilesets.commontiles import Tileset

end_game = True
class GameLevel(gamelevel6_x.GameLevel):
	levelFileName = "kilopowa"
	level_min = 1
	
	villagersPraising = False
	
	def OnStart(self):
		self.skip = False
		if base.num_bibles < base.NEEDED_BIBLES:
			self.hud.show_dialog(_("""Oh no! You only have %d Bibles! You need at least %d total! Dave now has to back track and pick up more Bibles!""" % (base.num_bibles, base.NEEDED_BIBLES)))
			
			base.NEED_MORE_BIBLES = True
		else:
			base.NEED_MORE_BIBLES = False
			
		
	def OnLoop(self):
		pass
		
		# Aaah there, I can see it the kilapowa village praise the Lord my God!
		# For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life. 
		# are you a man of God? - I'm just one of His servants
	
	def OnRunSpecial1(self, g, t, a):
		s = tilevid.Sprite(g.images['hut1'],t.rect)
		g.sprites.append(s)

		
	def OnRunSpecial2(self, g, t, a):
		s = Villager(g, t.rect)
		g.sprites.append(s)
		
	def OnRunSpecial3(self, g, t, a):
		s = tilevid.Sprite(g.images['cauldron'],t.rect)
		g.sprites.append(s)
		
	def OnRunSpecial4(self, g, t, a):
		pass
		
	def OnRunSpecial5(self, g, t, a):
		def trigger(g, s, a):
			g.hud.show_dialog(_("\"Aah there, I can see it, the Kilapowa village!\nPraise the Lord, I'm on time!!\""))
			s.agroups = None	## Remove the groups from colliding with this object in the future	

		self.addTriggerCallback(t.rect,trigger)
	
		
	def OnRunSpecial6(self, g, t, a):
		def trigger(g, s, a):
			#g.hud.show_dialog(_("\"Today has salvation come to this village!\nCome to the living God, all you who hunger!\""),preachTheGospel)
			s.agroups = None	## Remove the groups from colliding with this object in the future	

		self.addTriggerCallback(t.rect,trigger)
		
		def preachTheGospel(g):
			
			g.villagersPraising = False
			
			def setNextPreachingPos(g):
				g.player.setPos((19,13))
				
			def endPreach(g):
				g.villagersPraising = False
				
			#def preach4(g):
				# Act 14:15-17
				g.hud.show_dialog(_(""""""),endPreach)

				
			def preach3(g):
				# could put show_dialog in here if needed
				
				# time to change the location
				g.hud.fade_in_out((0.3,2,0.3),(setNextPreachingPos,None,preach4))
				
			def preach2(g):
				# Joh 3:16
				g.hud.show_dialog(_(""""""),preach3)	
				
			def setFirstPreachingPos(g):
				g.player.setPos((75,13))
				
			def preach1(g):
				# Psa 14:3
				# Joh 8:34
				# Rom 6:23
				g.hud.show_dialog(_("""	"""),preach2)
				
				# begin preaching by first moving in position when screen is faded (dark)
				# and start the dialog when faded out (everything visible) 
			g.hud.fade_in_out((0.3,2,0.3),(setFirstPreachingPos,None,preach1))
			

	def OnRunSpecial7(self, g, t, a):
		def trigger(g, s, a):
			s.agroups = None ## Remove the groups from colliding with this object in the future
			self.skip = True
			

		self.addTriggerCallback(t.rect,trigger)
			
	def OnRunSpecial8(self, g, t, a):
		def trigger(g, s, a):
			s.agroups = None	## Remove the groups from colliding with this object in the future	
		
			g.hud.add_pending_dialog(_(""""""))

		self.addTriggerCallback(t.rect,trigger)

	def OnExit(self):
		if base.NEED_MORE_BIBLES == True:
			base.DATA["chapter"] = randrange(1,5)
			base.DATA["level"] = randrange(1,2) - 1
			self.nextState = base.NEXTLEVEL
		else:
			if self.skip == True:
				self.nextState = base.SHOWGAMEOVER
		
	def loadLevelImages(self):
		gamelevel6_x.GameLevel.loadLevelImages(self)
		self.load_images(self.idata2)

	idata2 = [
		('blank',os.path.join('images', 'blank.png'), (0, 0, 32, 32)),
		('bible',os.path.join('images', 'bible.png'), (0, 0, 32, 32)),
		('hut1', os.path.join('images', 'hut.gif'), (0, 0, 130, 104)),
		('cauldron', os.path.join('images', 'cauldron.png'), (0, 0, 130, 52)),
		('villager_1', os.path.join('images', 'villager_1.png'), (0, 0, 32, 48)),
		('villager_2', os.path.join('images', 'villager_2.png'), (0, 0, 32, 48)),
		('villager_3', os.path.join('images', 'villager_3.png'), (0, 0, 32, 48)),
		('villager_4', os.path.join('images', 'villager_4.png'), (0, 0, 32, 48)),
		('villager_5', os.path.join('images', 'villager_5.png'), (0, 0, 32, 48)),
	]
