
from player import *
#import colsprs

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
			# a.rect.right = t.rect.left
			# a.dx /= 1.5
			# a.dx = -a.dx
			
		if (c['right'] == 1 and a._rect.left >= t._rect.right and a.rect.left < t.rect.right):
			a.onRightLineContact(t)

		if (c['bottom'] == 1 and a._rect.top >= t._rect.bottom and a.rect.top < t.rect.bottom):
			a.onBottomLineContact(t)
				
	# --------------------- #
	#  Tile Collision Data  #
	# --------------------- #
	## Here we initialize the tile data.  The columns are (groups,function,config)

	tdata = {
		2+0*8:('player,genemy,colspr',tile_block,{'top':0,'bottom':0,'left':0,'right':0, 'can_climb':1}),

		0+1*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		1+1*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		2+1*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		3+1*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),

		5+1*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		6+1*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		
		0+2*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		1+2*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		
		5+2*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':1}),

		0+3*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		1+3*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		2+3*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':1}),
		3+3*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':1}),
		5+3*8:('player,genemy,colspr',tile_block,{'top':0,'bottom':0,'left':0,'right':0, 'can_climb':1}),
		
		0+4*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		1+4*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		2+4*8:('player,genemy,colspr',tile_block,{'top':0,'bottom':0,'left':0,'right':0, 'can_climb':1}),
		3+4*8:('player,genemy,colspr',tile_block,{'top':0,'bottom':0,'left':0,'right':0, 'can_climb':1}),

		5+4*8:('player,genemy,colspr',tile_block,{'top':0,'bottom':0,'left':0,'right':0, 'can_climb':1}),

		2+5*8:('player,genemy,colspr',tile_block,{'top':0,'bottom':0,'left':0,'right':0, 'can_climb':1}),

		0+6*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		1+6*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		2+6*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		3+6*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		4+6*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		5+6*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		6+6*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':1}),
		7+6*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':1}),

		# Sun block
		4+8*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		5+8*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		4+9*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		5+9*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),

		# Block w/ vine attachment
		7+9*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
	}

	
	# ---------------- #
	#  Tile Animation  #
	# ---------------- #
    ## This function swaps specific tiles in the background so that they are animated.
	def animate_background(self):
		if ((self.frame % 5) == 0): ## Every 5th game frame (at 25 FPS)
			tmp = self.tiles[23]
			self.tiles[23] = self.tiles[7]
			self.tiles[7] = tmp

			tmp = self.tiles[31]
			self.tiles[31] = self.tiles[15]
			self.tiles[15] = tmp;

			tmp = self.tiles[22]
			self.tiles[22] = self.tiles[30]
			self.tiles[30] = tmp

			tmp = self.tiles[64]
			self.tiles[64] = self.tiles[72]
			self.tiles[72] = tmp

			tmp = self.tiles[65]
			self.tiles[65] = self.tiles[73]
			self.tiles[73] = tmp

			tmp = self.tiles[66]
			self.tiles[66] = self.tiles[74]
			self.tiles[74] = tmp

			tmp = self.tiles[67]
			self.tiles[67] = self.tiles[75]
			self.tiles[75] = tmp

