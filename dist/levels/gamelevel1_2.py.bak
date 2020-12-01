import gamelevel1_x
import base
from pgu import tilevid

class GameLevel(gamelevel1_x.GameLevel):
	level_maj = 1
	level_min = 2
	levelFileName = "level1_2"
	

	def OnRunSpecial1(self, g, t, a):
		def trigger(g, s, a):
			g.hud.show_dialog(_("If you see an exclamation mark above Dave's head, press the M key to see what he wants to say."))
			s.agroups = None	
		self.addTriggerCallback(t.rect,trigger)
		


	def OnRunSpecial2(self, g, t, a):
		def trigger(g, s, a):
			g.hud.add_pending_dialog(_("""\"Tip: You can press the Space bar key to jump.\""""))
			s.agroups = None
		self.addTriggerCallback(t.rect,trigger)

	def OnRunSpecial3(self, g, t, a):
		pass

	def OnExit(self):
		self.gotoNextLevel()
