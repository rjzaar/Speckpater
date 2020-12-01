import gamelevel1_x
import base
from pgu import tilevid

class GameLevel(gamelevel1_x.GameLevel):
	level_maj = 1
	level_min = 1
	levelFileName = "level1_1"
	
	def OnStart(self):
		#base.sound.Play("LevelStart")
		self.found_water = 0
		self.hud.show_dialog(_("""\"Oooh, this splitting headache!
\tThe plane\'s fuel leak must have been worse than I thought.\""""));

	def OnRunSpecial1(self, g, t, a):
		def special_hit1(g, s, a):
			g.hud.show_dialog(_("""What a mess! Thank the Lord I'm okay!
\tWhere is the shipment of Kilopawa New Testaments?
They must have spilled out of the plane!
\tIt looks like the back door popped open again! How long did I fly without noticing it?
\tI need to backtrack and search for the Bibles. The translation dedication is next week!
\tThat gives me 5 days to find at least %d Bibles!""" % base.NEEDED_BIBLES));
			s.agroups = None	## Remove the groups from colliding with this object in the future
		t.rect.x = 50
		t.rect.y = 545
		s = tilevid.Sprite(g.images['crashed_plane'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')	## Set the 'player' group to collide with this object
		s.hit = special_hit1

	def OnRunSpecial2(self, g, t, a):
		def special_hit2(g, s, a):
			s.agroups = None	## Remove the groups from colliding with this object in the future	
			g.hud.add_pending_dialog(_("""Tip: To jump on to this bridge press the spacebar while
holding down the right arrow key.
\tThis will make Dave jump to the right."""))
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')	## Set the 'player' group to collide with this object
		s.hit = special_hit2

	def OnRunSpecial3(self, g, t, a):
		def special_hit3(g, s, a):
			if (not g.found_water):
				g.found_water = 1
				self.hud.show_dialog(_("""These are tree monkeys. They like to throw guavas at you.
Be careful. If you get hit by a guava you will loose encouragment.
\tHint: To see future messages, tips, and hints press the
"M" key when an exclamation point appears over Dave\'s head."""))
			s.agroups = None	## Remove the groups from colliding with this object in the future
		
		s = tilevid.Sprite(g.images['blank'],t.rect)
		g.sprites.append(s)
		s.agroups = g.string2groups('player')	## Set the 'player' group to collide with this object
		s.hit = special_hit3

	def OnExit(self):
		#self.hud.show_dialog("The sign reads,\n\t\"Kilapowa Village\n20 kilometers -->\"");
		self.gotoNextLevel()
