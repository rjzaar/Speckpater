from __future__ import division
from __future__ import print_function
from builtins import range
from past.utils import old_div
import pygame
from pygame.locals import *
import os, sys
import random
import base
import leveledit
from player import *

from enemies.enemy import *
from enemies.monkey import *
from enemies.snake import *
from enemies.puma import *
from enemies.jaguar import *
from enemies.groundenemy import *
from enemies.hungrymonkey import HungyMonkey
from enemies.popupenemy import *
from enemies.bat import *
from enemies.eagle import *
from enemies.beehive import *
from enemies.fallingblock import *
from enemies.rollingobject import *

import hud
from pgu import tilevid, timer

import guis
from guis import *

from pgu import gui, html

import levelfile

# from base import Testing
from base import testLevelname
from base import ResourceException
from base import TILE_SIZE
from base import makeBool

# MAYO add bible verses
from bibleverse import *
import eztext

BG_TILE_SIZE = 128


# ----------------------- #
#     Main Game Level Class    #
# ----------------------- #
## The individual game levels inherit from this class
class GameLevel(tilevid.Tilevid):
    background = "levelbg1.png"
    levelFileName = "level1_1"
    tilesetName = "commontiles"

    # persistent variables that will be saved, can be used for the story, etc
    pvars = None

    def getGameVar(self, key, default):
        if self.pvars != None and key in self.pvars:
            val = self.pvars[key]

            if type(default) == bool:
                return makeBool(val)
            else:
                return type(default)(self.pvars[key])
        return default

    def setGameVar(self, key, value):
        if self.pvars != None:
            self.pvars[key] = value

    ## Constructor -- maj and min are the major and minor level numbers
    def __init__(self, screen):
        tilevid.Tilevid.__init__(self)
        self.screen = screen

        ## create a background layer
        self.bg = tilevid.Tilevid()

        self.num_bibles = base.num_bibles
        ## This is the rectangle that we're focusing on.
        self.focus_rect = (0, 0, 1, 1)

        ##                self.loadLevel(self.level_maj, self.level_min)

        ## Create a new HUD
        self.hud = hud.HUD(self)

        ##MAYO: add the Bible verse set up
        if base.gameDifficulty == 1:
            self.mybible = bibleverse("easy")
            print("easy")
        elif base.gameDifficulty == 2:
            self.mybible = bibleverse("medium")
            print("medium")
        elif base.gameDifficulty == 3:
            self.mybible = bibleverse("hard")
            print("hard")

        self.inputing = False
        self.retval = []

        # for testing
        self.safeMode = False
        self.player = None

    ## Player Constructor
    def player_new(g, t, value):
        g.clayer[t.ty][t.tx] = 0
        g.focus_rect = t.rect  ## Set the initial focus for the screen
        dave = Player(g, t.rect)  ## Create the Dave player
        g.sprites.append(dave)
        g.player = dave
        g.player.numBananas = 0

    # -------------- #
    #     Monkey Enemy     #
    # -------------- #
    def monkey_enemy(g, t, a):
        s = Monkey(g, t.rect)
        g.sprites.append(s)

    # ------------- #
    #     Bat Enemies    #
    # ------------- #
    def bat_enemy_vert(g, t, a):
        s = Bat(g, t.rect)
        s.ycycle = 1  # How fast the bat should cycle vertically
        s.ymag = 3  # How dynamic the bat's vertical motion should be
        s.xcycle = 1  # How fast the bat should cycle horizontally
        s.xmag = 0  # How dynamic the bat's horizontal motion should be
        g.sprites.append(s)

    def bat_enemy_circle(g, t, a):
        s = Bat(g, t.rect)
        s.ycycle = 1  # How fast the bat should cycle vertically
        s.ymag = 3  # How dynamic the bat's vertical motion should be
        s.xcycle = 1  # How fast the bat should cycle horizontally
        s.xmag = 3  # How dynamic the bat's horizontal motion should be
        g.sprites.append(s)

    def bat_enemy_fig8(g, t, a):
        s = Bat(g, t.rect)
        s.ycycle = 2  # How fast the bat should cycle vertically
        s.ymag = 3  # How dynamic the bat's vertical motion should be
        s.xcycle = 1  # How fast the bat should cycle horizontally
        s.xmag = 5  # How dynamic the bat's horizontal motion should be
        g.sprites.append(s)

    # --------------- #
    #     Eagle Enemies    #
    # --------------- #

    def eagle_enemy_circle(g, t, a):
        s = Eagle(g, t.rect)
        s.ycycle = 1  # How fast the eagle should cycle vertically
        s.ymag = 3  # How dynamic the eagle's vertical motion should be
        s.xcycle = 1  # How fast the eagle should cycle horizontally
        s.xmag = 4.5  # How dynamic the eagle's horizontal motion should be
        g.sprites.append(s)

    # ------------- #
    #     Snake Enemy    #
    # ------------- #

    def snake_enemy(g, t, a):
        s = Snake(g, t.rect)
        g.sprites.append(s)

    # ----------------- #
    #     Bee Swarm Enemy    #
    # ----------------- #

    def beeswarm_enemy(g, t, a):
        s = BeeHive(g, t.rect)
        g.sprites.append(s)

    # --------------------- #
    #     Falling Block Enemy    #
    # --------------------- #
    def falling_block_enemy(g, t, a):
        s = FallingBlock(g, t.rect, 0)
        g.sprites.append(s)

    # ------------ #
    #     Puma Enemy     #
    # ------------ #

    def puma_enemy(g, t, a):
        s = Puma(g, t.rect, 14, 6.0, 1.6)
        g.sprites.append(s)

    # -------------- #
    #     Jaguar Enemy     #
    # -------------- #

    def jaguar_enemy(g, t, a):
        s = Jaguar(g, t.rect, 14, 6.0, 1.6)
        g.sprites.append(s)

    def hanging_spider_enemy(g, t, a):
        s = PopupEnemy(g, 'hangingspider', 1, 7, t.rect, 0, (False, False), (0, 0, 0, 4), 3, 0.05)
        g.sprites.append(s)

    def wallsnake_enemy_right(g, t, a):
        s = PopupEnemy(g, 'wallsnake', 3, 7, t.rect, 90, (False, False), (0, 0, 2, 1), 5)
        g.sprites.append(s)

    def wallsnake_enemy_left(g, t, a):
        s = PopupEnemy(g, 'wallsnake', 3, 7, t.rect, 90, (False, True), (-1, 0, 2, 1), 5)
        g.sprites.append(s)

    def wallsnake_enemy_down(g, t, a):
        s = PopupEnemy(g, 'wallsnake', 3, 7, t.rect, 0, (False, False), (0, 0, 0, 2), 5)
        g.sprites.append(s)

    def rollingstone_enemy_left(g, t, a):
        s = RollingObject(g, 'rollingstone', t.rect, -4, True)
        g.sprites.append(s)

    def rollingstone_enemy_right(g, t, a):
        s = RollingObject(g, 'rollingstone', t.rect, 4, True)
        g.sprites.append(s)

    def hungymonkey_enemy(g, t, a):
        # creates an ground enemy that wanders maxium of 14 tiles in distance to
        # west and east from the trigger (initial) position
        # maxium speed of 5.0 and accelaration of 1.4
        # s = GroundEnemy(g, g.images['spider_0_1'], t.rect, 14, 6.0, 2.5)
        s = HungyMonkey(g, t.rect, 14, 5.0, 1.4)
        g.sprites.append(s)

    # ----------- #
    #     Win Block    #
    # ----------- #
    ## This is the block that exits the level.
    def exit_block(g, t, a):

        def exit_hit(g, s, a):
            # base.sound.Play("LevelExit");
            g.OnExit()

        s = tilevid.Sprite(g.images['blank'], t.rect)
        g.sprites.append(s)
        s.agroups = g.string2groups('player')
        s.hit = exit_hit

    # ------------- #
    #     Bible Block    #
    # ------------- #

    def bible_block(g, t, a):
        def bible_pickup(g, s, a):
            if base.SOUND:
                base.sound.Play("BiblePickup");

            g.sprites.remove(s)
            # MAYO get the Bible verse and show it
            g.retval = g.mybible.getverse()
            g.inputing = False
            if g.retval[1]:
                # g.hud.show_dialog(_("""Damaged Bible! Type in the blank word to keep the bible"""));
                g.inputing = True
                g.hud.show_dialog(_("Damaged Bible! " + g.retval[0]));
            else:
                g.num_bibles += 1
                base.num_bibles = g.num_bibles
                g.hud.show_dialog(_(g.retval[0]));
            g.OnBiblePickedUp(s, s.tilepos)

        s = tilevid.Sprite(g.images['bible'], t.rect)
        g.sprites.append(s)
        s.agroups = g.string2groups('player')
        s.hit = bible_pickup

        s.tilepos = (
        old_div(t.rect.x, TILE_SIZE), old_div(t.rect.y, TILE_SIZE))  # this can be used to identify the specific bible

    def OnBiblePickedUp(g, bible, tile):
        if base.gameDifficulty == base.DIFFICULTY_HARDEST:
            g.player.encourage(3)  # default action is to encourage Dave
        else:
            g.player.encourage(4)  # default action is to encourage Dave

    # ------------- #
    #     Misc Blocks    #
    # ------------- #

    def bananas_block(g, t, a):
        def pickup(g, s, a):
            # base.sound.Play("");
            g.player.onPickupBanana(g, 3)
            g.sprites.remove(s)

        s = tilevid.Sprite(g.images['bananas'], t.rect)
        g.sprites.append(s)
        s.agroups = g.string2groups('player')
        s.hit = pickup

    # ---------------- #
    #     Special Blocks     #
    # ---------------- #
    def special_block1(g, t, a):
        g.OnRunSpecial1(g, t, a)
        pass

    def special_block2(g, t, a):
        g.OnRunSpecial2(g, t, a)
        pass

    def special_block3(g, t, a):
        g.OnRunSpecial3(g, t, a)
        pass

    def special_block4(g, t, a):
        g.OnRunSpecial4(g, t, a)
        pass

    def special_block5(g, t, a):
        g.OnRunSpecial5(g, t, a)
        pass

    def special_block6(g, t, a):
        g.OnRunSpecial6(g, t, a)
        pass

    def special_block7(g, t, a):
        g.OnRunSpecial7(g, t, a)
        pass

    def special_block8(g, t, a):
        g.OnRunSpecial8(g, t, a)
        pass

    # ------------------------- #
    #     Blank Special Run Events #
    # ------------------------- #
    ## These are meant to be overridden in the custom levels
    def OnRunSpecial1(self, g, t, a):
        pass

    def OnRunSpecial2(self, g, t, a):
        pass

    def OnRunSpecial3(self, g, t, a):
        pass

    def OnRunSpecial4(self, g, t, a):
        pass

    def OnRunSpecial5(self, g, t, a):
        pass

    def OnRunSpecial6(self, g, t, a):
        pass

    def OnRunSpecial7(self, g, t, a):
        pass

    def OnRunSpecial8(self, g, t, a):
        pass

    # ---------------- #
    #     Tile Code Data     #
    # ---------------- #
    ## Here we initialize the sprites that are to be spawned from the various codes.

    cdata = {
        1: (exit_block, None),  ## This is a exit block
        2: (player_new, None),
        ## This is a new player block. There should only be one of these on a map, otherwise it will cause problems.
        3: (bible_block, None),  ## This is a Bible that spawns and waits for the player to pick it up.
        4: (bananas_block, None),
        8: (special_block1, None),
        9: (special_block2, None),
        10: (special_block3, None),
        11: (special_block4, None),
        12: (special_block5, None),
        13: (special_block6, None),
        14: (special_block7, None),
        15: (special_block8, None),
        16: (monkey_enemy, None),
        17: (bat_enemy_vert, None),
        18: (bat_enemy_circle, None),
        19: (bat_enemy_fig8, None),
        20: (hungymonkey_enemy, None),
        21: (snake_enemy, None),
        22: (beeswarm_enemy, None),
        23: (falling_block_enemy, None),
        24: (jaguar_enemy, None),

        28: (hanging_spider_enemy, None),
        29: (wallsnake_enemy_right, None),
        30: (wallsnake_enemy_left, None),
        31: (wallsnake_enemy_down, None),

        32: (rollingstone_enemy_left, None),
        33: (rollingstone_enemy_right, None),

        34: (eagle_enemy_circle, None),

    }

    # ------------------- #
    #     Sprite Image Data    #
    # ------------------- #
    ## Here we initialize the image data.     The columns are (name,file_name,shape)
    ## Naming convention is Pose_Direction_Frame
    idata = [
        ## Stand
        ('player_1_1_1', os.path.join('images', 'dave_stand_left.png'), (0, 0, 32, 48)),
        ('player_1_2_1', os.path.join('images', 'dave_stand_right.png'), (0, 0, 32, 48)),
        ## Walk
        ## Left
        ('player_2_1_1', os.path.join('images', 'dave_walk_left_1.png'), (0, 0, 32, 48)),
        ('player_2_1_2', os.path.join('images', 'dave_walk_left_2.png'), (0, 0, 32, 48)),
        ('player_2_1_3', os.path.join('images', 'dave_walk_left_3.png'), (0, 0, 32, 48)),
        ('player_2_1_4', os.path.join('images', 'dave_walk_left_4.png'), (0, 0, 32, 48)),
        ## Right
        ('player_2_2_1', os.path.join('images', 'dave_walk_right_1.png'), (0, 0, 32, 48)),
        ('player_2_2_2', os.path.join('images', 'dave_walk_right_2.png'), (0, 0, 32, 48)),
        ('player_2_2_3', os.path.join('images', 'dave_walk_right_3.png'), (0, 0, 32, 48)),
        ('player_2_2_4', os.path.join('images', 'dave_walk_right_4.png'), (0, 0, 32, 48)),
        ## Jump
        ('player_3_1_1', os.path.join('images', 'dave_jump_left.png'), (0, 0, 32, 48)),
        ('player_3_2_1', os.path.join('images', 'dave_jump_right.png'), (0, 0, 32, 48)),
        ## Climb
        ('player_4_0_1', os.path.join('images', 'dave_climb1.png'), (0, 0, 32, 48)),
        ('player_4_0_2', os.path.join('images', 'dave_climb2.png'), (0, 0, 32, 48)),
        ('player_4_0_3', os.path.join('images', 'dave_climb3.png'), (0, 0, 32, 48)),
        ('player_4_0_4', os.path.join('images', 'dave_climb4.png'), (0, 0, 32, 48)),

        #############
        ## Enemies ##
        #############

        ## Monkey
        ('monkey_0_1', os.path.join('images', 'monkey1.png'), (0, 0, 32, 32)),
        ('monkey_0_2', os.path.join('images', 'monkey2.png'), (0, 0, 32, 32)),
        ('monkey_0_3', os.path.join('images', 'monkey3.png'), (0, 0, 32, 32)),
        ('monkey_0_4', os.path.join('images', 'monkey4.png'), (0, 0, 32, 32)),

        # ('monkey_1_1',os.path.join('images', 'monkeyEating1.png'),(0, 0, 32, 32)),

        ## Guava
        ('guava', os.path.join('images', 'guava.png'), (0, 0, 20, 16)),

        ## Bat
        ('bat_0_1', os.path.join('images', 'bat1.png'), (0, 0, 17, 14)),
        ('bat_0_2', os.path.join('images', 'bat2.png'), (0, 0, 17, 14)),
        ('bat_0_3', os.path.join('images', 'bat3.png'), (0, 0, 17, 14)),

        ## Eagle
        ('eagle_0_1', os.path.join('images', 'eagle.png'), (0, 0, 91, 76)),
        ('eagle_0_2', os.path.join('images', 'eagle2.png'), (0, 0, 91, 76)),
        ('eagle_0_3', os.path.join('images', 'eagle3.png'), (0, 0, 91, 76)),
        ('eagle_0_4', os.path.join('images', 'eagle4.png'), (0, 0, 91, 76)),
        ('eagle_0_5', os.path.join('images', 'eagle5.png'), (0, 0, 91, 76)),

        ## Snake
        ('snake_0_1', os.path.join('images', 'snake1.png'), (0, 0, 10, 30)),
        ('snake_0_2', os.path.join('images', 'snake2.png'), (0, 0, 10, 30)),
        ('snake_0_3', os.path.join('images', 'snake3.png'), (0, 0, 10, 30)),

        ## Spider
        ('spider_0_1', os.path.join('images', 'spider1.png'), (0, 0, 28, 14)),
        ('spider_0_2', os.path.join('images', 'spider2.png'), (0, 0, 28, 14)),
        ('spider_0_3', os.path.join('images', 'spider3.png'), (0, 0, 28, 14)),

        ## Bees
        ('beehive', os.path.join('images', 'beehive.png'), (0, 0, 32, 32)),
        ('beeswarm_0_1', os.path.join('images', 'beeswarm1.png'), (0, 0, 32, 32)),
        ('beeswarm_0_2', os.path.join('images', 'beeswarm2.png'), (0, 0, 32, 32)),
        ('beeswarm_0_3', os.path.join('images', 'beeswarm3.png'), (0, 0, 32, 32)),
        ('beeswarm_0_4', os.path.join('images', 'beeswarm4.png'), (0, 0, 32, 32)),

        ## Falling blocks
        ('block', os.path.join('images', 'block.png'), (0, 0, 64, 32)),

        ('rollingstone', os.path.join('images', 'rollingstone.png'), (0, 0, 32, 32)),

        ## Jaguar
        ('jaguar_1_1', os.path.join('images', 'jaguar_1_1.png'), (0, 0, 69, 29)),
        ('jaguar_1_2', os.path.join('images', 'jaguar_1_2.png'), (0, 0, 69, 29)),
        ('jaguar_1_3', os.path.join('images', 'jaguar_1_3.png'), (0, 0, 69, 29)),
        ('jaguar_1_4', os.path.join('images', 'jaguar_1_4.png'), (0, 0, 69, 29)),
        ('jaguar_1_5', os.path.join('images', 'jaguar_1_5.png'), (0, 0, 69, 29)),
        ('jaguar_1_6', os.path.join('images', 'jaguar_1_6.png'), (0, 0, 69, 29)),
        ('jaguar_2_1', os.path.join('images', 'jaguar_2_1.png'), (0, 0, 69, 29)),
        ('jaguar_2_2', os.path.join('images', 'jaguar_2_2.png'), (0, 0, 69, 29)),
        ('jaguar_2_3', os.path.join('images', 'jaguar_2_3.png'), (0, 0, 69, 29)),
        ('jaguar_2_4', os.path.join('images', 'jaguar_2_4.png'), (0, 0, 69, 29)),
        ('jaguar_2_5', os.path.join('images', 'jaguar_2_5.png'), (0, 0, 69, 29)),
        ('jaguar_2_6', os.path.join('images', 'jaguar_2_6.png'), (0, 0, 69, 29)),

        ('jag_walk_1_1', os.path.join('images', 'jag_walk_1_1.png'), (0, 0, 69, 29)),
        ('jag_walk_1_2', os.path.join('images', 'jag_walk_1_2.png'), (0, 0, 69, 29)),
        ('jag_walk_1_3', os.path.join('images', 'jag_walk_1_3.png'), (0, 0, 69, 29)),
        ('jag_walk_1_4', os.path.join('images', 'jag_walk_1_4.png'), (0, 0, 69, 29)),
        ('jag_walk_1_5', os.path.join('images', 'jag_walk_1_5.png'), (0, 0, 69, 29)),
        #                 ('jag_walk_1_6',os.path.join('images', 'jag_walk_1_6.png'),(0, 0, 69, 29)),
        ('jag_walk_2_1', os.path.join('images', 'jag_walk_2_1.png'), (0, 0, 69, 29)),
        ('jag_walk_2_2', os.path.join('images', 'jag_walk_2_2.png'), (0, 0, 69, 29)),
        ('jag_walk_2_3', os.path.join('images', 'jag_walk_2_3.png'), (0, 0, 69, 29)),
        ('jag_walk_2_4', os.path.join('images', 'jag_walk_2_4.png'), (0, 0, 69, 29)),
        ('jag_walk_2_5', os.path.join('images', 'jag_walk_2_5.png'), (0, 0, 69, 29)),
        #                 ('jag_walk_2_6',os.path.join('images', 'jag_walk_2_6.png'),(0, 0, 69, 29)),

        ('monkey_walk_1', os.path.join('images', 'monkey_walk_1.png'), (0, 0, 32, 32)),
        ('monkey_walk_2', os.path.join('images', 'monkey_walk_2.png'), (0, 0, 32, 32)),
        ('monkey_walk_3', os.path.join('images', 'monkey_walk_3.png'), (0, 0, 32, 32)),
        # ('monkey_walk_4',os.path.join('images', 'monkey_walk_4.png'),(0, 0, 32, 32)),
        ('monkey_sit_1', os.path.join('images', 'monkey_sit.png'), (0, 0, 32, 32)),
        ('monkey_sit_2', os.path.join('images', 'monkey_sit_2.png'), (0, 0, 32, 32)),

        ('monkey_banana_1', os.path.join('images', 'monkey_banana_1.png'), (0, 0, 32, 32)),
        ('monkey_banana_2', os.path.join('images', 'monkey_banana_2.png'), (0, 0, 32, 32)),
        ('monkey_banana_3', os.path.join('images', 'monkey_banana_3.png'), (0, 0, 32, 32)),
        # monkey_banana_2.png

        ('hangingspider_1', os.path.join('images', 'hangingspider1.png'), (0, 0, 28, 128)),
        ('wallsnake_1', os.path.join('images', 'wallsnake1.png'), (0, 0, 32, 64)),
        ('wallsnake_2', os.path.join('images', 'wallsnake2.png'), (0, 0, 32, 64)),
        ('wallsnake_3', os.path.join('images', 'wallsnake3.png'), (0, 0, 32, 64)),

        ##########
        ## Misc ##
        ##########

        ('banana', os.path.join('images', 'banana.png'), (0, 0, 18, 18)),
        ('bananas', os.path.join('images', 'bananas.png'), (0, 0, 32, 32)),

        ('star', os.path.join('images', 'star.png'), (0, 0, 6, 6)),
        ('talkative', os.path.join('images', 'exclamation.png'), (0, 0, 17, 32)),

        ('blank', os.path.join('images', 'blank.png'), (0, 0, 32, 32)),
        ('bible', os.path.join('images', 'bible.png'), (0, 0, 32, 32)),
        # todo, load this in the first level only
        ('crashed_plane', os.path.join('images', 'crashed_plane.png'), (0, 0, 96, 64)),
    ]

    # ---------------- #
    #     Main Game Code     #
    # ---------------- #

    level_maj = 1
    level_min = 1

    # loads map geometry and background
    def loadLevelGeometry(self):
        w, h = base.SCREEN_WIDTH, base.SCREEN_HEIGHT

        fname, tname, codes, background = levelfile.loadLevelFile(self.levelFileName)

        tname = os.path.join('levels/tilesets', tname + '.png')
        fname = os.path.join('levels', fname + '.tga')
        background = os.path.join('levels', background + ".png")

        ## load the level from tga file
        try:
            self.tga_load_level(fname, 1)
        except IOError:
            raise ResourceException("Failed to level tga file \"" + fname + "\"")

        ## load the tileset
        try:
            self.tga_load_tiles(tname, (TILE_SIZE, TILE_SIZE), self.tdata)
        except IOError:
            raise ResourceException("Failed to load tileset from file \"" + tname + "\"")

        self.bounds = pygame.Rect(0, 0,
                                  len(self.tlayer[0]) * TILE_SIZE,
                                  (len(self.tlayer) * TILE_SIZE) + base.HUD_HEIGHT_INACTIVE);

        ## Load background tiles and randomize background.
        try:
            self.bg.tga_load_tiles(background, (BG_TILE_SIZE, BG_TILE_SIZE), self.tdata)
        except IOError:
            raise base.ResourceException("failed to load level background from \"" + background + "\"")

        ## parallaxing moves twice as slow as the foreground, but should contain
        ## the entire field.
        bgW = 5 + old_div((old_div(self.size[0], 4) - 5), 2)
        bgH = 4 + old_div((old_div(self.size[1], 4) - 4), 2)

        self.bg.resize((bgW, bgH));
        self.bg.bounds = pygame.Rect(0, 0,
                                     len(self.bg.tlayer[0]) * BG_TILE_SIZE,
                                     (len(self.bg.tlayer) * BG_TILE_SIZE) + base.HUD_HEIGHT_INACTIVE);

        for y in range(self.bg.size[1]):
            for x in range(self.bg.size[0]):
                self.bg.set((x, y), random.randint(0, 3));

    def loadLevelImages(self):
        self.load_images(self.idata)

    def loadLevel(self):
        w, h = base.SCREEN_WIDTH, base.SCREEN_HEIGHT

        self.loadLevelGeometry()

        ## Load the images for the game
        try:
            self.loadLevelImages()
        except pygame.error:
            # get_error() returns SDL error msg
            raise ResourceException(pygame.get_error())

        ## Run the codes on the map to spawn sprites
        self.run_codes(self.cdata, (0, 0, len(self.tlayer[0]), len(self.tlayer)))

        return True

    ## OnStart() is meant to be overridden by each individual level, to do various things (such as display messages) when the level starts.
    def OnStart(self):
        pass  ## do nothing

    def OnExit(self):
        self.gotoNextLevel()

    def OnLoop(self):
        pass

    def daveInTrouble(self, value):
        if not self.safeMode:
            # -1 means big trouble when player always looses the level
            if value == -1:
                self.nextState = base.GAMEOVER
            elif value > 0:
                # onTrouble returns False if dave cannot be troubled at the moment
                ret = self.player.onTrouble(value)
                # check if Dave has run out of courage
                if self.player.courage == 0:
                    self.nextState = base.GAMEOVER

                return ret
        return False

    def gotoNextLevel(self):
        self.nextState = base.NEXTLEVEL

    def handleKeys(self, key):
        if (key == K_ESCAPE):
            if base.Testing:  # allow quick quit if testing
                self.nextState = base.QUITGAME
            elif self.paused == 0:
                self.hud.pause()
                self.canexit = 1
        elif (key == K_F10):
            if (self.canexit == 1):
                self.paused = 0
                self.nextState = base.QUITGAME
        elif (base.Testing and key == K_F11):
            if (self.paused == 0):

                fname = leveledit.loadEditor(self, 'triggers')

                if self.levelFileName != fname:
                    print("level file changed to", fname + ", loading the testlevel script and restarting level")
                    # global testLevelname
                    base.testLevelname = fname
                    self.nextState = base.GOTOTESTLEVEL
                else:
                    print("reloading level geometry")
                    # reload the level geometry
                    self.loadLevelGeometry()

        elif (base.Testing and key == K_F5):
            self.nextState = base.RESTARTLEVEL
        elif (base.Testing and key == K_F3):
            self.safeMode = not self.safeMode
            print("safe mode =", self.safeMode)
        elif (base.Testing and key == K_F6):
            toggleSelectLevelDialog(self)
        elif (base.Testing and key == K_F7):
            base.testLevelname = "testlevel"
            self.nextState = base.GOTOTESTLEVEL
        elif (self.inputing):
            # collect key presses
            # self.hud.show_dialog(_(pygame.key.name(key)));
            # self.txtbx.update(key)
            # blit txtbx on the sceen
            # self.txtbx.draw(self.screen)
            pass


        else:
            next(self.hud)
            self.canexit = 0

    def handleButton(self, e):
        if e.button == 0 or e.button == 1:
            next(self.hud)
            self.canexit = 0

    def start(self):
        self.currentlevel = self
        self.frame = 0
        self.paused = 0
        self.quake = 0
        self.canexit = 0
        self.nextState = base.GAMECONTINUES

        self.OnStart()

    def run(self):
        time = timer.Timer(base.FPS)

        self.loadLevel()
        self.start()

        # global app
        maingui = gui.App()

        self.guiCont = gui.Container(align=0, valign=-1)

        self.levelSelDlg = SelectLevelDialog(self)

        # toggling dialog's visibility at certain position seems to be quite tricky
        # we need to first add the dialog in to the container ...
        self.guiCont.add(self.levelSelDlg, 0, 0)

        maingui.init(self.guiCont)

        # ... then we can remove it (so that it's invisible until we want to show it)
        self.guiCont.remove(self.levelSelDlg)
        self.levelSelDlg.isVisible = False
        # MAYO added the eztext
        txtbx = eztext.Input(maxlength=45, x=100, y=570, color=(255, 0, 0),
                             prompt="Type in the missing word to repair the Bible: ")
        while 1:
            # MAYO now check to see if the word is correct.
            ev = pygame.event.get()
            if self.inputing:
                txtbx.update(ev)
                txtbx.draw(self.screen)

                pygame.display.flip()

            for e in ev:

                if (e.type == QUIT):
                    self.nextState = base.QUITGAME
                elif (e.type == KEYDOWN):
                    # MAYO now add int the code to check for the bible being correct.
                    if ((e.key == K_RETURN) and self.inputing):
                        if txtbx.value == self.retval[2]:
                            self.num_bibles += 1
                            base.num_bibles = self.num_bibles
                            self.hud.show_dialog(_("You fixed the Bible!"));
                            txtbx.value = ""

                        else:
                            self.hud.show_dialog(_("You couldn't fix the Bible!"));
                            txtbx.value = ""

                        txtbx.update(ev)
                        txtbx.draw(self.screen)

                        pygame.display.flip()
                        self.inputing = False
                    self.handleKeys(e.key)
                elif (e.type == JOYBUTTONDOWN):
                    self.handleButton(e)
                else:
                    maingui.event(e)

            if (self.nextState != base.GAMECONTINUES):
                break

            ## Paint the background.
            self.bg.view.x = old_div(self.view.x, 2)
            self.bg.view.y = old_div(self.view.y, 2)
            self.bg.paint(self.screen)

            ## Paint the foreground (player and such)
            self.paint(self.screen)

            ## Paint the HUD
            if self.player != None:
                self.hud.paint(self.screen)
                self.player.hudHeight = self.hud.height

            maingui.paint(self.screen)

            # if not (self.paused):
            #         if (self.exit):
            #                 break         ## exit while

            if self.player != None and (
                    (self.player.rect.y + self.player.rect.height) > ((len(self.tlayer) - 1) * TILE_SIZE)):
                print("Whoops! Fell off the level -- try again!")
                self.daveInTrouble(-1)

            if not self.paused:

                self.frame += 1
                self.animate_background()

                # todo, the list index goes out of range in vid.py at line 427
                # when the bottom of dave's sprite rect goes out of the screen
                # edit: this bug should be fixed but leaving this here for now until
                # try:

                self.OnLoop()
                self.loop()

                # todo should we catch the "undeclared variable" errors from level scripts?
                # except NameError, e:
                #         print e, ""
                # except IndexError, e:
                #         print e , "This is known bug which should have been fixed, plese report this"

                if (self.quake):
                    self.focus_rect.x += random.randrange(-5, 5)
                    self.focus_rect.y += random.randrange(-5, 5)
                    if (self.quake > 0):
                        self.quake -= 1

                self.view.clamp_ip(self.focus_rect)

            time.tick();

            pygame.display.flip()

        return self.nextState

    def __del__(self):
        ## Delete all of the sprites in the video
        while (len(self.sprites) > 0):
            self.sprites.remove(self.sprites[0])

        ## Delete the HUD
        del self.hud

    # some helper functions

    def addBlocks(self, blocks):
        for currTile in blocks:
            self.tlayer[currTile[0][1]][currTile[0][0]] = copy.copy(currTile[1])

    def removeBlocks(self, blocks):
        for currTile in blocks:
            self.tlayer[currTile[0][1]][currTile[0][0]] = 0

    def appendTileFromTrigger(self, array, t):
        x = old_div(t.rect.x, TILE_SIZE)
        y = old_div(t.rect.y, TILE_SIZE)
        tile = copy.copy(self.tlayer[y][x])
        array.append(((x, y), tile))

        # helper function

    def addTriggerCallback(self, pos, fn):
        s = tilevid.Sprite(self.images['blank'], pos)
        self.sprites.append(s)
        s.agroups = self.string2groups('player')  ## Set the 'player' group to collide with this object
        s.hit = fn
