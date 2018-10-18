
import os
import base
import platform

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

REQUIRED_FIELDS = "There's four required file names for: level tga, tileset, trigger and background."

def loadLevelFile(filename):
	f = None
	fn = os.path.join('levels',filename + ".lev")
	try:
		f = file(fn)
	except IOError:
		raise base.ResourceException("Cannot load level file \"" + fn + "\"")
	lines = f.readlines()
	if(len(lines) != 4):
		raise Exception("Invalid level file, the line count does not match four.",
		REQUIRED_FIELDS,
		"When the file has these lines:",lines)
		
	for i in range(0,len(lines)):
		if platform.system() == 'Windows':
			lines[i] = lines[i].strip("\n")
		elif platform.system() == 'Linux':
			lines[i] = lines[i].strip("\r\n") #assuming the files are save in Windows text
				
	f.close()
	return lines
	
def saveLevelFile(filename,data):
	if(len(data) != 4):
		raise Exception("missing data fields for saving level file.",
		REQUIRED_FIELDS,
		"When save data has these fields:",data)
		
	f = file(os.path.join('levels',filename + ".lev"),"w")
	for d in data:
		f.write(d + "\n")
	f.close()
	
