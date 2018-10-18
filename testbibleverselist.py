from  bibleverse import *


mybible = bibleverse()
mybible.shuffle()

for i in range(10):
    verse = mybible.verselist(i)
    print verse
    