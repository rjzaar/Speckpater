from __future__ import division
from __future__ import print_function
from builtins import str
from past.utils import old_div
import pygame
from pygame.locals import *
from pgu.tilevid import *
import copy
import base
import items
import random
import math
from base import difficultyMul, difficultyLevel

# constants used for the confusion stars

# in frames, for each difficulty level, should be high enough for all stars 
TIME_CONFUSED = (base.FPS * 3.0, base.FPS * 2.0, base.FPS * 1.8)
TIME_BETWEEN_STARS = 7  # num frames after each star is created
MAX_CONFUSION_STARS = 5

## Player movement constants
X_MAX_SPEED = 8.0
X_ACCEL = 1.5
X_DEACCEL = 4.0

JUMP_SPEED = 15.0

Y_MAX_SPEED = 6.0
Y_ACCEL = 2.0
Y_DEACCEL = 2.0

GRAVITY = 1.5

MAX_FALL_SPEED = 13.0

# time in frames dave has to fall until he becomes "worried"
FALL_TIME = 24  # takes about 10 tiles long fall

# FALL_TIME is tuned so that dave can jump in level 4_1 from the lowest 
# tree branch on the right side of the river without getting hurt

AIR_CONTROL = 0.3  # How much horizontal control the player has when not on the ground

## Player state constants
## (state number, max number of frames, time interval, has direction?)
STAND = (1, 1, 1, 1);
WALK = (2, 4, 4, 1);
JUMP = (3, 1, 1, 1);
CLIMB = (4, 4, 3, 0);

## Player directions
LEFT = 1;
RIGHT = 2;


class StarSprite(Sprite):
    def __init__(self, g, timer):
        Sprite.__init__(self, g.images['star'], g.player.rect.topleft)
        self.spdMul = 0.3
        self.xmag = random.randrange(14, 20)
        self.ymag = random.randrange(3, 6)
        self.xcycle = 0.5 + random.random() * 0.5
        self.ycycle = 0.5 + random.random() * 0.5
        self.rframe = random.random() * 1000
        self.timer = timer

    def loop(self, game, sprite):
        r = ((game.frame + self.rframe) * self.spdMul) % 360

        self.rect.x = game.player.rect.centerx + math.sin(r * self.xcycle) * self.xmag - old_div(self.rect.width, 2)
        self.rect.y = game.player.rect.y + math.cos(r * self.ycycle) * self.ymag - old_div(self.rect.height, 2)

        self.timer -= 1
        if self.timer <= 0:
            game.sprites.remove(self)


class TalkativeSprite(Sprite):
    def __init__(self, g):
        Sprite.__init__(self, g.images['talkative'], (0, 0))

    def loop(self, game, sprite):
        self.rect.centerx = game.player.rect.centerx + 7
        self.rect.y = game.player.rect.y - 50

        cf = game.frame * 0.2 % 360
        scale = int(1.0 + math.sin(
            cf) * 0.25)  # Convert result into an int because: The transformation code below gives a deprecation warning that the above code does not accept floats.

        img = game.images['talkative'][0]
        img = pygame.transform.scale(img, (scale * 16, scale * 32))
        self.setimage(img)


# game.sprites.remove(self)

class Player(Sprite):
    def __init__(self, g, pos):
        Sprite.__init__(self, g.images['player_1_2_1'], pos)
        self.groups = g.string2groups('player')

        self.courage = base.MAX_COURAGE_POINTS
        self.confusionTimer = 0

        self.state = JUMP
        self.direction = RIGHT
        self.anim_frame = 1
        self.image_string = ""
        self.dy = self.dx = 0
        self.can_climb = 0
        self.state = self.state
        self.on_ground = 1
        self.go_down = 0
        self.jumpAllowed = True
        # timer for free move mode
        self.freeMode = 0

        self.actionTimer = 0

        self.fallTimer = 0

        self.talkativeMark = None

        self.hudHeight = 0

    def isTalkativeMarkerVisible(self):
        return self.talkativeMark != None

    def showTalkativeMarker(self, game, show):
        if show:
            if not self.isTalkativeMarkerVisible():
                self.talkativeMark = TalkativeSprite(game)
                game.sprites.append(self.talkativeMark)
        else:
            if self.isTalkativeMarkerVisible():
                game.sprites.remove(self.talkativeMark)
                self.talkativeMark = None

    def onClimbableTile(self, t):
        c = t.config
        # -- Determines if the player can climb this tile --#
        if (c['can_climb'] == 1 and (self.rect.left - 16) < t.rect.left and (self.rect.right + 16) > t.rect.right):
            self.can_climb = 1
            if (self.state == CLIMB):  ## This snaps the climbing player to the vine
                self.rect.left = t.rect.left

    def onTopLineContact(self, t):
        if self.freeMode > 0: return  # allow going trough
        c = t.config
        ## if it's climbable vine we can go down
        if self.go_down and c['can_climb'] == 1:
            if ((self.rect.left - 16) < t.rect.left and (self.rect.right + 16) > t.rect.right):
                self.can_climb = 1
                ## Snap the player x to the vine x
                self.rect.left = t.rect.left
        else:
            self.rect.bottom = t.rect.top
            self.on_ground = 1
            self.dy = 0

    def onBottomLineContact(self, t):
        if self.freeMode > 0: return
        self.dy = 0

    def onLeftLineContact(self, t):
        if self.freeMode > 0:    return
        self.rect.right = t.rect.left
        self.dx = 0

    def onRightLineContact(self, t):
        if self.freeMode > 0: return
        self.rect.left = t.rect.right
        self.dx = 0

    def onTrouble(self, value):
        if self.confusionTimer == 0:
            self.confusionTimer = TIME_CONFUSED[(difficultyLevel() - 1)]
            self.courage -= value * difficultyMul()
            if self.courage < 0:
                self.courage = 0

            return True
        return False

    def encourage(self, value):
        self.courage += value * difficultyMul()
        if self.courage > base.MAX_COURAGE_POINTS:
            self.courage = base.MAX_COURAGE_POINTS

    def onPickupBanana(self, game, num):
        base.numBananas += num

        if game.getGameVar('firstbanana', False) == False:
            game.setGameVar('firstbanana', True)
            game.hud.add_pending_dialog(_("""Bananas are a good snack, I bet at least the monkeys think so.
			Tip: press T to throw a banana for the monkeys on the ground."""))

    ## Player Loop
    def loop(self, game, sprite):
        self.__move(game)
        self.__animate(game)
        self.on_ground = 0
        self.can_climb = 0

        # handle the confused time and add stars
        if self.confusionTimer > 0:

            tc = TIME_CONFUSED[(difficultyLevel() - 1)]
            lastStarTime = tc - TIME_BETWEEN_STARS * MAX_CONFUSION_STARS
            if lastStarTime < 0:
                raise "not enough time for confusion stars, increase the constant TIME_CONFUSED"

            timer = tc - self.confusionTimer
            if self.confusionTimer >= lastStarTime and timer % TIME_BETWEEN_STARS == 0:
                s = StarSprite(game, self.confusionTimer - (self.confusionTimer - lastStarTime))
                game.sprites.append(s)

            self.confusionTimer -= 1

    # if self.confusionTimer == 0:
    #	print "clear!"

    def __move(self, game):
        keys = pygame.key.get_pressed()
        # get joystick input
        joy = {"up": False, "down": False, "left": False, "right": False, \
               "one": False, "two": False, "twelve": False}
        if base.has_joy:  # peace, gentleness..... No wait wrong kind of joy.
            joy["up"] = base.joy.get_axis(1) < -0.1
            joy["down"] = base.joy.get_axis(1) > 0.1
            joy["left"] = base.joy.get_axis(0) < -0.1
            joy["right"] = base.joy.get_axis(0) > 0.1
            joy["one"] = base.joy.get_button(0)
            joy["two"] = base.joy.get_button(1)
            joy["twelve"] = base.joy.get_button(11)  # 'A' button on Xbox 360 controller with MacOSX driver
        # joy["thirteen"] = base.joy.get_button(12)
        # print joy["twelve"]

        self.upOrDownKeys = keys[K_DOWN] or keys[K_UP] or joy["down"] or joy["up"]
        # self.upOrDownKeys = keys[K_DOWN] or keys[K_UP]
        prevState = self.state

        if keys[K_m]:
            game.hud.show_pending_dialog()

        if self.freeMode > 0:
            self.freeMode -= 1

        # check if we are falling
        if self.on_ground == 0 and self.state != CLIMB and self.freeMode == 0:
            self.fallTimer += 1
        else:
            # if we have fell too long and didnt grab from a vine
            if self.fallTimer > FALL_TIME and self.state != CLIMB and self.freeMode == 0:
                if game.daveInTrouble(old_div((self.fallTimer - FALL_TIME), 3)):
                    if base.SOUND:
                        base.sound.Play("oof1")
                    print("ouch")
                    if self.courage > 0 and not game.getGameVar('fallLesson', False):
                        game.setGameVar('fallLesson', True)
                        game.hud.add_pending_dialog(_("""Owh, I hurt my ankle in that fall. 
						I have to be more careful when jumping down from high... 
						\"The LORD upholdeth all that fall, and raiseth up all those that be bowed down.\"
						... That psalm 145, 14, always encourages me to continue."""))

            self.fallTimer = 0

        # free move mode
        if base.Testing:
            fmtim = 10

            moveDist = 20
            if keys[K_KP0]:
                moveDist *= 2

            if keys[K_KP8]:
                self.rect.y -= moveDist
                self.freeMode = fmtim
            if keys[K_KP2]:
                self.rect.y += moveDist
                self.freeMode = fmtim
            if keys[K_KP6]:
                self.rect.x += moveDist
                self.freeMode = fmtim
            if keys[K_KP4]:
                self.rect.x -= moveDist
                self.freeMode = fmtim

        if (self.on_ground == 1):
            self.state = STAND

        if ((keys[K_t] or joy["one"]) and self.actionTimer == 0 and base.numBananas > 0):
            # if (keys[K_t] and self.actionTimer == 0 and base.numBananas > 0):
            base.numBananas -= 1
            s = items.Banana(game, self.rect)
            game.sprites.append(s)
            dir = 45
            if (self.direction == LEFT): dir = -45
            s.throw(dir(8))
            self.actionTimer = base.FPS * 3

        if self.actionTimer > 0:
            self.actionTimer -= 1

        if ((keys[K_SPACE] or joy["two"] or joy["twelve"]) and self.jumpAllowed and (
                ((self.on_ground == 1) and (self.state != JUMP)) or (self.state == CLIMB))):

            # if (keys[K_SPACE] and self.jumpAllowed and (((self.on_ground == 1) and (self.state != JUMP)) or (self.state == CLIMB))):
            self.jumpAllowed = False
            self.dy = -JUMP_SPEED
            self.state = JUMP
            self.on_ground = 0

            if (prevState == CLIMB):
                self.dy = old_div(self.dy * 4, 5)

        if not (keys[K_SPACE] or joy["two"]):
            # if not keys[K_SPACE]:
            self.jumpAllowed = True

        ## We check to see if we're trying to walk in one direction or another
        if (self.state == CLIMB):
            if (self.can_climb == 1):
                self.dx = 0  ## If they jumped onto a vine, this makes them stop their vertical momentum.
            else:
                self.state = JUMP  ## This means that if they were trying to climb, but now they no longer can climb, then they should be in a jump state (they went off the end of the vine)
        else:
            self.dy += GRAVITY
            if keys[K_LEFT] or joy["left"]:
                self.direction = LEFT
                if (self.state != JUMP):
                    self.state = WALK

                if self.fallTimer == 0:
                    self.dx -= X_ACCEL
                else:
                    self.dx -= X_ACCEL * AIR_CONTROL

                # If Dave is jumping from a vine, make him jump at full speed with no accelleration.
                if (prevState == CLIMB):
                    self.dx = -X_MAX_SPEED

                if (self.dx < -X_MAX_SPEED):
                    self.dx = -X_MAX_SPEED

            if keys[K_RIGHT] or joy["right"]:
                self.direction = RIGHT
                if (self.state != JUMP):
                    self.state = WALK

                if self.fallTimer == 0:
                    self.dx += X_ACCEL
                else:
                    self.dx += X_ACCEL * AIR_CONTROL

                # If Dave is jumping from a vine, make him jump at full speed with no accelleration.
                if (prevState == CLIMB):
                    self.dx = X_MAX_SPEED

                if (self.dx > X_MAX_SPEED):
                    self.dx = X_MAX_SPEED

        ## Now we check to see if we're climbing. If so, climbing state trumps walk state (as far as display goes)
        if (self.can_climb == 1):
            if keys[K_UP] or joy["up"]:
                self.state = CLIMB
                self.dy -= Y_ACCEL
                if (self.dy < -Y_MAX_SPEED):
                    self.dy = -Y_MAX_SPEED
            elif keys[K_DOWN] or joy["down"]:
                if self.on_ground == 0:
                    self.state = CLIMB
                self.dy += Y_ACCEL
                if (self.dy > Y_MAX_SPEED):
                    self.dy = Y_MAX_SPEED
            elif (self.state == CLIMB):
                if (self.dy > 0):
                    self.dy -= Y_DEACCEL
                    if self.dy < 0:
                        self.dy = 0
                elif (self.dy < 0):
                    self.dy += Y_DEACCEL
                    if self.dy > 0:
                        self.dy = 0

        if keys[K_DOWN] or joy["down"]:
            self.go_down = 1
        else:
            self.go_down = 0

        if (self.state == STAND):
            if (self.dx > 0):
                if (self.dx >= X_DEACCEL):
                    self.dx -= X_DEACCEL
                else:
                    self.dx = 0;
            elif (self.dx < 0):
                if (self.dx <= -X_DEACCEL):
                    self.dx += X_DEACCEL
                else:
                    self.dx = 0;

        # disable velocity for free moving
        if self.freeMode > 0:
            self.dy = 0
            self.dx = 0

        ## Limit the player sprite so that it can't go off the right edge of the screen.
        if (self.rect.x + self.rect.width + self.dx < game.bounds.width):
            if (self.rect.x + self.dx >= 0):
                self.rect.x += self.dx

        if (self.dy > MAX_FALL_SPEED):
            self.dy = MAX_FALL_SPEED  ## limit the speed gravity can pull you, otherwise you drop like a ROCK over long distances. :)

        if (self.rect.y + self.rect.height + self.dy > game.bounds.height):
            pass  # this is handled in basegamelevel
        else:
            if (self.rect.y + self.dy < 0):  ## Limit the player sprite so that it can't go off the top of the screen.
                self.rect.y = 0
                self.dy = 0
            else:
                self.rect.y += self.dy
                game.focus_rect = copy.copy(
                    self.rect)  ## We need to use a copy here, otherwise when there's an earthquake it sends the player flying all around randomly instead of just shaking the camera.
                game.focus_rect.y += old_div(self.hudHeight, 2)

    ## Update the player's sprite information
    def __animate(self, game):
        state, maxFrames, interval, hasDirection = self.state

        ## If Dave is climbing but not moving, his sprite is not updated
        if ((self.state == CLIMB) and not self.upOrDownKeys):
            return

        ## Image string format is "player_STATE_DIRECTION_FRAME"

        ## STATE
        image_string = "player_" + str(state)

        ## DIRECTION
        if (hasDirection):
            image_string += "_" + str(self.direction)
        else:
            image_string += "_0"

        ## FRAME
        if (maxFrames == 1):
            image_string += "_1"
        else:
            if ((game.frame % interval) == 0):
                self.anim_frame += 1
                if (self.anim_frame > maxFrames):
                    self.anim_frame = 1
            image_string += "_" + str(self.anim_frame)

        ## Set image string
        self.setimage(game.images[image_string])

    def setPos(self, pos):
        self.rect.x = pos[0] * base.TILE_SIZE
        self.rect.y = pos[1] * base.TILE_SIZE
        self.dx = 0
        self.dy = 0
