import gamelevel5_x
from player import *
from pgu import tilevid

from tilesets.mountaintiles import Tileset

class GameLevel(gamelevel5_x.GameLevel, Tileset):
	level_maj = 5
	level_min = 1
	levelFileName = "level5_1"

				
	def OnRunSpecial1(self, g, t, a):
		def trigger(g, s, a):
			g.hud.add_pending_dialog(_("\"How did the Bibles get all the way up here?\""))
			s.agroups = None	
		self.addTriggerCallback(t.rect,trigger)
		
		
	def OnRunSpecial2(self, g, t, a):
		def trigger(g, s, a):
                        g.hud.add_pending_dialog(_("""Eagles! Those are beautifully designed creatures!
                        Be careful though, eagles have their teritory, and are very aggresive."""));
                        s.agroups = None
                self.addTriggerCallback(t.rect,trigger)
	
	def OnExit(self):
		self.gotoNextLevel()

