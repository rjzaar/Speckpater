import gamelevel5_x
from player import *
from pgu import tilevid

from tilesets.commontiles import Tileset

class GameLevel(gamelevel5_x.GameLevel, Tileset):
	level_maj = 5
	level_min = 2
	levelFileName = "level5_2"
	
	
	def OnRunSpecial1(self, g, t, a):
		def trigger(g, s, a):
			g.hud.add_pending_dialog(_("""\"Another Bible for the lost, thank you Jesus!\"
			Hmmm there seems to be bit dirt on this text... There now it's clean!
			Psalm 118, verse 22,  'The stone which the builders refused is
			'become the head stone of the corner.'
			Aah yes that is important verse to remember."""))
			s.agroups = None

		self.addTriggerCallback(t.rect,trigger)
		
	def OnRunSpecial2(self, g, t, a):
		def trigger(g, s, a):
			g.hud.show_dialog(_("\"Wow slippy rock!\""))
			s.agroups = None

		self.addTriggerCallback(t.rect,trigger)

	def OnExit(self):
		self.gotoNextLevel()
