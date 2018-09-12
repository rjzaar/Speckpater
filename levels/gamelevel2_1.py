import gamelevel2_x
import base
from pgu import tilevid

class GameLevel(gamelevel2_x.GameLevel):
	level_maj = 2
	level_min = 1
	levelFileName = "level2_1"
	
	def OnStart(self):
		self.hit_ground = 0
		self.hud.show_dialog(_("\"...aaaaAAAAH!\""));

	def OnRunSpecial1(self, g, t, a):
		def special_hit1(g, s, a):
			if (not g.hit_ground):
				if base.SOUND:
					base.sound.Play("oof1")
				g.hit_ground = 1
			s.agroups = None

		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit1

	def OnRunSpecial2(self, g, t, a):
		def special_hit(g, s, a):
			g.hud.add_pending_dialog(_("\"This looks like a mine... or maybe a cave...\""));
			#a.dx = 4 # kick the player to the right a bit when this happens			
			#g.quake = 200
			s.agroups = None

		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit


	def OnRunSpecial3(self, g, t, a):
		def special_hit(g, s, a):
			#g.hud.show_dialog(_("\"It's stopped.\n\tI think that must have been a landslide,\nthe cave entrance looks closed off now.\n\tI'll just have to find another way out.\""));
			g.quake = 0
			s.agroups = None

		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit


	def OnExit(self):
		self.hud.show_dialog(_("\"This passage looks good, even if it's the only one... I'll keep going.\""));
		self.gotoNextLevel()
