import os, pygame.mixer
import base
from pygame.locals import *
from pgu import engine
from pgu import gui

pygame.mixer.init()
global Music
Music = {"MenuMusic": None, "JungleMusic": None, "CaveMusic": None, "MountainMusic": None, "TempleMusic": None}


def LoadMusic():
    # print base.SOUND, base.MUSIC_LOADED
    if base.SOUND == True:
        if base.MUSIC_LOADED == False:
            Music["MenuMusic"] = pygame.mixer.Sound(os.path.join('sounds', 'bgmusic.ogg'))
            Music["JungleMusic"] = pygame.mixer.Sound(os.path.join('sounds', 'jungle.ogg'))
            Music["CaveMusic"] = pygame.mixer.Sound(os.path.join('sounds', 'cave.ogg'))
            Music["MountainMusic"] = pygame.mixer.Sound(os.path.join('sounds', 'mountain.ogg'))
            Music["TempleMusic"] = pygame.mixer.Sound(os.path.join('sounds', 'temple.ogg'))

            # pygame.mixer.music.load(os.path.join("sounds","bgmusic.ogg"))
            base.MUSIC_LOADED = True


def Play(category):
    #	print Music
    # print base.SOUND, base.MUSIC_LOADED
    if base.SOUND == True:
        if base.MUSIC_LOADED == True:
            Music[category].play(-1)


def Stop(category):
    #	print Music
    # print base.SOUND, base.MUSIC_LOADED
    if base.SOUND == True:
        if base.MUSIC_LOADED == True:
            # Music[category].stop()
            Music[category].fadeout(1800)
