from __future__ import print_function
from builtins import object
import os, pygame.mixer

import base


class DaveSound(object):
    def __init__(self):
        pygame.mixer.init(22050, 8, 1, 2048)
        self.sounds = {'LevelExit': pygame.mixer.Sound(os.path.join('sounds', 'sound09.ogg'))}
        self.sounds['LevelStart'] = pygame.mixer.Sound(os.path.join('sounds', 'sound08.ogg'))
        self.sounds['GameStart'] = pygame.mixer.Sound(os.path.join('sounds', 'sound01.ogg'))
        self.sounds['BiblePickup'] = pygame.mixer.Sound(os.path.join('sounds', 'sound10.ogg'))

    # self.sounds['JungleMusic'] = pygame.mixer.Sound(os.path.join('sounds', 'jungle.ogg'))
    # self.sounds['caveMusic'] = pygame.mixer.Sound(os.path.join('music', 'cave.ogg'))
    #		self.sounds['Thud'] = pygame.mixer.Sound(os.path.join('sounds, 'Thud.wav'))

    def Play(self, soundName):

        if not base.soundsEnabled:
            return

        if (soundName not in self.sounds):
            self.sounds[soundName] = pygame.mixer.Sound(os.path.join('sounds', soundName + ".ogg"))

        soundToPlay = self.sounds.get(soundName)

        if (soundToPlay != None):
            soundToPlay.play()
        else:
            print("Could not play sound " + soundName)
