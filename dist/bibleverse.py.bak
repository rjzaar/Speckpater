# This program gives a set of verses.
import random

TOTALVERSES=38 # Total number of bible verses
EASY=5    #number of bible verses to use each game.
MEDIUM=10
HARD=25

class bibleverse:
	def __init__(self, difficulty):
		#load all verses into the file of verses
		f = open('bible.txt', 'r')
		self.verses = []
		self.totalverses = []
		for i in range(TOTALVERSES):
			self.totalverses.append(f.readline())
		f.close()
		self.diffnum=0
		self.damaged = False
		random.shuffle(self.totalverses)
		if difficulty=="easy":
			self.diffnum=EASY
		elif difficulty=="medium":
			self.diffnum=MEDIUM
		elif difficulty=="hard":
			self.diffnum=HARD
		self.verses = self.totalverses[:self.diffnum]		
		
	def getverse(self):
		self.damaged = False
		idam = random.random()
		if idam<0.3:
			self.damaged = True
		ranword=""
		
			
		retval = (self.verses[int(random.random()*self.diffnum)])
		if self.damaged:
			#blank out words
			sv=retval.split()
			ranwordnum = int(random.random()*len(sv))
			ranword = sv[ranwordnum]
			sv[ranwordnum]="_"*len(ranword)
			retval=" ".join(sv)
		return (retval,self.damaged,ranword)
	def verselist(self,num):
		return (self.verses[num])
	
		

