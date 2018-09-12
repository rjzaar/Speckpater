import os
import base
import pygame
import math
import music
import levelfile
import basegamelevel
import menu

from pygame.locals import *
from pgu import engine
from pgu import timer
from base import saveGame
from base import loadGame
from sound import DaveSound
from base import initLevel, initCustomLevel
from base import testLevelname

	
class Game(engine.State):		
	def __init__(self, main):
		self.main = main
		self.data = base.DATA
		self.data['level'] = base.getSaveGameVar(self.data,'level',1)
		base.gameDifficulty = base.getSaveGameVar(self.data,'difficulty',base.saveGameKeys['difficulty'])
		base.num_bibles = base.getSaveGameVar(self.data,'bibles',0)
		self.data['chapter'] = base.getSaveGameVar(self.data,'chapter',1)
		base.numBananas = base.getSaveGameVar(self.data,'bananas',0)
		base.NEED_MORE_BIBLES = self.data['need_more_bibles']
		
		self.orig_num_bibles = base.num_bibles
		self.orig_num_bananas = base.numBananas
		
		if base.gameDifficulty == 2:
			base.NEEDED_BIBLES = 85
		elif base.gameDifficulty == 3:
			base.NEEDED_BIBLES = 115
		
		if not 'fallLesson' in self.main.gameVariables:
			print "loading the fallLesson variable"
			self.main.gameVariables['fallLesson'] = base.getSaveGameVar(self.data,'fallLesson',False)
			self.main.gameVariables['firstbanana'] = base.getSaveGameVar(self.data,'firstbanana',False)
			
		self.playing = None
##		pygame.mixer.music.load(os.path.join("data","bgmusic2.ogg"))
##		pygame.mixer.music.play(-1)

	def init(self):
		if base.Testing:
			pygame.mouse.set_visible(True)
		else:
			pygame.mouse.set_visible(False)
		
	def loop(self):
		gameVariables = self.main.gameVariables
		levelName = ""
		currentLevel = None
		running = True
		
		while running:
				
			while currentLevel == None:
				levelName = "gamelevel" + str(self.data['chapter']) + "_" + str(self.data['level'])
		
				try:
					if base.num_bibles >= base.NEEDED_BIBLES:
						if base.NEED_MORE_BIBLES == True:
							base.NEED_MORE_BIBLES = False
							levelName = "gamelevel" + str(6) + "_" + str(1)
							
					
					## Load the new level from the dynamically loaded module
					currentLevel = initLevel(levelName)
					# save all the variables level and other scripts might have created in gameVariables
					for key,value in gameVariables.iteritems():
						self.data[key] = value
					saveGame(self.data)
														
				except ImportError, err:
					# if we weren't looking for the first level of current major 
					# number (x_0), then check for next major
					if self.data['level'] > 1:
						self.data['chapter'] += 1
						self.data['level'] = 1
					else:
						raise base.ResourceException("Error loading level " + levelName + "!")
				
				if base.SOUND == True:
					if self.data["chapter"] == 5:
						if self.playing != "MountainMusic":
							for item in music.Music:
								music.Stop(item)
							music.Play("MountainMusic")
							self.playing = "MountainMusic"
					
					if self.data["chapter"] == 4:
						if self.playing != "TempleMusic":
							for item in music.Music:
								music.Stop(item)
							music.Play("TempleMusic")
							self.playing = "TempleMusic"
							
					if self.data["chapter"] == 2:
						if self.playing != "CaveMusic":
							for item in music.Music:
								music.Stop(item)
							music.Play("CaveMusic")
							self.playing = "CaveMusic"
	
					if (((self.data["chapter"] == 1) or (self.data["chapter"] == 3) or (self.data["chapter"] == 6))):
						if self.playing != "JungleMusic":
							for item in music.Music:
								music.Stop(item)
							music.Play("JungleMusic")
							self.playing = "JungleMusic"
			
			chapter = int(self.data['chapter'])
			print "Loaded level", levelName
						
			if len(base.testLevelname) > 0:
				currentLevel.levelFileName = base.testLevelname
														
			# give the level access to the gameVariables
			currentLevel.pvars = gameVariables
			# run until user quits
			endState = currentLevel.run()
		
			if (endState == base.NEXTLEVEL):
				self.data['bibles'] = base.num_bibles
				self.data['bananas'] = base.numBananas
				
				self.data['level'] += 1
				currentLevel = None
				base.testLevelname = ""
			elif endState == base.GAMEOVER:
				base.num_bibles = int(self.data['bibles'])
				base.numBananas = int(self.data['bananas'])
				
				if base.testLevelname == "":
					currentLevel = initLevel(levelName)
				else: # special case for restarting the testlevel which uses custom level class 
					currentLevel = initCustomLevel("testlevel")
				
			elif (endState == base.RESTARTLEVEL):
				if base.testLevelname == "":
					currentLevel = initLevel(levelName)
				else: # special case for restarting the testlevel which uses custom level class 
					currentLevel = initCustomLevel("testlevel")
			elif endState == base.QUITGAME: # todo, game over screen?
				running = False
			elif endState == base.GOTOLEVEL:
				levelName = currentLevel.gotoLevelName
				currentLevel = initLevel(levelName)
				# need to keep track on these
				self.data['chapter'] = currentLevel.level_maj
				self.data['level'] = currentLevel.level_min
				base.testLevelname = ""
			elif endState == base.GOTOTESTLEVEL:
				if base.testLevelname == "": 
					Exception("testLevelname not set")
					# user the testlevel.py level script
					levelName = "testlevel"												 
								
					currentLevel = initCustomLevel(base.testLevelname)
								
					# need to keep track on these
					self.data['chapter'] = currentLevel.level_maj
					self.data['level'] = currentLevel.level_min
				else:
					raise Exception("Unknown level end state",endState)
			elif endState == base.SHOWGAMEOVER:
				return GameOver(self.main)
					
		#import menu
		#menu.Loading(self.main)
		return menu.Menu(self.main)
			
class GameOver(engine.State):	
	def __init__(self,main):
		self.main = main
		
	def init(self):
		self.quit = False
		self.cur = 0
		self.menu = ["", "close"]
		self.showMessage = "Congratulations! You beat the game!"
		self.bkgr = pygame.image.load(os.path.join("images","bibledave.png")).convert()
		self.zones = []

	def paint(self,screen):
		screen.fill((255,255,255))
		img = self.bkgr
		img.set_alpha(128)
		screen.blit(img,(0,0))
		
		bg = 0,0,0
		
		fnt = pygame.font.Font("BD_Cartoon_Shout.ttf",30)
		fnt2 = pygame.font.Font("BD_Cartoon_Shout.ttf",26)

		y = 255
		fg = (0xaa,0x00,0x00)
		score = 0
		
		self.zones = []
		n = 0
		c = 0,0,0
		img = fnt.render(self.showMessage,1,c)
		x = (base.SCREEN_WIDTH-img.get_width())/2
		screen.blit(img,(x,y))
		self.zones.append((n,pygame.Rect(x,y,img.get_width(),img.get_height())))
		
		y = 285
		for val in self.menu:
			c = 0,150,100
			if n == self.cur: 
				c = 250,250,250
			img = fnt2.render(val,1,c)
			img2 = fnt2.render(val,1,bg)
			x = (base.SCREEN_WIDTH-img.get_width())/2
			screen.blit(img2,(x+2,y+2))
			screen.blit(img,(x,y))
			self.zones.append((n,pygame.Rect(x,y,img.get_width(),img.get_height())))
			y += 10
			n += 1
		
		fnt = pygame.font.Font("BD_Cartoon_Shout.ttf",10)
		y = 550
		c = 29, 145, 3
		#c = 0,150,100
		for line in ["This game comes with ABSOLUTELY NO WARRANTY. It is free software and",
		"you are welcome to distribute it under the terms of the GNU General Public License.",
		"(C) The Bible Dave Development Team"]:
			img = fnt.render(line,1,c)
			img2 = fnt.render(line,1,bg)
##			x = (base.SCREEN_WIDTH-img.get_width())/2
			x = 10
			screen.blit(img2,(x+2,y+2))
			screen.blit(img,(x,y))
			y += 12
			
		
		fnt = pygame.font.Font("BD_Cartoon_Shout.ttf",10)
		x,y = 405,10
##		c = 36, 45, 126
		c = 85,85,85
		bg = 0,0,0
		
		info = "Bible Dave - Christian Coders Community project v%s" % base.VERSION
		img = fnt.render(info,1,c)
		img2 = fnt.render(info,1,bg)
		screen.blit(img2,(x+1,y+1))
		screen.blit(img,(x,y))

		pygame.display.flip()
		
	def event(self,e):
		data = base.DATA
##		gameVariables = self.main.gameVariables
		
		if e.type is KEYDOWN and e.key == K_UP:
			self.cur = (self.cur-1+len(self.menu))%len(self.menu)
			self.repaint()
		if e.type is KEYDOWN and e.key == K_DOWN:
			self.cur = (self.cur+1+len(self.menu))%len(self.menu)
			self.repaint()
			
		if e.type is MOUSEMOTION:
			for n,rect in self.zones:
				if rect.collidepoint(e.pos):
					if self.cur != n:
						self.cur = n
						self.repaint()
						
##		ToDo: Finish Joystick movement settings
##		if e.type is JOYAXISMOTION: and e.key == K_UP:
##			self.cur = (self.cur-1+len(self.menu))%len(self.menu)
##			self.repaint()
##		if e.type is JOYAXISMOTION: and e.key == K_DOWN:
##			self.cur = (self.cur+1+len(self.menu))%len(self.menu)
##			self.repaint()
			
		if (e.type is KEYDOWN and e.key in (K_RETURN,K_ESCAPE)) or (e.type is MOUSEBUTTONDOWN) or (e.type is  JOYBUTTONDOWN):
			val = self.menu[self.cur]
			if e.type is KEYDOWN and e.key == K_ESCAPE:
				return menu.Credits(self.main)

			if val == "close":
				return menu.Credits(self.main)
