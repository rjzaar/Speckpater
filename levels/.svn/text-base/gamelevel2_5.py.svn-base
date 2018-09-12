import gamelevel2_x
import base
from pgu import tilevid

class GameLevel(gamelevel2_x.GameLevel):
	level_maj = 2
	level_min = 5
	levelFileName = "level2_5"
	
	def OnStart(self):
		pass

	def OnExit(self):
		self.gotoNextLevel()

	def OnRunSpecial4(self, g, t, a):
		def special_hit(g, s, a):
			g.hud.add_pending_dialog(_("The sign reads:\n\t\"<--- Mine exit\""));
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit

	def OnRunSpecial5(self, g, t, a):
		def special_hit(g, s, a):
			g.hud.add_pending_dialog(_("The sign reads:\n\t\"To mine exit --->\""));
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit

	def OnRunSpecial6(self, g, t, a):
		def special_hit(g, s, a):
			g.hud.show_dialog(_("The sign reads:\n\t\"PROCEED WITH CAUTION: Dangerous mines ahead.\""));
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit

	def OnRunSpecial7(self, g, t, a):
		def special_hit(g, s, a):
			#g.hud.show_dialog(_("The sign reads:\n\t\"DANGER: Last chance to turn back!\""));
			s.agroups = None
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit

	# Trigger #8 will eventually be the one that kicks the player out to the series of extra-difficult cave levels.
	def OnRunSpecial8(self, g, t, a):
		def special_hit(g, s, a):
			#g.hud.show_dialog(_("\"I've got an uneasy feeling about this...\""));
			self.gotoNextLevel()
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit
