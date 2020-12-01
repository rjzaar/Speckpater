from __future__ import division
from past.utils import old_div
import pygame
import os
import music

from pygame.locals import *
from pgu import engine
from pgu import gui

import base
from base import Testing
from base import blitText

from base import loadImage

import music

import gettext


# Generic functions ###
class Menu(engine.State):
    def __init__(self, main):
        self.main = main
        music.LoadMusic()

    def init(self):
        pygame.mouse.set_visible(True)
        self.quit = False
        self.cur = 0
        if os.path.exists(base.path):
            self.menu = ["continue game", "start a new game", "options", "credits", "help", "about", "quit"]
        else:
            self.menu = ["start a new game", "options", "credits", "help", "about", "quit"]
        self.bkgr = pygame.image.load(os.path.join("images", "speckpater_front.png")).convert()
        self.sourceforgeLogo = pygame.image.load(os.path.join("images", "sflogo.png")).convert()
        self.pythonLogo = pygame.image.load(os.path.join("images", "PythonPowered.gif")).convert()
        self.zones = []

    # if self.main.sound == True:
    # for music in self.main.playingMusic.keys():
    # if music != "menu":
    # if self.main.playingMusic[music] == True:
    # pygame.mixer.music.fadeout(1000)
    # self.main.playingMusic[music] = False
    # if self.main.playingMusic["menu"] != True:
    # self.main.playingMusic["menu"] = True
    # pygame.mixer.music.load(os.path.join("sounds","bgmusic.ogg"))
    # pygame.mixer.music.play(-1)

    def paint(self, screen):
        screen.fill((255, 255, 255))
        img = self.bkgr
        screen.blit(img, (0, 0))

        screen.blit(self.sourceforgeLogo, (630, 560))
        screen.blit(self.pythonLogo, (730, 560))

        bg = 0, 0, 0

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 26)

        ##		x,y = 0,300
        y = 250

        fg = (0x00, 0xaa, 0x00)
        score = 0

        self.zones = []
        n = 0
        for val in self.menu:
            # mayo: below starting with C=, is where colour change from main , new game, continue etc
            c = 119, 90, 254
            # mayo: below starting with C=, is colour for roll over of main , new game, continue, etc
            if n == self.cur:
                c = 63, 185, 0
            img = fnt.render(val, 1, c)
            img2 = fnt.render(val, 1, bg)
            x = old_div((base.SCREEN_WIDTH - img.get_width()), 2)
            screen.blit(img2, (x + 2, y + 2))
            screen.blit(img, (x, y))
            self.zones.append((n, pygame.Rect(x, y, img.get_width(), img.get_height())))
            y += 40
            n += 1

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 10)
        y = 550
        c = 49, 165, 23
        for line in ["This game comes with ABSOLUTELY NO WARRANTY. It is free software and",
                     "you are welcome to distribute it under the terms of the GNU General Public License.",
                     "(C) MAYO Development Team"]:
            img = fnt.render(line, 1, c)
            img2 = fnt.render(line, 1, bg)
            ##			x = (base.SCREEN_WIDTH-img.get_width())/2
            x = 10
            screen.blit(img2, (x + 2, y + 2))
            screen.blit(img, (x, y))
            y += 12

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 10)
        x, y = 405, 10
        ##		c = 36, 45, 126
        c = 0, 36, 0
        bg = 0, 0, 0

        info = "Speckpater - MAYO with thanks to the Christian Coders Community project v%s" % base.VERSION
        img = fnt.render(info, 1, c)
        img2 = fnt.render(info, 1, bg)
        screen.blit(img2, (x + 1, y + 1))
        screen.blit(img, (x, y))

        pygame.display.flip()

    def event(self, e):
        if base.SOUND:
            if base.PLAYING_MENU_MUSIC == False:
                for item in music.Music:
                    music.Stop(item)
                music.Play("MenuMusic")
                base.PLAYING_MENU_MUSIC = True
        ##		gameVariables = self.main.gameVariables

        if e.type is KEYDOWN and e.key == K_UP:
            self.cur = (self.cur - 1 + len(self.menu)) % len(self.menu)
            self.repaint()
        if e.type is KEYDOWN and e.key == K_DOWN:
            self.cur = (self.cur + 1 + len(self.menu)) % len(self.menu)
            self.repaint()

        if e.type is MOUSEMOTION:
            for n, rect in self.zones:
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

        if (e.type is KEYDOWN and e.key in (K_RETURN, K_ESCAPE)) or (e.type is MOUSEBUTTONDOWN) or (
                e.type is JOYBUTTONDOWN):
            val = self.menu[self.cur]
            if e.type is KEYDOWN and e.key == K_ESCAPE:
                return engine.Quit(self.main)

            if val == "continue game":
                base.PLAYING_MENU_MUSIC = False
                ##				return Loading(self.main)
                import game
                return game.Game(self.main)

            if val == "credits":
                return Credits(self.main)

            if val == "start a new game":
                base.PLAYING_MENU_MUSIC = False
                return SetDifficulty(self.main)
            if val == "quit":
                return engine.Quit(self.main)

            if val == "about":
                return About(self.main)

            if val == "help":
                return Help(self.main)

            if val == "options":
                return Options(self.main)


class Intro(engine.State):
    def __init__(self, main):
        self.main = main

    def init(self):
        pygame.mouse.set_visible(False)
        self.quit = False
        self.logo = pygame.image.load(os.path.join("images", "speck-splash4.gif")).convert()

    def paint(self, screen):
        # x = base.SCREEN_WIDTH/2
        screen.fill((255, 255, 255))
        img = self.logo
        y = old_div((base.SCREEN_HEIGHT - img.get_height()), 2)

        bg = 0, 0, 0
        c = 0
        fnt = pygame.font.Font(base.FONT_FILENAME, 26)

        x = old_div((base.SCREEN_WIDTH - img.get_width()), 2)
        x2 = x + 80
        y2 = y + 80
        ##		screen.blit(img2,(x+2,y+2))
        fnt2 = pygame.font.Font("BD_Cartoon_Shout.ttf", 40)
        while c <= 250:
            img2 = fnt.render("Community Project", 1, (c, c, c))
            screen.fill(bg)
            screen.blit(img, (x, y))
            screen.blit(img2, (x2, y2))
            c += 5

            img3 = fnt2.render("Loading...", 1, (250, 250, 250))
            screen.blit(img3, (300, 500))
            pygame.display.flip()

        return Menu(self.main)


class Options(engine.State):
    def __init__(self, main):
        self.main = main

    def init(self):
        self.quit = False
        self.cur = 0
        self.menu = ["fullscreen/windowed mode", "sounds and music on/off", "", "back"]
        self.bkgr = pygame.image.load(os.path.join("images", "speckpater_front.png")).convert()

        self.sourceforgeLogo = pygame.image.load(os.path.join("images", "sflogo.png")).convert()
        self.pythonLogo = pygame.image.load(os.path.join("images", "PythonPowered.gif")).convert()

        self.zones = []

    def paint(self, screen):
        screen.fill((255, 255, 255))
        img = self.bkgr
        screen.blit(img, (0, 0))

        screen.blit(self.sourceforgeLogo, (630, 560))
        screen.blit(self.pythonLogo, (730, 560))

        bg = 0, 0, 0

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 26)

        y = 250
        fg = (0xaa, 0x00, 0x00)
        score = 0

        self.zones = []
        n = 0
        for val in self.menu:
            c = 119, 90, 254
            if n == self.cur:
                c = 63, 185, 0
            img = fnt.render(val, 1, c)
            img2 = fnt.render(val, 1, bg)
            x = old_div((base.SCREEN_WIDTH - img.get_width()), 2)
            screen.blit(img2, (x + 2, y + 2))
            screen.blit(img, (x, y))
            self.zones.append((n, pygame.Rect(x, y, img.get_width(), img.get_height())))
            y += 40
            n += 1

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 10)
        y = 550
        c = 49, 165, 23
        for line in ["This game comes with ABSOLUTELY NO WARRANTY. It is free software and",
                     "you are welcome to distribute it under the terms of the GNU General Public License.",
                     "(C) MAYO Development Team"]:
            img = fnt.render(line, 1, c)
            img2 = fnt.render(line, 1, bg)
            ##			x = (base.SCREEN_WIDTH-img.get_width())/2
            x = 10
            screen.blit(img2, (x + 2, y + 2))
            screen.blit(img, (x, y))
            y += 12

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 10)
        x, y = 405, 10
        ##		c = 36, 45, 126
        c = 85, 85, 85
        bg = 0, 0, 0

        info = "Speckpater - MAYO with thanks to the Christian Coders Community project v%s" % base.VERSION
        img = fnt.render(info, 1, c)
        img2 = fnt.render(info, 1, bg)
        screen.blit(img2, (x + 1, y + 1))
        screen.blit(img, (x, y))

        pygame.display.flip()

    def event(self, e):
        ##		gameVariables = self.main.gameVariables

        if e.type is KEYDOWN and e.key == K_UP:
            self.cur = (self.cur - 1 + len(self.menu)) % len(self.menu)
            self.repaint()
        if e.type is KEYDOWN and e.key == K_DOWN:
            self.cur = (self.cur + 1 + len(self.menu)) % len(self.menu)
            self.repaint()

        if e.type is MOUSEMOTION:
            for n, rect in self.zones:
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

        if (e.type is KEYDOWN and e.key in (K_RETURN, K_ESCAPE)) or (e.type is MOUSEBUTTONDOWN) or (
                e.type is JOYBUTTONDOWN):
            val = self.menu[self.cur]
            if e.type is KEYDOWN and e.key == K_ESCAPE:
                return Menu(self.main)

            if val == "back":
                return Menu(self.main)
            if val == "sounds and music on/off":
                if base.SOUND:
                    pygame.mixer.quit()
                    base.SOUND = False
                    base.PLAYING_MENU_MUSIC = False
                else:
                    pygame.mixer.init()
                    base.SOUND = True
            # base.PLAYING_MENU_MUSIC = True

            if val == "fullscreen/windowed mode":
                # save changes
                if int(self.main.settings['fullScreen']) == 0:
                    self.main.settings['fullScreen'] = "1"
                elif int(self.main.settings['fullScreen']) == 1:
                    self.main.settings['fullScreen'] = "0"
                base.saveGameSettings(self.main.settings)

                pygame.display.quit()
                pygame.display.init()

                pygame.display.set_caption("Speckpater %s" % base.VERSION)
                pygame.display.set_icon(pygame.image.load(os.path.join("images", "dave_jump_right.png")))

                screenMode = base.getFullScreenFlag(self.main.settings)
                base.setScreenMode(screenMode, int(
                    self.main.settings['bpp']))  # Get bits per pixel (colour depth) mode from settings file and set it
                gamma = float(self.main.settings['gamma'])  # Get gama settings from settings file
                pygame.display.set_gamma(gamma, gamma, gamma)  # Set gamma

                self.main.screen = pygame.display.set_mode((base.SCREEN_WIDTH, base.SCREEN_HEIGHT), screenMode)
                pygame.display.flip()
                self.repaint()


class SetDifficulty(engine.State):
    def __init__(self, main):
        self.main = main

    def init(self):
        self.quit = False
        self.cur = 0
        self.menu = ["easy", "medium", "hard", "", "back"]
        self.bkgr = pygame.image.load(os.path.join("images", "speckpater_front.png")).convert()

        self.sourceforgeLogo = pygame.image.load(os.path.join("images", "sflogo.png")).convert()
        self.pythonLogo = pygame.image.load(os.path.join("images", "PythonPowered.gif")).convert()

        self.zones = []

    def paint(self, screen):
        screen.fill((255, 255, 255))
        img = self.bkgr
        screen.blit(img, (0, 0))

        screen.blit(self.sourceforgeLogo, (630, 560))
        screen.blit(self.pythonLogo, (730, 560))

        bg = 0, 0, 0

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 26)

        y = 250
        fg = (0xaa, 0x00, 0x00)
        score = 0

        self.zones = []
        n = 0
        for val in self.menu:
            c = 119, 90, 254
            if n == self.cur:
                c = 63, 185, 0
            img = fnt.render(val, 1, c)
            img2 = fnt.render(val, 1, bg)
            x = old_div((base.SCREEN_WIDTH - img.get_width()), 2)
            screen.blit(img2, (x + 2, y + 2))
            screen.blit(img, (x, y))
            self.zones.append((n, pygame.Rect(x, y, img.get_width(), img.get_height())))
            y += 40
            n += 1

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 10)
        y = 550
        c = 49, 165, 23
        for line in ["This game comes with ABSOLUTELY NO WARRANTY. It is free software and",
                     "you are welcome to distribute it under the terms of the GNU General Public License.",
                     "(C) MAYO Development Team"]:
            img = fnt.render(line, 1, c)
            img2 = fnt.render(line, 1, bg)
            ##			x = (base.SCREEN_WIDTH-img.get_width())/2
            x = 10
            screen.blit(img2, (x + 2, y + 2))
            screen.blit(img, (x, y))
            y += 12

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 10)
        x, y = 405, 10
        ##		c = 36, 45, 126
        c = 85, 85, 85
        bg = 0, 0, 0

        info = "Speckpater - MAYO with thanks to the Christian Coders Community project v%s" % base.VERSION
        img = fnt.render(info, 1, c)
        img2 = fnt.render(info, 1, bg)
        screen.blit(img2, (x + 1, y + 1))
        screen.blit(img, (x, y))

        pygame.display.flip()

    def event(self, e):
        data = base.DATA
        ##		gameVariables = self.main.gameVariables

        if e.type is KEYDOWN and e.key == K_UP:
            self.cur = (self.cur - 1 + len(self.menu)) % len(self.menu)
            self.repaint()
        if e.type is KEYDOWN and e.key == K_DOWN:
            self.cur = (self.cur + 1 + len(self.menu)) % len(self.menu)
            self.repaint()

        if e.type is MOUSEMOTION:
            for n, rect in self.zones:
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

        if (e.type is KEYDOWN and e.key in (K_RETURN, K_ESCAPE)) or (e.type is MOUSEBUTTONDOWN) or (
                e.type is JOYBUTTONDOWN):
            val = self.menu[self.cur]
            if e.type is KEYDOWN and e.key == K_ESCAPE:
                return Menu(self.main)

            if val == "back":
                return Menu(self.main)
            if val == "hard":
                data['chapter'] = 1
                data['level'] = 1
                data['bibles'] = 0
                data['bananas'] = 0
                data['difficulty'] = base.DIFFICULTY_HARDEST
                base.saveGame(data)
                ##				return Loading(self.main)
                import game
                return game.Game(self.main)

            if val == "easy":
                data['chapter'] = 1
                data['level'] = 1
                data['bibles'] = 0
                data['bananas'] = 0
                data['difficulty'] = base.DIFFICULTY_EASIEST
                base.saveGame(data)
                ##				return Loading(self.main)
                import game
                return game.Game(self.main)

            if val == "medium":
                data['chapter'] = 1
                data['level'] = 1
                data['bibles'] = 0
                data['bananas'] = 0
                data['difficulty'] = base.DIFFICULTY_MEDIUM
                base.saveGame(data)
                ##				return Loading(self.main)
                import game
                return game.Game(self.main)


class About(engine.State):
    def __init__(self, main):
        self.main = main

    def init(self):
        self.quit = False
        self.cur = 0
        self.menu = ["", "back"]
        self.aboutInfo = ["Speckpater (The Bacon Priest) is a Project of MAYO",
                          "(Mission Action Youth Organisation).",
                          "To find out more about MAYO see mayostudios.org",
                          "Speckpater is heavily based on Bible Dave",
                          "which is an opensource computer game.",
                          "Opensource games allow others to freely copy, modify",
                          "and redistribute the game.",
                          "We also licence this game as opensource (GPLv3) so others can copy,",
                          "modify and redistribute the game.",
                          "",
                          "Here is the original copyright/about information",
                          "Bible Dave - A Christian Coders Community project v%s" % base.VERSION,
                          "All code and images (C) Bible Dave Development Team",
                          "Released under the GNU General Public License v2 (See GPL-License.txt)",
                          "",
                          "Bible Dave uses Phil's Pygame Utilities (PGU) and Pygame",
                          "which are released under the GNU LGPL v2.1 (See LGPL-License.txt)"]
        self.bkgr = pygame.image.load(os.path.join("images", "speckpater_front.png")).convert()

        self.sourceforgeLogo = pygame.image.load(os.path.join("images", "sflogo.png")).convert()
        self.pythonLogo = pygame.image.load(os.path.join("images", "PythonPowered.gif")).convert()

        self.zones = []

    def paint(self, screen):
        screen.fill((255, 255, 255))
        img = self.bkgr
        img.set_alpha(128)
        screen.blit(img, (0, 0))

        screen.blit(self.sourceforgeLogo, (630, 560))
        screen.blit(self.pythonLogo, (730, 560))

        bg = 0, 0, 0

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 15)
        fnt2 = pygame.font.Font("BD_Cartoon_Shout.ttf", 26)

        y = 250
        fg = (0xaa, 0x00, 0x00)
        score = 0

        self.zones = []
        n = 0
        for val in self.aboutInfo:
            c = 0, 0, 0
            img = fnt.render(val, 1, c)
            x = old_div((base.SCREEN_WIDTH - img.get_width()), 2)
            screen.blit(img, (x, y))
            self.zones.append((n, pygame.Rect(x, y, img.get_width(), img.get_height())))
            y += 15
        # n += 1

        y1 = y + 30
        for val in self.menu:
            c = 119, 90, 254
            if n == self.cur:
                c = 63, 185, 0
            img = fnt2.render(val, 1, c)
            img2 = fnt2.render(val, 1, bg)
            x = old_div((base.SCREEN_WIDTH - img.get_width()), 2)
            screen.blit(img2, (x + 2, y1 + 2))
            screen.blit(img, (x, y1))
            self.zones.append((n, pygame.Rect(x, y, img.get_width(), img.get_height())))
            y1 += 10
            n += 1

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 10)
        y = 550
        c = 29, 145, 3
        # c = 0,150,100
        for line in ["This game comes with ABSOLUTELY NO WARRANTY. It is free software and",
                     "you are welcome to distribute it under the terms of the GNU General Public License.",
                     "(C) The Bible Dave Development Team"]:
            img = fnt.render(line, 1, c)
            img2 = fnt.render(line, 1, bg)
            ##			x = (base.SCREEN_WIDTH-img.get_width())/2
            x = 10
            screen.blit(img2, (x + 2, y + 2))
            screen.blit(img, (x, y))
            y += 12

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 10)
        x, y = 405, 10
        ##		c = 36, 45, 126
        c = 85, 85, 85
        bg = 0, 0, 0

        info = "Bible Dave - Christian Coders Community project v%s" % base.VERSION
        img = fnt.render(info, 1, c)
        img2 = fnt.render(info, 1, bg)
        screen.blit(img2, (x + 1, y + 1))
        screen.blit(img, (x, y))

        pygame.display.flip()

    def event(self, e):
        data = base.DATA
        ##		gameVariables = self.main.gameVariables

        if e.type is KEYDOWN and e.key == K_UP:
            self.cur = (self.cur - 1 + len(self.menu)) % len(self.menu)
            self.repaint()
        if e.type is KEYDOWN and e.key == K_DOWN:
            self.cur = (self.cur + 1 + len(self.menu)) % len(self.menu)
            self.repaint()

        if e.type is MOUSEMOTION:
            for n, rect in self.zones:
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

        if (e.type is KEYDOWN and e.key in (K_RETURN, K_ESCAPE)) or (e.type is MOUSEBUTTONDOWN) or (
                e.type is JOYBUTTONDOWN):
            val = self.menu[self.cur]
            if e.type is KEYDOWN and e.key == K_ESCAPE:
                return Menu(self.main)

            if val == "back":
                return Menu(self.main)


class Credits(engine.State):
    def __init__(self, main):
        self.main = main

    def init(self):
        self.quit = False
        self.cur = 0
        self.menu = ["", "main menu"]
        self.credits = ["The Mayo Team/speckpator team",

                        "Mr.Robert Zaar, Nicholas Munro, Kevin Doss", "Aidan Bui, Adeyn Dixon-Mason, Gabriel Hunyh",
                        "",
                        "The Bible dave/chiristian coders team",
                        ""
                        "Programming: Clint Herron (HanClinto), Joseph Quigley (CPUFreak91), Jari",
                        "Vincent van Beveren, HeardTheWord",
                        "",
                        "Art/Graphics: Lava, Vincent van Beveren", "Neil (Lotus)", "Kiwee -- Conceptual Artist",
                        "",
                        "Sound Effects:", "fingolfin", "Clint Herron (HanClinto)",
                        "",
                        "Music: Jeff McArthur, Andy Salazar, Penny (www.helpfulinventions.com)"
                        "",

                        "The rest:",
                        "Realm Master -- Conceptual Writer", "buddboy -- Web Site Designer",
                        "firemaker103 -- Web Site Designer", "Darryl Dixon -- Packager and game distribution",
                        "",
                        "Also special thanks to the", "Christian Coder's Network Community for their support",
                        "and to SourceForge.net for hosting"]
        self.bkgr = pygame.image.load(os.path.join("images", "speckpater_front.png")).convert()

        self.sourceforgeLogo = pygame.image.load(os.path.join("images", "sflogo.png")).convert()
        self.pythonLogo = pygame.image.load(os.path.join("images", "PythonPowered.gif")).convert()

        self.zones = []

    def paint(self, screen):
        screen.fill((255, 255, 255))
        img = self.bkgr
        img.set_alpha(128)
        screen.blit(img, (0, 0))

        screen.blit(self.sourceforgeLogo, (630, 560))
        screen.blit(self.pythonLogo, (730, 560))

        bg = 0, 0, 0

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 15)
        fnt2 = pygame.font.Font("BD_Cartoon_Shout.ttf", 26)

        y = 25
        fg = (0xaa, 0x00, 0x00)
        score = 0

        self.zones = []
        n = 0
        for val in self.credits:
            c = 0, 0, 0
            img = fnt.render(val, 1, c)
            x = old_div((base.SCREEN_WIDTH - img.get_width()), 2)
            screen.blit(img, (x, y))
            self.zones.append((n, pygame.Rect(x, y, img.get_width(), img.get_height())))
            y += 15
        # n += 1

        y1 = y + 30
        for val in self.menu:
            c = 119, 90, 254
            if n == self.cur:
                c = 63, 185, 0
            img = fnt2.render(val, 1, c)
            img2 = fnt2.render(val, 1, bg)
            x = old_div((base.SCREEN_WIDTH - img.get_width()), 2)
            screen.blit(img2, (x + 2, y1 + 2))
            screen.blit(img, (x, y1))
            self.zones.append((n, pygame.Rect(x, y, img.get_width(), img.get_height())))
            y1 += 10
            n += 1

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 10)
        y = 550
        c = 29, 145, 3
        # c = 0,150,100
        for line in ["This game comes with ABSOLUTELY NO WARRANTY. It is free software and",
                     "you are welcome to distribute it under the terms of the GNU General Public License.",
                     "(C) The Bible Dave Development Team"]:
            img = fnt.render(line, 1, c)
            img2 = fnt.render(line, 1, bg)
            ##			x = (base.SCREEN_WIDTH-img.get_width())/2
            x = 10
            screen.blit(img2, (x + 2, y + 2))
            screen.blit(img, (x, y))
            y += 12

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 10)
        x, y = 405, 10
        ##		c = 36, 45, 126
        c = 85, 85, 85
        bg = 0, 0, 0

        info = "Bible Dave - Christian Coders Community project v%s" % base.VERSION
        img = fnt.render(info, 1, c)
        img2 = fnt.render(info, 1, bg)
        screen.blit(img2, (x + 1, y + 1))
        screen.blit(img, (x, y))

        pygame.display.flip()

    def event(self, e):
        data = base.DATA
        print ("Hello!")
        ##		gameVariables = self.main.gameVariables

        if e.type is KEYDOWN and e.key == K_UP:
            self.cur = (self.cur - 1 + len(self.menu)) % len(self.menu)
            self.repaint()
        if e.type is KEYDOWN and e.key == K_DOWN:
            self.cur = (self.cur + 1 + len(self.menu)) % len(self.menu)
            self.repaint()

        if e.type is MOUSEMOTION:
            for n, rect in self.zones:
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

        if (e.type is KEYDOWN and e.key in (K_RETURN, K_ESCAPE)) or (e.type is MOUSEBUTTONDOWN) or (
                e.type is JOYBUTTONDOWN):
            val = self.menu[self.cur]
            if e.type is KEYDOWN and e.key == K_ESCAPE:
                return Menu(self.main)

            if val == "main menu":
                return Menu(self.main)


class Help(engine.State):
    def __init__(self, main):
        self.main = main

    def init(self):
        self.quit = False
        self.cur = 0
        self.menu = ["", "back"]
        self.helpInfo = ["Controls:",
                         "Jump -- Space", "Walk left -- Left arrow", "Walk right -- Right arrow",
                         "Grab hold of and climb up vine -- Up arrow", "Climb down vine -- Down arrow",
                         "View message -- M key", "Throw banana -- T"]
        self.bkgr = pygame.image.load(os.path.join("images", "speckpater_front.png")).convert()

        self.sourceforgeLogo = pygame.image.load(os.path.join("images", "sflogo.png")).convert()
        self.pythonLogo = pygame.image.load(os.path.join("images", "PythonPowered.gif")).convert()

        self.zones = []

    def paint(self, screen):
        screen.fill((255, 255, 255))
        img = self.bkgr
        img.set_alpha(128)
        screen.blit(img, (0, 0))

        screen.blit(self.sourceforgeLogo, (630, 560))
        screen.blit(self.pythonLogo, (730, 560))

        bg = 0, 0, 0

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 15)
        fnt2 = pygame.font.Font("BD_Cartoon_Shout.ttf", 26)

        y = 240
        fg = (0xaa, 0x00, 0x00)
        score = 0

        self.zones = []
        n = 0
        for val in self.helpInfo:
            c = 0, 0, 0
            img = fnt.render(val, 1, c)
            x = 250
            screen.blit(img, (x, y))
            self.zones.append((n, pygame.Rect(x, y, img.get_width(), img.get_height())))
            y += 18
        # n += 1

        y += 30
        for val in self.menu:
            c = 119, 90, 254
            if n == self.cur:
                c = 63, 185, 0
            img = fnt2.render(val, 1, c)
            img2 = fnt2.render(val, 1, bg)
            x = old_div((base.SCREEN_WIDTH - img.get_width()), 2)
            screen.blit(img2, (x + 2, y + 2))
            screen.blit(img, (x, y))
            self.zones.append((n, pygame.Rect(x, y, img.get_width(), img.get_height())))
            y += 10
            n += 1

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 10)
        y = 550
        c = 29, 145, 3
        # c = 0,150,100
        for line in ["This game comes with ABSOLUTELY NO WARRANTY. It is free software and",
                     "you are welcome to distribute it under the terms of the GNU General Public License.",
                     "(C) The Bible Dave Development Team"]:
            img = fnt.render(line, 1, c)
            img2 = fnt.render(line, 1, bg)
            ##			x = (base.SCREEN_WIDTH-img.get_width())/2
            x = 10
            screen.blit(img2, (x + 2, y + 2))
            screen.blit(img, (x, y))
            y += 12

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 10)
        x, y = 405, 10
        ##		c = 36, 45, 126
        c = 85, 85, 85
        bg = 0, 0, 0

        info = "Bible Dave - Christian Coders Community project v%s" % base.VERSION
        img = fnt.render(info, 1, c)
        img2 = fnt.render(info, 1, bg)
        screen.blit(img2, (x + 1, y + 1))
        screen.blit(img, (x, y))

        pygame.display.flip()

    def event(self, e):
        data = base.DATA
        ##		gameVariables = self.main.gameVariables

        if e.type is KEYDOWN and e.key == K_UP:
            self.cur = (self.cur - 1 + len(self.menu)) % len(self.menu)
            self.repaint()
        if e.type is KEYDOWN and e.key == K_DOWN:
            self.cur = (self.cur + 1 + len(self.menu)) % len(self.menu)
            self.repaint()

        if e.type is MOUSEMOTION:
            for n, rect in self.zones:
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

        if (e.type is KEYDOWN and e.key in (K_RETURN, K_ESCAPE)) or (e.type is MOUSEBUTTONDOWN) or (
                e.type is JOYBUTTONDOWN):
            val = self.menu[self.cur]
            if e.type is KEYDOWN and e.key == K_ESCAPE:
                return Menu(self.main)

            if val == "back":
                return Menu(self.main)
