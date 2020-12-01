import gamelevel1_x
from player import *
from pgu import tilevid

class GameLevel(gamelevel1_x.GameLevel):
	level_maj = 1
	level_min = 3
	levelFileName = "level1_3"
	
	def OnStart(self):
		self.hud.add_pending_dialog(_("Hint:\nYou can press 'space' for Dave to jump,\nand 'up' for him to lock on to a vine"))
		self.agroups = None

	def OnRunSpecial1(self, g, t, a):
		pass

	def OnRunSpecial2(self, g, t, a):
		pass
		
	def OnRunSpecial3(self, g, t, a):
		pass
		
	def OnExit(self):
		self.gotoNextLevel()
