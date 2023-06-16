import gamelevel2_x
import base
from pgu import tilevid

class GameLevel(gamelevel2_x.GameLevel):
	level_maj = 2
	level_min = 4
	levelFileName = "level2_4"
	
	def OnStart(self):
		self.hud.show_dialog(_("\"Phew, is it just me or\nis it getting warm in here?\""));

	def OnRunSpecial1(self, g, t, a):
		def special_hit(g, s, a):
			g.hud.add_pending_dialog(_("\"Well that looks like the exit, but the path's caved in!\n\tI pray I can find another way out...\""));
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit

	def OnRunSpecial2(self, g, t, a):
		def special_hit(g, s, a):
			g.hud.add_pending_dialog(_("The sign reads:\n\t\"CAUTION: Lava flows\""));
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit

	def OnRunSpecial3(self, g, t, a):
		def special_hit(g, s, a):
			g.hud.add_pending_dialog(_("The sign reads:\n\t\"Mine exit\""));
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit

	def OnExit(self):
		self.hud.show_dialog(_("\"Fresh air!\""));
		self.gotoNextLevel()
