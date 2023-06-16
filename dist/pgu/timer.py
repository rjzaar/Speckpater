"""A timer for games with set-rate FPS.
"""
from __future__ import division

from builtins import object
from past.utils import old_div
import pygame


class Timer(object):
    """A timer for games with set-rate FPS.
    
    <pre>Timer(fps)</pre>
    """

    def __init__(self, fps):
        if fps == 0:
            self.tick = self._blank
            return
        self.wait = old_div(1000, fps)
        self.nt = pygame.time.get_ticks()
        pygame.time.wait(0)

    def _blank(self):
        pass

    def tick(self):
        """Wait correct amount of time each frame.  Call this once per frame.
        
        <pre>Timer.tick()</pre>
        """
        self.ct = pygame.time.get_ticks()
        if self.ct < self.nt:
            pygame.time.wait(self.nt - self.ct)
            self.nt += self.wait
        else:
            self.nt = pygame.time.get_ticks() + self.wait


class Speedometer(object):
    """A timer replacement that returns out FPS once a second.
    <pre>Speedometer()</pre>
    
    <strong>Attributes</strong>
    <dl>
    <dt>fps <dd>always set to the current FPS
    </dl>
    """

    def __init__(self):
        self.frames = 0
        self.st = pygame.time.get_ticks()
        self.fps = 0

    def tick(self):
        """ Call this once per frame.
        
        <pre>Speedometer.tick()</pre>
        """
        r = None
        self.frames += 1
        self.ct = pygame.time.get_ticks()
        if (self.ct - self.st) >= 1000:
            r = self.fps = self.frames
            # print "%s: %d fps"%(self.__class__.__name__,self.fps)
            self.frames = 0
            self.st += 1000
        pygame.time.wait(0)  # NOTE: not sure why, but you gotta call this now and again
        return r

# vim: set filetype=python sts=4 sw=4 noet si :
