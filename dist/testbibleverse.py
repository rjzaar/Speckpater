from __future__ import print_function
from builtins import range
from bibleverse import *

mybible = bibleverse("easy")
for i in range(5):
    verse = mybible.getverse()
    print(verse[0], verse[1], verse[2])
