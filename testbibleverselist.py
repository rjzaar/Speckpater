from __future__ import print_function
from builtins import range
from bibleverse import *

mybible = bibleverse()
mybible.shuffle()

for i in range(10):
    verse = mybible.verselist(i)
    print(verse)
