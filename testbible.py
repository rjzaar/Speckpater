from __future__ import print_function

my_file = open('bible.txt', 'r')
verse = "TEST"
while (verse[:3] != "end"):
    verse = my_file.readline()
    print(verse)
