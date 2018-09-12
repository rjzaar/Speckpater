import gamelevel1_x
from player import *
from pgu import tilevid

class GameLevel(gamelevel1_x.GameLevel):
	level_maj = 1
	level_min = 5
	levelFileName = "level1_5"
	
	def OnStart(self):
		self.cracked_branch = 0
		#self.hud.show_dialog(_("\"I've got a long way to go,\nand it looks like it's going to rain.\nI pray I can find good shelter soon!\""));

	def OnRunSpecial1(self, g, t, a):
		pass
		#def special_hit(g, s, a):
		#	g.hud.show_dialog("Hint:\nYou can press 'space' for Dave to jump,\nand 'up' for him to climb vines!");
		#	s.agroups = None
		#
		#s = tilevid.Sprite(g.images['blank'],t.rect)
		#g.sprites.append(s)
		#s.agroups = g.string2groups('player')
		#s.hit = special_hit

	def OnRunSpecial2(self, g, t, a):
		def special_hit(g, s, a):
			g.hud.add_pending_dialog(_("\"Try jumping on the stepping stones to cross the waterfall.\""));
			s.agroups = None
		
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit

	def OnRunSpecial3(self, g, t, a):
		def special_hit(g, s, a):
			if (not g.cracked_branch):
				g.cracked_branch = 1
				g.hud.show_dialog(_("\"Uh oh! Dave has slipped!\""));
			s.agroups = None
		
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit


	def OnExit(self):
		#self.hud.show_dialog(_("\"Please save me, Lord!\""));
		self.gotoNextLevel()
