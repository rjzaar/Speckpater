import gamelevel3_x
from pgu import tilevid
import base

class GameLevel(gamelevel3_x.GameLevel):
	level_maj = 3
	level_min = 1
	levelFileName = "level3_1"
	
	def OnStart(self):
		#self.hud.show_dialog(_("\"Thank you God for getting me out of the dreary caves!\""))
		pass

	def OnRunSpecial1(self, g, t, a):
		def special_hit1(g, s, a):
			g.hud.add_pending_dialog(_("""Hint: These are ground monkeys. Unlike their tree monkey counterparts, these monkeys are easily distracted by bananas.
\t\nTip: Climb this nearby tree and pick a banana. While facing the monkey press 'T' to throw the banana.
\tIf the banana lands near the monkey the monkey will eat it, ignoring you while you walk past. If you overshoot, walk farther away from the monkey and try again.
\tTo climb a tree, walk under a vine, jump, and press the 'Up" arrow key to latch on to it."""))
			s.agroups = None
		
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit1
		
	def OnRunSpecial2(self, g, t, a):
		def special_hit2(g, s, a):
			g.hud.add_pending_dialog(_("""\"What's that!? I thought all the jaguars left the jungle!
\tOh well, I hope it's the last one.\""""))
			s.agroups = None
		
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit2
		
	def OnRunSpecial3(self, g, t, a):
		def special_hit3(g, s, a):
			g.hud.add_pending_dialog(_("""\"Hrmm. This bridge is in bad condition.\""""))
			s.agroups = None
		
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')
		s.hit = special_hit3

	def OnExit(self):
		# this dialog wouldnt be displayed so i commented this out
		#self.hud.show_dialog("This concludes the demo for now!\n\tWe hope you've enjoyed it,\n stay tuned for more!\n\thttp://www.christiancoders.com/");
		#self.nextState = base.GAMEOVER
		self.gotoNextLevel()
