from __future__ import division
from __future__ import print_function
from builtins import str
from future.utils import raise_
from past.utils import old_div
import os
from getpass import getuser

import pygame, pygame.font, pygame.image
import pygame
from pygame.locals import *
import levelfile

# remember to change the version number in bibledave.nsi
VERSION = "0.9"

### Game constants ###

EXIT = 0
NEWGAME = 1
SAVEGAME = 2
CONTINUEGAME = 3
LOADGAME = 4
SHOWCREDITS = 5
GOTOOPTIONS = 6

GAMECONTINUES = 0
RESTARTLEVEL = 1
NEXTLEVEL = 2
GOTOLEVEL = 3
GAMEOVER = 4
QUITGAME = 5
GOTOTESTLEVEL = 6
SHOWGAMEOVER = 7

DIFFICULTY_EASIEST = 1
DIFFICULTY_MEDIUM = 2
DIFFICULTY_HARDEST = 3

MAX_COURAGE_POINTS = 20

GRAVITY = 0.2
MAX_VELOCITY = 12

TILE_SIZE = 32

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

HUD_HEIGHT_ACTIVE = old_div(SCREEN_HEIGHT, 4)
HUD_HEIGHT_INACTIVE = old_div(SCREEN_HEIGHT, 7)

FPS = 30
NEEDED_BIBLES = 65
NEED_MORE_BIBLES = True
DONT_LOAD_LAST_LEVEL = False
DATA = None
SOUND = None
MUSIC_LOADED = False
PLAYING_MENU_MUSIC = False

FONT_FILENAME = "SF Comic Script.ttf"
HELP_OR_BUGS = """For help and bug reporting join or go to:
\thttp://sourceforge.net/projects/bibledave/
\thttp://christiandevs.com"""

# set this to one when you are testing
Testing = False
num_bibles = 0
numBananas = 0
# joystick variables
has_joy = False
joy = None
is_playing_music = False
is_playing_jungle = False
path = os.path.join(os.path.expanduser("~"), '.bibledave')
opath = os.path.join(os.path.expanduser("~"), '.bibledaveo')
print("The configuration file is located at:", path)


def A_(message): return message


languages = {"English": 'en', "Finnish": 'fi'}
curLang = "English"


def initLocalization(settings):
    import gettext
    import os
    localeDir = os.path.join(os.getcwd(), 'locales')

    curLang = settings['lang']

    # gettext.bindtextdomain('bibledave', localeDir )
    # gettext.textdomain('bibledave')
    # gettext.install('bibledave', localeDir)
    # print gettext.textdomain(),gettext.bindtextdomain('bibledave')

    language = [languages[curLang]]

    l = gettext.find('bibledave', localeDir, language)
    if l == None:
        raise NameError('No language file found for language')

    t = gettext.translation('bibledave', localeDir, language)
    t.install()


# helper function
def getFullScreenFlag(settings):
    return (0, pygame.FULLSCREEN)[int(settings['fullScreen'])]


def setLanguage(settings, langIndex):
    global curLang
    cl = settings['lang']

    lkeys = list(languages.keys())
    index = 0
    for key in lkeys:
        if key == cl:
            if index + 1 == len(lkeys):
                cl = lkeys[0]  # back to first
            else:
                cl = lkeys[index + 1]  # to next
            break
        index += 1

    curLang = cl
    settings['lang'] = cl
    # change the language
    initLocalization(settings)


def setGamma(settings, add):
    gamma = float(settings['gamma'])

    if add:
        gamma += 0.1
        if gamma > 2.0: gamma = 2.0
    else:
        gamma -= 0.1
        if gamma < 0.1: gamma = 0.1

    pygame.display.set_gamma(gamma, gamma, gamma)

    settings['gamma'] = gamma


def setColorDepth(settings, bIncrease):
    bpp = int(settings['bpp'])

    # just a couple of color modes, 32 and 16
    if bpp == 16:
        bpp = 32
    elif bpp == 32:
        bpp = 16

    # try to set the mode
    setScreenMode(getFullScreenFlag(settings), bpp)

    settings['bpp'] = bpp


def setSoundsEnabled(settings, notUsed):
    global soundsEnabled
    soundsEnabled = int(not soundsEnabled)
    enableSounds(soundsEnabled)
    settings['sounds'] = soundsEnabled


def setFullScreenMode(settings, notUsed):
    isFullScreen = settings['fullScreen']
    isFullScreen = int(not isFullScreen)

    # try to change the mode
    setScreenMode((0, pygame.FULLSCREEN)[isFullScreen], int(settings['bpp']))
    # save changes
    settings['fullScreen'] = isFullScreen


gameSettings = [
    ("lang", A_("Language"), curLang, setLanguage),
    ("bpp", A_("Color depth"), 32, setColorDepth), ("gamma", A_("Gamma correction"), 1.0, setGamma),
    # use boolean here for default value so that we know how to display it in the game settings menu
    ("sounds", A_("Sounds enabled"), True, setSoundsEnabled),
    ("fullScreen", A_("Full screen"), True, setFullScreenMode)]


def saveGameSettings(settings):
    f = open(opath, 'w')
    for opt in settings:
        f.write(opt + '\t' + str(settings[opt]) + '\n')
    f.close()


def loadGameSettings():
    settings = {}  # dictinory holds the settings
    # first load the default settings that should be overwritten
    for setting in gameSettings:
        # make booleans integers
        if type(bool()) == type(setting[2]):
            settings[setting[0]] = str(int(setting[2] == True))
        else:
            settings[setting[0]] = str(setting[2])

    if os.path.isfile(opath):
        f = open(opath, 'r')

        lines = f.readlines()
        for line in lines:
            strings = line.split()
            if (len(strings) != 2):
                print("Invalid game setting line \"" + str(strings) + "\", skipping it...")
                continue

            settings[strings[0]] = strings[1]

        f.close()

    return settings


def saveGame(data):
    f = open(path, 'w')
    for opt in data:
        f.write(opt + '\t' + str(data[opt]) + '\n')
    f.close()


# define the default values in here
saveGameKeys = {'chapter': 1, 'level': 1, 'difficulty': DIFFICULTY_MEDIUM, 'bibles': 0, 'need_more_bibles': True}


def hasValidSaveGameopen():
    try:
        f = open(path, 'r')
    except IOError:
        return False

    # ok we have the file, now see if it's valid or not
    data = loadGame()
    for key in list(saveGameKeys.keys()):
        # it's invalid if it's missing even one entry
        if not key in data:
            return False

    return True


def makeBool(value):
    if type(value) == str:
        return value == "True"
    return bool(value)


def getSaveGameVar(data, key, default):
    if key in data:
        if type(default) == bool:
            return makeBool(data[key])
        else:
            return type(default)(data[key])

    return default


def loadGame():
    data = {}  # dictinory holds the settings
    if os.path.exists(path) == False:
        # set the defaults
        for defEntry in list(saveGameKeys.items()):
            data[defEntry[0]] = defEntry[1]

    if os.path.isfile(path):
        f = open(path, 'r')

        lines = f.readlines()
        for line in lines:
            strings = line.split()
            if (len(strings) != 2):
                print("Invalid game data line \"" + str(strings) + "\", skipping it...")
                continue

            data[strings[0]] = strings[1]

        f.close()

    return data


def blitText(size, color, text, pos, shaOff=None):
    font = pygame.font.Font(FONT_FILENAME, size)

    if shaOff != None:
        txt = font.render(text, True, (0, 0, 0))
        screen.blit(txt, (pos[0] + shaOff[0], pos[1] + shaOff[1]))

    txt = font.render(text, True, color)
    screen.blit(txt, pos)


def drawTextColored(surface, fontsize, message, location, color):
    font = pygame.font.Font(FONT_FILENAME, fontsize)
    fontcolor = color
    orig = font.render(message, 1, fontcolor)

    ##		shadowcolor = 100, 100, 100
    ##		offset = 2
    ##		orig = orig.convert()
    ##		size = orig.get_width() + offset, orig.get_height() + offset
    ##		img = pygame.Surface(size, 16)
    ##		img = img.convert()
    ##		img.set_colorkey((0, 0, 0))
    ##		orig.set_palette_at(1, shadowcolor)
    ##		img.blit(orig, (offset, offset))
    ##		orig.set_palette_at(1, fontcolor)
    ##		img.blit(orig, (0, 0))
    ##		surface.blit(img, location)

    surface.blit(orig, location)


def drawText(surface, fontsize, message, location):
    drawTextColored(surface, fontsize, message, location, (191, 191, 191))


# This function is used by the HUD to determine when a line is too long, and when it should split.
def getTextRenderWidth(fontsize, message):
    font = pygame.font.Font(FONT_FILENAME, fontsize)
    txt = font.render(message, True, (0, 0, 0))
    return txt.get_width()


# ------------------------------------------------------- #
#	 Loads an image and converts it to the right bit depth	#
# ------------------------------------------------------- #
def loadImage(name):
    name = os.path.join('images', name)
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print("Failed loading image '%s', reason: '%s'" % (name, message))
        raise_(SystemExit, message)

    image = image.convert()
    return image


screen = None
sound = None
soundsEnabled = 1
testLevelname = ""


def setScreenMode(flags, bpp):
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, bpp)


def enableSounds(enable):
    global soundsEnabled
    soundsEnabled = enable


gameDifficulty = DIFFICULTY_MEDIUM


def difficultyMul():
    return float(gameDifficulty + 1) / (DIFFICULTY_MEDIUM + 1)


def difficultyMulStep(step):
    mul = 1.0 + step * float(gameDifficulty - DIFFICULTY_MEDIUM)
    # make sure it doesnt get too low
    if mul <= 0.0:
        mul = 0.001
        if base.Testing:
            raise "difficultyMulStep multiplier is negative or zero!"
    return mul


def difficultyLevel():
    return gameDifficulty


def initLevel(levelName):
    if (screen == None):
        raise Exception("screen is None")

    ## Dynamically import the level
    exec("from levels import " + levelName)

    ## Load the new level from the dynamically loaded module
    return eval(levelName + ".GameLevel(screen)")


from levels import tilesets
from levels.tilesets import *


def initCustomLevel(levelFileName):
    import basegamelevel

    # have to take a peek in the lev file to find out the tile class name
    fname, tname, codes, background = levelfile.loadLevelFile(levelFileName)

    exec("class GameLevel(basegamelevel.GameLevel,tilesets." + tname + ".Tileset): pass")
    return GameLevel(screen)


# exception class used to deal with all resource exceptions
# for example when some graphics file cannot be loaded

class ResourceException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
