#!/usr/bin/python
"""a simple level editor for pygame

interface:
- menus for common commands
- toolbox
- tile edit area
	left click to use current tool
	right click to select a tile
	middle drag to move around the level
- tile select area
	left click to select a tile in tile mode
	right click to select a tile in background mode
- code select area
	left click to select a code

keys:
l - load
s - save
p - play

a - select all
z - undo
c - copy selection to clipboard
v - paste clipboard at selection origin
delete - delete selection
f - fill selection

arrows - change tile
shift+arrows - scroll screen by 1/8 screen size jumps
ctrl+arrows - scroll screen by full screen size jumps
return - toggle fullscreen
"""

import os,sys	
from optparse import OptionParser
from ConfigParser import ConfigParser
import base
import pygame
from pygame.locals import *
import glob

import levelfile

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui, html, tilevid


class _app(gui.Container):
	
    def loadSets(self):
        self.tiles = pygame.image.load(os.path.join('levels/tilesets',self.tname + ".png"))
        self.tiles_w, self.tiles_h = (self.tiles.get_width(), self.tiles.get_height())
        self.level.tga_load_tiles(self.tiles,(self.tile_w,self.tile_h))

        self.codes = pygame.image.load(os.path.join('levels', self.cname + '.png'))
        self.codes_w, self.codes_h = (self.codes.get_width(), self.codes.get_height())
				
        tmp = self.level.tiles
        self.level.tiles = [None for i in xrange(0,256)]
        self.level.tga_load_tiles(self.codes,(self.tile_w,self.tile_h))
        self.level.codes = self.level.tiles
        self.level.tiles = tmp
				
    def initLevel(self,width,height,tname, cname, bgname):
        self.fname = None
        self.tname = tname
        self.cname = cname
        self.bgname = bgname
				
        self.loadSets()
		
        self.level_w, self.level_h = width, height
        self.level.resize((width,height),1)
				
        self.dirty = 0
        self.requiresSave = 1

    def loadLevel(self,levelFilename):
			
			  ## store for reload
        self.levelFilename = levelFilename
			
        lfn = levelFilename
        self.fname, self.tname, self.cname,bg = fname,tiles,codes,self.bgname = levelfile.loadLevelFile(lfn)

        print "loading level",levelFilename,"geometry:",self.fname,"tileset:",self.tname,"triggers:",self.cname
				
        self.loadSets()
		
        self.level.tga_load_level(os.path.join('levels', self.fname + '.tga'),1)
        self.level_w, self.level_h = len(self.level.tlayer[0]),len(self.level.tlayer)

        self.dirty = 0
        self.requiresSave = 0
				
    def __init__(self, data):
        gui.Container.__init__(self)
        self.screen, lfname = data

        #Change later
        self.screen_w = base.SCREEN_WIDTH
        self.screen_h = base.SCREEN_HEIGHT
        self.tile_w = self.tile_h = base.TILE_SIZE

        self.level = tilevid.Tilevid()
				
        self.tiles_w, self.tiles_h = 0,0
        self.requiresSave = 0
				
        self.loadLevel(lfname)

        self.tile = 0
        self.code = 0
        
        self.mode = 'tile'
        self.modenum = 0
        self.clipboard = None
        self.history = []
        
        self.changes = []
        self.dirty = 0
            
    def mod(self,rect):
        self.dirty = 1
        self.changes.append((pygame.Rect(rect),self.copy(rect)))

    def view_init(self,dw,dh):
        self.view_w = dw #/ self.tile_w
        self.view_h = dh #/ self.tile_h

        self.select = Rect(0,0,self.level.size[0],self.level.size[1])
            
    def fill(self,rect,v):
        lvl = self.level
        w,h = lvl.size
        
        for layer,n in [ (lvl.tlayer,0), (lvl.blayer,1), (lvl.clayer,2) ]:
            for y in range(0,rect.h):
                for x in range(0,rect.w):
                    tx,ty = x+rect.x,y+rect.y
                    if tx >= 0 and tx < w and ty >= 0 and ty < h: layer[ty][tx] = v[n]
            
    def copy(self,rect):
        data = [[[None for x in range(0,rect.w)] for y in range(0,rect.h)] for l in range(0,4)] 

        lvl = self.level
        w,h = lvl.size
        
        for layer,n in [ (lvl.tlayer,0), (lvl.blayer,1), (lvl.clayer,2) ]:
            for y in range(0,rect.h):
                for x in range(0,rect.w):
                    tx,ty = x+rect.x,y+rect.y
                    if tx >= 0 and tx < w and ty >= 0 and ty < h: data[n][y][x] = layer[ty][tx]
        return data
                            
    def paste(self,rect,data):
        lvl = self.level
        w,h = lvl.size
        
        for layer,n in [ (lvl.tlayer,0), (lvl.blayer,1), (lvl.clayer,2) ]:
            for y in range(0,rect.h):
                for x in range(0,rect.w):
                    tx,ty = x+rect.x,y+rect.y
                    v = data[n][y][x]
                    if v != None and tx >= 0 and tx < w and ty >= 0 and ty < h: layer[ty][tx] = v

    def archive(self):
        if not len(self.changes): return
        
        self.dirty = 1
        h = self.history
        if len(h) >= 32:
            del h[0]
        
        lvl = self.level
        
        h.append(self.changes)
        self.changes = []
            
    def undo(self):
        if len(self.changes): self.archive()
                
        if len(self.history) == 0: return
        
        self.dirty = 1
        changes = self.history.pop()
        
        changes.reverse()
        for rect,data in changes:
            self.paste(rect,data)
                
        self.vdraw.repaint()
        self.tpicker.repaint() #huh?
        
        self.changes = []
        return
        
        self.level.fill((0,0,0,0),(off[0],off[1],self.view_w,self.view_h))
        self.level.blit(c,off)
        self.vdraw.repaint()
        self.tpicker.repaint()
            
    def __setattr__(self,k,v):
        self.__dict__[k] = v
        
        if k == 'view':
            if hasattr(self,'vdraw'): self.vdraw.repaint()
        
        if k == 'tile':
            if hasattr(self,'tpicker'): self.tpicker.repaint()
                        
        if k == 'code':
            if hasattr(self,'cpicker'): self.cpicker.repaint()

    def event(self,e):
        if e.type is KEYDOWN:
            for key,cmd,value in keys:
                if e.key == key:
                    cmd(value)
                    return
        return gui.Container.event(self,e)

class tpicker(gui.Widget):
    def __init__(self):
        gui.Widget.__init__(self)
        self.style.width = app.tiles_w
        self.style.height = app.tiles_h
            
    def paint(self,s):
        s.fill((128,128,128))
        s.blit(app.tiles,(0,0))
        if (app.mode in ('tile', 'bkgr')):
            if (app.mode == 'tile'): color = (0,0,255)
            else: color = (255,0,255)
            w = app.tiles_w/app.tile_w
            x,y = app.tile%w,app.tile/w
            off = x*app.tile_w,y*app.tile_h
            pygame.draw.rect(s,color,(off[0],off[1],app.tile_w,app.tile_h),2)
        pygame.draw.lines(s,(0,0,0),1,[(0,0),(0,self.style.height-1),(self.style.width-1,self.style.height-1),(self.style.width-1,0)],1)
            
    def event(self,e):
        if (e.type is MOUSEBUTTONDOWN and e.button == 1) or (e.type is MOUSEMOTION and e.buttons[0] and self.container.myfocus == self):
            w = app.tiles_w/app.tile_w
            x,y = e.pos[0]/app.tile_w,e.pos[1]/app.tile_h
            n = x+y*w
            self.set(n)
            cmd_mode('tile')
        elif (e.type is MOUSEBUTTONDOWN and e.button == 3) or (e.type is MOUSEMOTION and e.buttons[2] and self.container.myfocus == self):
            w = app.tiles_w/app.tile_w
            x,y = e.pos[0]/app.tile_w,e.pos[1]/app.tile_h
            n = x+y*w
            self.set(n)
            cmd_mode('bkgr')
	
    def set(self,n):
        if n < 0 or n >= len(app.level.tiles) or app.level.tiles[n] == None: return
        app.tile = n


class cpicker(gui.Widget):
    def __init__(self):
        gui.Widget.__init__(self)
        self.style.width = app.codes_w
        self.style.height = app.codes_h
            
    def paint(self,s):
        s.fill((128,128,128))
        s.blit(app.codes,(0,0))
        if (app.mode == 'code'):
            w = app.codes_w/app.tile_w
            x,y = app.code%w,app.code/w
            off = x*app.tile_w,y*app.tile_h
            pygame.draw.rect(s,(0,0,255),(off[0],off[1],app.tile_w,app.tile_h),2)
        pygame.draw.lines(s,(0,0,0),1,[(0,0),(0,self.style.height-1),(self.style.width-1,self.style.height-1),(self.style.width-1,0)],1)
            
    def event(self,e):
        if (e.type is MOUSEBUTTONDOWN and e.button == 1) or (e.type is MOUSEMOTION and e.buttons[0] == 1 and self.container.myfocus == self):
            w = app.codes_w/app.tile_w
            x,y = e.pos[0]/app.tile_w,e.pos[1]/app.tile_h
            n = x+y*w
            self.set(n)
            cmd_mode('code')
    
    def set(self,n):
        if n < 0 or n >= len(app.level.codes) or app.level.codes[n] == None: return
        app.code = n		

class vdraw(gui.Widget):            
    def __init__(self,**params):
        gui.Widget.__init__(self,**params)
        self.rect.w,self.rect.h = self.style.width,self.style.height
        self.scroll = 0
        
        s = pygame.Surface((self.rect.w,self.rect.h))
        clrs = [(148,148,148),(108,108,108)]
        inc = 7
        for y in range(0,self.rect.w/inc):
            for x in range(0,self.rect.h/inc):
                s.fill(clrs[(x+y)%2],(x*inc,y*inc,inc,inc))
        self.bg = s

        s = pygame.Surface((self.rect.w,self.rect.h)).convert_alpha()
        s.fill((0,0,0,0))
        for x in range(0,app.view_w):
            pygame.draw.line(s,(0,0,0),(self.rect.w*x/app.view_w,0),(self.rect.w*x/app.view_w,self.rect.h))
        for y in range(0,app.view_h):
            pygame.draw.line(s,(0,0,0),(0,self.rect.h*y/app.view_h),(self.rect.w,self.rect.h*y/app.view_h))
        self.grid = s
        
        self.pos = 0,0
				
        self.font = self.style.font

            
    def paint(self,s):
        s.fill((128,128,128))

        #make sure to clamp the bounds
        if app.level.bounds != None:
            app.level.view.clamp_ip(app.level.bounds)
        
        #draw border		
        rect = pygame.Rect(0,0,app.level.size[0],app.level.size[1])
        tcorners = [rect.topleft,rect.topright,rect.bottomright,rect.bottomleft]
        corners = [app.level.tile_to_screen(tcorners[n]) for n in range(0,4)]
        pygame.draw.lines(s,(255,255,0),1,corners,2)

        app.level.paint(s)
        
        tmp_tiles = app.level.tiles
        tmp_tlayer = app.level.tlayer
        tmp_blayer = app.level.blayer
        
        app.level.tiles = app.level.codes
        app.level.tlayer = app.level.clayer
        app.level.blayer = None
        
        app.level.paint(s)
        
        app.level.tiles = tmp_tiles
        app.level.tlayer = tmp_tlayer
        app.level.blayer = tmp_blayer

        rect = pygame.Rect(app.select.x,app.select.y,app.select.w,app.select.h)
        tcorners = [rect.topleft,rect.topright,rect.bottomright,rect.bottomleft]
        corners = [app.level.tile_to_screen(tcorners[n]) for n in range(0,4)]
        pygame.draw.lines(s,(255,255,255),1,corners,2)

        if (self.scroll == 0):
            rect = pygame.Rect(self.pos[0],self.pos[1],1,1)
            tcorners = [rect.topleft,rect.topright,rect.bottomright,rect.bottomleft]
            corners = [app.level.tile_to_screen(tcorners[n]) for n in range(0,4)]
            pygame.draw.lines(s,(196,196,196),1,corners,2)

        pygame.draw.lines(s,(0,0,0),1,[(0,0),(0,self.rect.h-1),(self.rect.w-1,self.rect.h-1),(self.rect.w-1,0)],1)
        
								
    def event(self,e):
        if e.type is MOUSEMOTION:
            self.getpos(e)
            print self.pos," - ",self.pos[0] * base.TILE_SIZE,self.pos[1] * base.TILE_SIZE
        if (e.type is MOUSEBUTTONDOWN and e.button == 2) or (e.type is MOUSEMOTION and e.buttons[1]==1 and self.container.myfocus == self):
            self.picker_down(e)
        if e.type is MOUSEBUTTONDOWN and e.button == 1:
            self.getpos(e)
            a = '%s_down'%app.mode
            if hasattr(self,a): getattr(self,a)(e)
        if e.type is MOUSEMOTION and e.buttons[0] and self.container.myfocus == self:
            a = '%s_drag'%app.mode
            if hasattr(self,a): getattr(self,a)(e)
        if e.type is MOUSEBUTTONUP and e.button == 1:
            a = '%s_up'%app.mode
            if hasattr(self,a): getattr(self,a)(e)
        if e.type is MOUSEBUTTONDOWN and e.button == 3:
            self.move_down(e)
            self.scroll = 1
        if e.type is MOUSEBUTTONUP and e.button == 3:
            self.scroll = 0
        if e.type is MOUSEMOTION and e.buttons[2] and self.container.myfocus == self:
            self.move_drag(e)
    
    #move
    def move_down(self,e):
        self.moff = app.level.view.x,app.level.view.y
        self.m1 = e.pos
            
    def move_drag(self,e):
        m1 = self.m1
        m2 = e.pos
        #app.view = app.level.subsurface((x,y,app.view_w,app.view_h))
        app.level.view.x,app.level.view.y = self.moff[0] + m1[0]-m2[0], self.moff[1]+m1[1]-m2[1]
        self.repaint()
                    
    #picker
    def picker_down(self,e):
        pos = self.getpos(e)
        if pos == None: return 
        tx,ty = pos
        
        if app.mode == 'tile':
            app.tile = app.level.tlayer[ty][tx]
        if app.mode == 'bkgr':
            app.tile = app.level.blayer[ty][tx]
        app.code = app.level.clayer[ty][tx]

    #tile
    def tile_down(self,e):
        app.archive()
        self.tile_drag(e)
    
    def tile_drag(self,e):
        pos = self.getpos(e)
        #r,g,b,a = app.view.get_at(pos)
        #r = app.tile
        #app.view.set_at(pos,(r,g,b))
        
        if pos == None: return
        tx,ty = pos
        app.mod(pygame.Rect(tx,ty,1,1))
        app.level.tlayer[ty][tx] = app.tile
        self.repaint()
            
    #bkgr
    def bkgr_down(self,e):
        app.archive()
        self.bkgr_drag(e)
    
    def bkgr_drag(self,e):
        pos = self.getpos(e)
        #r,g,b,a = app.view.get_at(pos)
        #g = app.tile
        #app.view.set_at(pos,(r,g,b))
        if pos == None: return
        tx,ty = pos
        app.mod(pygame.Rect(tx,ty,1,1))
        app.level.blayer[ty][tx] = app.tile
        self.repaint()

    #code
    def code_down(self,e):
        app.archive()
        self.code_drag(e)

    def code_drag(self,e):
        pos = self.getpos(e)
        #r,g,b,a = app.view.get_at(pos)
        #b = app.code
        #app.view.set_at(pos,(r,g,b))
        if pos == None: return
        tx,ty =  pos
        app.mod(pygame.Rect(tx,ty,1,1))
        app.level.clayer[ty][tx] = app.code
        self.repaint()
            
    #eraser
    def eraser_down(self,e):
        app.archive()
        self.eraser_drag(e)
    
    def eraser_drag(self,e):
        pos = self.getpos(e)
        if pos == None: return
        tx,ty = pos
        app.mod(pygame.Rect(tx,ty,1,1))
        app.level.tlayer[ty][tx] = 0
        app.level.blayer[ty][tx] = 0
        app.level.clayer[ty][tx] = 0
        #app.view.set_at(pos,(0,0,0))
        self.repaint()
            
    def getpos(self,e):
        tx,ty = app.level.screen_to_tile(e.pos)
        
        if tx < 0 or ty < 0 or tx >= app.level.size[0] or ty >= app.level.size[1]: return None
        
        if (tx,ty) != self.pos:
            self.pos = tx,ty
            self.repaint()
        return tx,ty
        
        x,y = e.pos[0]/app.tile_w,e.pos[1]/app.tile_h
        x = min(max(0,x),app.view_w-1)
        y = min(max(0,y),app.view_h-1)
        return x,y
    
    def getpos2(self,e):
        tx,ty = app.level.screen_to_tile(e.pos)
        
        return tx+1,ty+1
        
        w = app.tile_w
        h = app.tile_h
        x,y = (e.pos[0]+w/2)/w,(e.pos[1]+h/2)/h
        x = min(max(0,x),app.view_w)
        y = min(max(0,y),app.view_h)
        return x,y
    
    #select
    def select_down(self,e):
        pos = self.getpos2(e)
        pos = pos[0]-1,pos[1]-1
        app.select = Rect(pos[0],pos[1],1,1)
        self.repaint()
            
    def select_drag(self,e):
        pos = self.getpos2(e)
        app.select = Rect(app.select.x,app.select.y,pos[0]-app.select.x,pos[1]-app.select.y)
        app.select.w = max(1,app.select.w)
        app.select.h = max(1,app.select.h)

        self.repaint()
		

def cmd_all(value):
	app.select = Rect(0,0,app.level.size[0],app.level.size[1])
	app.vdraw.repaint()

def cmd_undo(value):
	app.undo()
	
def cmd_redo(value):
	pass
	
def cmd_copy(value):
        data = app.copy(app.select)
	app.clipboard = pygame.Rect(app.select),data
	return
	
	print app.clipboard.get_at((0,0))
	
def cmd_paste(value):
	if app.clipboard != None:
		app.archive()
		
		rect,data = app.clipboard
		rect = pygame.Rect(app.select.x,app.select.y,rect.w,rect.h)
		
		app.mod(rect)
		app.paste(rect,data)
		app.vdraw.repaint()

class Restart(Exception):
	pass
	
def _dirty(fnc,v):
	dialog = DirtyDialog()
	def onchange(value):
		value.close()
		return fnc(v)
	dialog.connect(gui.CHANGE,onchange,dialog)
	dialog.open()

	
	
class NewDialog(gui.Dialog):
	def __init__(self,**params):
		title = gui.Label("New...")
		
		import levels
		
		tilesetopts = ""
		tsn = levels.tilesets.__all__
		for set in tsn:
			tilesetopts += "<option value='" + set + "'>" + set
		
		doc = html.HTML(globals={'gui':gui,'dialog':self},data="""
<form id='form'>

<table>

<tr><td colspan=2>

<table>
<tr><td >Name: <td><input type='text' size=20 name='lname' value=''>
<tr><td>Tileset: <td> <select name="tiles" value='commontiles'>
""" + tilesetopts + """
</select>

<tr><td>Background: <td><input type='text' size=20 name='bgname' value='junglebg'>
</table>

<tr>
<td align=center>Level Size

<tr><td colspan='1' align='center' style='padding-right:8px;'>

<table>
<tr><td align=right>Width: <td><input type='text' size='4' value='120' name='width'>
<tr><td align=right>Height: <td><input type='text' size='4' value='30' name='height'>
</table>

<td colspan='1' align='center'>

<tr><td>&nbsp;

<tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE)'> <input type='button' value='Cancel' onclick='dialog.close()'>

</table>""")

		gui.Dialog.__init__(self,title,doc)

		self.value = doc['form']	
	
	
	
def cmd_new(value):
	if app.dirty: _dirty(_cmd_new,value)
	else: _cmd_new(value)

def _cmd_new(value):
	dialog = NewDialog()
	
	def onchange(value):
		value.close()
		vv = value.value
		ok = 0
		try:		
			# , vv['codes'].value
			codes = "triggers"
			width,height = int(vv['width'].value), int(vv['height'].value)
			tiles,fname,bg = vv['tiles'].value, vv['lname'].value, vv['bgname'].value

			app.initLevel(width,height,tiles,codes,bg)
			# use same name for both .tga and .lev
			app.fname = fname
			app.levelFilename = fname 
			app.dirty = 1
			app.requiresSave = 1
			ok = 1
		except Exception, v:
			ErrorDialog("New failed.",v).open()
		#if ok:
			#raise Restart()
	
	dialog.connect(gui.CHANGE,onchange,dialog)
	dialog.open()
	
	

def cmd_load(value):
	if app.dirty: _dirty(_cmd_load,value)
	else: _cmd_load(value)

def _cmd_load(value):
	dialog = LoadDialog()
	
	def onchange(value):
		value.close()
		vv = value.value
		ok = 0
		try:		
			#codes,tiles,fname = vv['codes'].value, vv['tiles'].value, vv['lname'].value
			
			app.loadLevel(vv['fname'].value)
			
			app.dirty = 0
			app.requiresSave = 0
			ok = 1
		except Exception, v:
			ErrorDialog("Load failed.",v).open()
		#if ok:
			#raise Restart()
	
	dialog.connect(gui.CHANGE,onchange,dialog)
	dialog.open()
	
	
class LoadDialog(gui.Dialog):
	def __init__(self,**params):
		title = gui.Label("Load...")
		
		options = ""
		
		files = glob.glob(os.path.join('levels', '*.lev'))
		limit = 10
		for file in files:
			limit = limit - 1
			if limit < 0: break
			fn = os.path.basename(file)
			n = os.path.splitext(fn)[0]
			options += "<option value='" + n + "'>" + fn
		
		doc = html.HTML(globals={'gui':gui,'dialog':self},data="""
<form id='form'>

<table width="200" height="70">


<tr>

<td>Level file: <td> <select name="fname">
""" + options + """
</select>


<tr>

<tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE)'> <input type='button' value='Cancel' onclick='dialog.close()'>

</table>""")

		gui.Dialog.__init__(self,title,doc)

		self.value = doc['form']	
	
	
#def _cmd_new(value):
#	try:
#		exec("from levels import testlevel")
#		eval("testlevel.GameLevel(screen)")
#	except ImportError, err:
#		raise base.ResourceException("Cannot load testlevel script")
		
def cmd_cut(value):
	cmd_copy(value)
	cmd_delete(value)

def cmd_fullscreen(value):
	pygame.display.toggle_fullscreen()
	
def cmd_delete(value):
	app.archive()
	app.mod(app.select)
	app.fill(app.select,(0,0,0,0))
	app.vdraw.repaint()

def cmd_fill(value):
	pass

def cmd_pick(value):
	dx,dy = value
	
	mods = pygame.key.get_mods()

	if (mods&KMOD_SHIFT) != 0:
		app.level.view.x += dx*app.vdraw.rect.w/8
		app.level.view.y += dy*app.vdraw.rect.h/8
		app.vdraw.repaint()
	elif (mods&KMOD_CTRL) != 0:
		app.level.view.x += dx*app.vdraw.rect.w
		app.level.view.y += dy*app.vdraw.rect.h
		app.vdraw.repaint()	
	else:
		w = app.tiles_w/app.tile_w
		if app.mode == 'code':
			n = app.code + dx + dy*w
			app.cpicker.set(n)
		else:
			n = app.tile + dx + dy*w
			app.tpicker.set(n)
		
def cmd_mode(value):
        if (value == None):
            app.modenum += 1
            if(app.modenum > 4): app.modenum = 0
            num, value = tools[app.modenum]
	app.mode = value
	app.vdraw.repaint()
	app.tpicker.repaint()
	app.cpicker.repaint()

def cmd_reload(value):
	if app.dirty: _dirty(_cmd_reload,value)
	else: _cmd_reload(value)

def _cmd_reload(value):
	if app.fname == None:
		ErrorDialog("Load failed","Image is untitled.").open()
		return
	if app.requiresSave == 1:
		ErrorDialog("Cannot load","Current file is not saved.").open()
		return
		
		# this is actually a reload
	app.loadLevel(app.levelFilename)
				
	#raise Restart()
	
def cmd_save(value):
	try:
		if app.levelFilename == None:
			raise Exception("no .lev filename")
		if app.fname == None:
			raise Exception("no .tga filename")

		app.level.tga_save_level(os.path.join('levels', app.fname + '.tga'))
		levelfile.saveLevelFile(app.levelFilename,(app.fname,app.tname,app.cname,app.bgname))
		app.dirty = 0
		app.requiresSave = 0
	except Exception, v:
		ErrorDialog("Save failed.",v).open()
		return
	
#import os
def cmd_play(value):
	if app.dirty: _dirty(_cmd_play,value)
	else: _cmd_play(value)

def _cmd_play(value):
	app.top.quit()
	
def cmd_changeLevel(value):
	print "not implemented"
	#SelectLevelDialog().open()

	
def cmd_resetLevel(value):
	print "not implemented"

tools = [
	(0,'tile'),
	(1,'bkgr'),
	(2,'code'),
	(3,'select'),
	(4,'eraser'),
	]
	
menus = [
	('File/New',cmd_new,None),
	('File/Save',cmd_save,None),
	('File/Load',cmd_load,None),
	('File/Reload',cmd_reload,None),
	('File/Play',cmd_play,None),
	
	('Edit/Undo',cmd_undo,None),
	('Edit/Cut',cmd_cut,None),
	('Edit/Copy',cmd_copy,None),
	('Edit/Paste',cmd_paste,None),
	('Edit/Delete',cmd_delete,None),
	('Edit/Select All',cmd_all,None),

        ('Mode/Select',cmd_mode,'select'),
        ('Mode/Erase',cmd_mode,'eraser'),
	]

keys =[
	(K_s,cmd_save,None),
	(K_d,cmd_load,None),
	(K_p,cmd_play,None),

	(K_a,cmd_all,None),
	(K_z,cmd_undo,None),
	(K_x,cmd_cut,None),
	(K_c,cmd_copy,None),
	(K_v,cmd_paste,None),
	(K_DELETE,cmd_delete,None),
	
	(K_F10,cmd_fullscreen,None),
        (K_F11,cmd_play,None),
	
	(K_UP,cmd_pick,(0,-1)),
	(K_DOWN,cmd_pick,(0,1)),
	(K_LEFT,cmd_pick,(-1,0)),
	(K_RIGHT,cmd_pick,(1,0)),
	]

class ErrorDialog(gui.Dialog):
	def __init__(self,tt,data,**params):
		title = gui.Label("Error: "+tt)
		data = str(data)
		
		doc = html.HTML(globals={'gui':gui,'dialog':self},data="""
<form id='form'>

<table>
<tr><td><h1>&lt;!&gt;&nbsp;</h1>
<td>"""+data+"""
<tr><td>&nbsp;
<tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE);dialog.close()'>
</table>""")
		gui.Dialog.__init__(self,title,doc)
		self.value = doc['form']

class DirtyDialog(gui.Dialog):
	def __init__(self,**params):
		title = gui.Label("File not yet saved...")
		data = "Your file is not yet saved.<br>Are you sure you want to continue?"
		
		doc = html.HTML(globals={'gui':gui,'dialog':self},data="""
<form id='form'>

<table>
<tr><td><h1>&nbsp;<b>!<b>&nbsp;</h1>
<td>"""+data+"""
<tr><td>&nbsp;
<tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE)'> <input type='button' value='Cancel' onclick='dialog.close()'>
</table>""")
		gui.Dialog.__init__(self,title,doc)
		self.value = doc['form']

def init_app(data):
	global app
	app = _app(data)
	
	#
	ss = 8
		
	#--- top
	x,y,h = 0,0,0
		
	#menus
	e = gui.Menus(menus)
	e.rect.w,e.rect.h = e.resize()
	app.add(e,x,y)
	menus_height = e.rect.h
	h = max(h,menus_height)
		
	#--- row
	x,y,h = ss,y+h+ss,0

	#vdraw
	dw = app.screen_w - (app.tiles_w+ss*4)
	dh = app.screen_h - (menus_height+ss*2)
	app.view_init(dw,dh)
	
	e = app.vdraw = vdraw(width=app.view_w, height=app.view_h)
	e.rect.w,e.rect.h = e.resize()
	app.add(e,x,y)
	x,h = x+e.rect.w,max(h,e.rect.h)
	
	#--- hspace
	x += ss
	
	#tpicker
	e = app.tpicker = tpicker()
	e.rect.w,e.rect.h = e.resize()
	#--- right
	x = app.screen_w-e.rect.w-ss
	app.add(e,x,y)
	x,h = x+e.rect.w,max(h,e.rect.h)
	tpicker_height = e.rect.h
	
	#cpicker
	e = app.cpicker = cpicker()
	e.rect.w,e.rect.h = e.resize()
	#--- right
	x = app.screen_w-e.rect.w-ss
	app.add(e,x,y+tpicker_height+ss)
	x,h = x+e.rect.w,max(h,e.rect.h)
	
	pygame.key.set_repeat(500,30)
	
	app.screen.fill((255,255,255,255))


def run():
	top = gui.Desktop()
	top.connect(gui.QUIT,cmd_play,None)
	top.init(app,app.screen)
	app.top=top
	top.run()

										
def loadEditor(level, cname):
	data = (level.screen, level.levelFileName)
	init_app(data)
	
	restart = 1
	while restart:
			restart = 0
			try:
					run()
			except Restart: restart = 1
			
				# return the current file names used in editor		
	if app.requiresSave == 1:
		return level.levelFilename

	return app.levelFilename

# vim: set filetype=python sts=4 sw=4 noet si :
