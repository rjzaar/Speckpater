import gamelevel2_x
import base
from pgu import tilevid

class GameLevel(gamelevel2_x.GameLevel):
	level_maj = 2
	level_min = 2
	levelFileName = "level2_2"
	
	def OnStart(self):
		pass

	def OnRunSpecial1(self, g, t, a):
		pass

	def OnRunSpecial2(self, g, t, a):
		pass

	def OnRunSpecial3(self, g, t, a):
		pass

	def OnExit(self):
		self.gotoNextLevel()
