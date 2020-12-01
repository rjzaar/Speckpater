
from player import *

class Tileset:
	
	# ------------ #
	#  Tile Block  #
	# ------------ #
	## This is code for a generic block which makes up the obstacles in a level.
	def tile_block(g, t, a):
		c = t.config
		
		if (c['can_climb'] == 1 and (a.rect.left - 16) < t.rect.left and (a.rect.right + 16) > t.rect.right):
			a.onClimbableTile(t)	
			
		if (c['top'] == 1 and a._rect.bottom <= t._rect.top and a.rect.bottom > t.rect.top):
			a.onTopLineContact(t)	
		if (c['left'] == 1 and a._rect.right <= t._rect.left and a.rect.right > t.rect.left):
			a.onLeftLineContact(t)
		if (c['right'] == 1 and a._rect.left >= t._rect.right and a.rect.left < t.rect.right):
			a.onRightLineContact(t)
		if (c['bottom'] == 1 and a._rect.top >= t._rect.bottom and a.rect.top < t.rect.bottom):
			a.onBottomLineContact(t)

	# ------------ #
	#  Lava Block  #
	# ------------ #
	## This is code for a lava block which spells instant-retry for Dave
	def lava_block(g, t, a):
		if base.SOUND:
			base.sound.Play("steam")
			base.sound.Play("yeow")
		g.daveInTrouble(-1);
	

	# --------------------- #
	#  Tile Collision Data  #
	# --------------------- #
	## Here we initialize the tile data.  The columns are (groups,function,config)

	tdata = {
		# Slopes		
		0+1*10:('player,genemy,colspr',tile_block,{'top':0,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':1, 'can_climb':0}),
		3+1*10:('player,genemy,colspr',tile_block,{'top':0,'bottom':1,'left':1,'right':1,'slope_r':1, 'slope_l':0, 'can_climb':0}),

		# Solid rock & partial floors
		0+2*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		1+2*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		2+2*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		3+2*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),

		# Solid rock
		1+4*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		2+4*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		1+5*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		2+5*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),

		# Ladder pieces
		4+2*10:('player,genemy,colspr',tile_block,{'top':0,'bottom':0,'left':0,'right':0,'slope_r':0, 'slope_l':0, 'can_climb':1}),
		4+3*10:('player,genemy,colspr',tile_block,{'top':0,'bottom':0,'left':0,'right':0,'slope_r':0, 'slope_l':0, 'can_climb':1}),
		4+4*10:('player,genemy,colspr',tile_block,{'top':0,'bottom':0,'left':0,'right':0,'slope_r':0, 'slope_l':0, 'can_climb':1}),

		# Floor pieces
		0+7*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		1+7*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		2+7*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		3+7*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':1,'right':0,'slope_r':0, 'slope_l':0, 'can_climb':0}),

		# Mid-lava platform
		4+8*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0,'slope_r':0, 'slope_l':0, 'can_climb':0}),

		# Lava rock
		5+8*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		6+8*10:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),

		# Lava
		0+8*10:('player,genemy,colspr',lava_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		1+8*10:('player,genemy,colspr',lava_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		2+8*10:('player,genemy,colspr',lava_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		3+8*10:('player,genemy,colspr',lava_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		0+9*10:('player,genemy,colspr',lava_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		1+9*10:('player,genemy,colspr',lava_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		2+9*10:('player,genemy,colspr',lava_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		3+9*10:('player,genemy,colspr',lava_block,{'top':1,'bottom':1,'left':1,'right':1,'slope_r':0, 'slope_l':0, 'can_climb':0}),
		
	}

	# ---------------- #
	#  Tile Animation  #
	# ---------------- #
    ## This function swaps specific tiles in the background so that they are animated.
	def animate_background(self):
		if ((self.frame % 16) == 0): ## Every 5th game frame (at 25 FPS)
			tmp = self.tiles[80]
			self.tiles[80] = self.tiles[81]
			self.tiles[81] = self.tiles[82]
			self.tiles[82] = self.tiles[83]
			self.tiles[83] = tmp

			tmp = self.tiles[90]
			self.tiles[90] = self.tiles[91]
			self.tiles[91] = self.tiles[92]
			self.tiles[92] = self.tiles[93]
			self.tiles[93] = tmp
