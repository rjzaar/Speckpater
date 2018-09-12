## HUD class that draws the overlay GUI for a game, and handles showing dialog boxes as well

import pygame
from pygame.locals import *
import os, sys
import base
from base import Testing
from pgu import tilevid, timer
from math import pi
from base import loadImage
import time


INITIAL_TEXT_ALPHA = 191
MAX_DIALOG_PENDING_TIME = 7
MAX_MSG_MARKER_TIME = base.FPS * 2.5

class HUD:
	def __init__(self, vid):
		self.vid = vid
		self.dialog_text = " " ## Dialog text is the text waiting to be drawn. Show_text is what is actually drawn.
		self.cursor = 0
		self.frame = 0
		self.text_lines = self.dialog_text.splitlines()
		self.line = 0
		self.drawTextColor = INITIAL_TEXT_ALPHA
		self.display_lines = ("", "", "", "")
		self.wait_for_next = 0
		self.dialogOn = 0
		self.courageImg = loadImage("rainbow.png")
		
		self.fadeStep = 0 # used for the blank screen effect
		
		self.pendingDlgs = []
		self.talkMarkerTimer = 0
		
	def isDialogsPending(self):
		return len(self.pendingDlgs) > 0
	
		

	## paint() draws the HUD to the surface specified
	def paint(self, surface):
		h = base.SCREEN_HEIGHT
		w = base.SCREEN_WIDTH
		
		# check how long the dialogs have been pending and remove the old ones
		if len(self.pendingDlgs) > 0:
			if (time.time() - self.pendingDlgs[0][2]) > MAX_DIALOG_PENDING_TIME:
				print "removing dialog from pend"
				self.pendingDlgs.pop(0)	
		
		
		if self.vid.player.isTalkativeMarkerVisible():
			self.talkMarkerTimer += 1
			if self.dialogOn == 1 or self.talkMarkerTimer > MAX_MSG_MARKER_TIME:
				self.vid.player.showTalkativeMarker(self.vid,False)			
			
		else:
			if self.dialogOn == 0 and self.isDialogsPending():
				if self.talkMarkerTimer <= MAX_MSG_MARKER_TIME: # only if the marker wasnt removed due to timeout
					self.vid.player.showTalkativeMarker(self.vid,True)
					self.talkMarkerTimer = 0
				

		# process the fading unless the dialog is on
		if self.fadeStep > 0 and not self.dialogOn:		
			
			# render fade
			f = 1.0
			if self.fadeStep == 1 or self.fadeStep == 3:
				f = float(self.fadeTimer) / self.fadeStepFrames
				if self.fadeStep == 1:
					f = 1.0 - f # reversed
					
			a = 0.30 # Comments here??? What do these 7 lines accomplish??? -- asked by Clint 06/17/2006
			b = 0.70
			c = 2.0
			pygame.draw.rect(surface,(0,0,0),(0, 0         ,w/c *f ,h*a * f)); # top left
			pygame.draw.rect(surface,(0,0,0),(w-w/c*f ,0      ,w * f, h*a * f)); # top right
			pygame.draw.rect(surface,(0,0,0),(w-w/c * f, h-h*b * f ,w ,h*b * f )); # bottom right
			pygame.draw.rect(surface,(0,0,0),(0, h-h*b  * f        ,w/c * f ,h*b  * f)); # bottom left
			#surface.fill((0,0,0),(0,0,w,h))
			
			# update fade (blank screen effect)
			if self.fadeTimer > 0:
				self.fadeTimer -= 1
			
			if self.fadeTimer == 0:
										
				# call the function if one at the end of each fading phase
				cb = self.fadeCallbacks[self.fadeStep - 1]
				if cb != None:
					cb(self.vid)
						
				if self.fadeStep == 3: # if last step reached
					self.fadeStep = 0 # then we have completed the fading
				else:
					# prepare the next step
					self.fadeStepFrames = self.fadeTimes[self.fadeStep] * base.FPS
					self.fadeTimer = self.fadeStepFrames
			
					# go to next step
					self.fadeStep += 1
			
		else: # render normally
			# save the rect's height so that it can be passed to player sprite
			self.height = base.HUD_HEIGHT_INACTIVE
			if self.dialogOn or self.drawTextColor > 0:
				self.height = base.HUD_HEIGHT_ACTIVE
			surface.fill((0,0,0),(0,h-self.height,w,h))
		
		# Draw the courage image and percentage text
		cpercent = float(self.vid.player.courage) / base.MAX_COURAGE_POINTS
		cipos = (3,3)
		surface.set_clip((cipos,(self.courageImg.get_width()*cpercent,self.courageImg.get_height())))
		surface.blit(self.courageImg, cipos)
		surface.set_clip()
		base.drawText (surface, 10, str(int(cpercent*100)) + "%", cipos)

		#pygame.draw.arc(surface, (255,255,255), (0,0,100,100), 0, pi, 3)

		#base.drawText (surface, 20, "Press ESC to pause", (20, 20))
		x = 15
		base.drawText (surface, 28, str(self.vid.num_bibles), (x, h-h/7))
		surface.blit (self.vid.images['bible'][0], (x,h-h/8+25))
		
		x += 55
		base.drawText (surface, 28, str(base.numBananas), (x, h-h/7))
		surface.blit (self.vid.images['bananas'][0], (x,h-h/8+25))
		

		self.frame += 1

		if (not self.vid.paused):

			# the idea here is to fade out the text so that it fades out more quickly when it becomes unreadable 
			self.drawTextColor -= int((INITIAL_TEXT_ALPHA * 4) / (self.drawTextColor + 1))		
			
			if (self.drawTextColor < 0):
				self.drawTextColor = 0

		if (self.drawTextColor > 0):

			if (self.vid.paused):
				self.move_cursor()
			
			min = self.line - 3
			max = min + 3

			if (min < 0):
				min = 0
			if (max > len(self.text_lines)):
				max = len(self.text_lines)

			for line_num in range(min, max + 1):
				if (self.line != line_num):
					draw_text = self.text_lines[line_num]
				else:
					draw_text = self.text_lines[line_num][0:self.cursor]
			
					if ((((self.frame / 10) % 2) == 0) and self.vid.paused): # Only add the blinky cursor if it's paused.
						draw_text += "_"
				
				if (len(draw_text) > 0):
					## Trim off the special character
					if (draw_text[0] == '\t'):
						draw_text = draw_text[1: len(draw_text)]

				base.drawTextColored (surface, 24, draw_text, (w/8, (h-h/4) + (line_num - min) * 30), (self.drawTextColor, self.drawTextColor, self.drawTextColor))

			if (self.vid.paused):
				# If we are waiting for the user to press a key...
				if (self.wait_for_next or ((self.line >= (len(self.text_lines) - 1)) and (self.at_end_of_line()))):
					# This code makes the "Press any key to continue..." text fade in and out -- I'm not sure how much I like it yet.				
					self.press_any_key_color += 2
					if (self.press_any_key_color > 127):
						self.press_any_key_color = 127

					drawColor = (self.press_any_key_color, self.press_any_key_color, self.press_any_key_color)

					# This code makes it fade in and out if the above code is set to cycle it between 0 and 255.
	#				if (self.press_any_key_color > 127):
	#					drawColor = (255 - self.press_any_key_color, 255 - self.press_any_key_color, 255 - self.press_any_key_color)

					base.drawTextColored (surface, 12, "Press any key to continue...", (w/8, (h-h/4) + (4) * 30 + 6), drawColor)
				else:
					self.press_any_key_color = 0				

	## show_dialog() pauses the game and displays a message.
	def show_dialog(self, message, callback = None):
		# self.text_lines = message.splitlines() -- had to comment this out because translators can't be counted on to split their own dialog lines properly.
		self.text_lines = self.split_message_lines(message); # We use our own splitlines() function so that we can split on the screen width rather than just \n
		self.drawTextColor = INITIAL_TEXT_ALPHA
		self.cursor = 0
		self.line = -1
		self.next_line();
		self.press_any_key_color = 0
		
		self.dlgCallback = callback
		
		self.dialogOn = 1

		## this was commented out because it did not work well to skip the text when fading in/out
		# if we are testing don't pause the game for the dialog, just print the text
		#if base.Testing:
		#	 print message
		#else:
		self.vid.paused = 1
		
	# add dialog message that will be displayed on demand
	def add_pending_dialog(self, message, callback = None):
		self.pendingDlgs.append((message,callback,time.time()))
		# simply reset the timer to allow the marker to appear again on new messages
		self.talkMarkerTimer = 0
		
	def show_pending_dialog(self):
		if self.dialogOn == 1 or len(self.pendingDlgs) == 0:
			return
					
		self.show_dialog(self.pendingDlgs[0][0],self.pendingDlgs[0][1])
		self.pendingDlgs.pop(0)		
				
		
	def fade_in_out(self,times,callbacks):
		if(len(times) != 3): raise "fade_in_out takes three times in an array"
		self.fadeTimes = times
		self.fadeStep = 1
		self.fadeStepFrames = times[0] * base.FPS
		self.fadeTimer = self.fadeStepFrames
		self.fadeCallbacks = callbacks
		

	
	## This is called to explicitly move the dialog to the next line (if waiting for input), or to just hurry things along
	def next(self):
		if not self.dialogOn:
			return
			
		if self.wait_for_next:
			self.wait_for_next = 0
		else:
			if ((self.line >= (len(self.text_lines) - 1)) and (self.at_end_of_line())): ## if there is no text waiting to be drawn, then unpause
				self.vid.paused = 0
				self.dialogOn = 0
				# call the assigned function if it's set
				if self.dlgCallback != None:
					self.dlgCallback(self.vid) # vid is the level
			else:
				if (self.at_end_of_line()):
					self.next_line()
				else:
					self.move_to_end_of_line()

	## Public method, meant to easily pause the game. Just a shortcut to show_dialog()
	def pause(self):
		self.show_dialog("Paused...\nF10 quits.")

	## Increments the cursor. When it reaches the end of a line, it will attempt to move to the next one.
	def move_cursor(self):
		if not self.wait_for_next:
			if (self.at_end_of_line()):
				self.next_line()
			else:
				if base.SOUND:
					base.sound.Play("pop1");
				self.cursor += 2

	## Moves the cursor to the next line
	def next_line(self):
		self.line += 1
		if (self.line > (len(self.text_lines) - 1)): ## If we're at the end of the lines
			self.line = len(self.text_lines) - 1
			self.move_to_end_of_line()
		else:
			if base.SOUND:
				base.sound.Play("pop2");
			self.cursor = 0
			if (len(self.text_lines[self.line]) > 0):
				## If we hit the special tab character,
				if (self.text_lines[self.line][0] == '\t'):
					## Wait for the user to explicitly give input
					self.wait_for_next = 1

	def at_end_of_line(self):
		return (self.cursor >= len(self.text_lines[self.line]))

	def move_to_end_of_line(self):
		self.cursor = len(self.text_lines[self.line])
	
	# This is our own custom split lines function so that we can check the rendered line width and split extra lines if necessary - questions can be sent to Clint
	def split_message_lines(self, message):
		retVal = []
		nextLine = []
		# Put a space on the right side of each special character
		m = message.replace('\t', ' \t')
		m = message.replace('\n', '\n ')
		
		# Now that we have prepared our message, we get all of the words split (we'll recombine below)
		words = m.split(' ')

		#print "Message =", message
		#print "m =", m
		#print "words =", words

		while(len(words) > 0): # Continue processing until we have no more words to process
			lineDone = False
			currentLine = [words.pop(0)]
			
			while( not lineDone ):
				if currentLine[len(currentLine)-1].endswith('\n'):
					lineDone = True
				else:
					if (len(words) == 0):
						lineDone = True
					else:
						if (base.getTextRenderWidth(24, " ".join( currentLine + words[0:1] ) ) > (base.SCREEN_WIDTH * 7 / 8)):
							lineDone = True
						else:
							currentLine.append(words.pop(0))

			#print "Created line '", currentLine
			retVal.append( " ".join( currentLine ) )
			
		return retVal
