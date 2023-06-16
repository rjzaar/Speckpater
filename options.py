from __future__ import division
from past.utils import old_div
import pygame
import os

from pygame.locals import *
from pgu import engine
from pgu import gui

import base
from base import Testing
from base import blitText

from base import loadImage

import gettext


# Generic functions ###
class Language(engine.State):
    def __init__(self, main):
        self.main = main

    def init(self):
        pygame.mouse.set_visible(1)
        self.quit = False
        self.cur = 0
        self.menu = ["back"]
        self.bkgr = pygame.image.load(os.path.join("images", "speckpater_front.png")).convert()
        self.zones = []

    def paint(self, screen):
        screen.fill((255, 255, 255))
        img = self.bkgr
        screen.blit(img, (0, 0))

        bg = 0, 0, 0

        fnt = pygame.font.Font("BD_Cartoon_Shout.ttf", 26)

        ##		x,y = 0,300
        y = 250
        fg = (0xaa, 0x00, 0x00)
        score = 0

        self.zones = []
        n = 0
        for val in self.menu:
            c = 0, 150, 100
            if n == self.cur:
                c = 250, 250, 250
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
        c = 0, 65, 226
        bg = 0, 0, 0

        info = "Bible Dave - Christian Coders Community project v%s" % base.VERSION
        img = fnt.render(info, 1, c)
        img2 = fnt.render(info, 1, bg)
        screen.blit(img2, (x + 1, y + 1))
        screen.blit(img, (x, y))

        pygame.display.flip()

    def event(self, e):
        data = self.main.data
        ##		gameVariables = self.main.gameVariables

        if e.type == KEYDOWN and e.key == K_UP:
            self.cur = (self.cur - 1 + len(self.menu)) % len(self.menu)
            self.repaint()
        if e.type == KEYDOWN and e.key == K_DOWN:
            self.cur = (self.cur + 1 + len(self.menu)) % len(self.menu)
            self.repaint()

        if e.type == MOUSEMOTION:
            for n, rect in self.zones:
                if rect.collidepoint(e.pos):
                    if self.cur != n:
                        self.cur = n
                        self.repaint()

        ##		ToDo: Finish Joystick movement settings
        ##		if e.type == JOYAXISMOTION: and e.key == K_UP:
        ##			self.cur = (self.cur-1+len(self.menu))%len(self.menu)
        ##			self.repaint()
        ##		if e.type == JOYAXISMOTION: and e.key == K_DOWN:
        ##			self.cur = (self.cur+1+len(self.menu))%len(self.menu)
        ##			self.repaint()

        if (e.type == KEYDOWN and e.key in (K_RETURN, K_ESCAPE)) or (e.type == MOUSEBUTTONDOWN) or (
                e.type == JOYBUTTONDOWN):
            val = self.menu[self.cur]
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                import menu
                return menu.Options(self.main)

            if val == "back":
                import menu
                return menu.Options(self.main)
