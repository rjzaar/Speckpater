
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
				
	# --------------------- #
	#  Tile Collision Data  #
	# --------------------- #
	## Here we initialize the tile data.  The columns are (groups,function,config)

	tdata = {
		0+1*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		1+1*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		0+2*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		1+2*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		0+3*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		1+3*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		0+4*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		1+4*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
				
		# sun block
		2+1*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		3+1*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		2+2*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
		3+2*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':1,'left':1,'right':1, 'can_climb':0}),
	
		2+3*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		3+3*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		4+3*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		5+3*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		
		2+4*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		3+4*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		4+4*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		5+4*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
		6+4*8:('player,genemy,colspr',tile_block,{'top':1,'bottom':0,'left':0,'right':0, 'can_climb':0}),
	}

	
	# ---------------- #
	#  Tile Animation  #
	# ---------------- #
    ## This function swaps specific tiles in the background so that they are animated.
	def animate_background(self):
		pass

