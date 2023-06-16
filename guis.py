from builtins import str
import base
import pygame
import re
from pygame.locals import *
from pgu import gui, html, tilevid


class SelectLevelDialog(gui.Dialog):

    def __init__(self, level):
        self.level = level

        title = gui.Label("Jump to level")

        doc = gui.Document()

        table = gui.Table()

        # table.td(gui.Label("select level"),colspan=1)

        table.tr()

        # dont set the current as default since it could be the testlevel
        # levname = level.__class__.__module__.split(".")[1]
        levname = ""

        sel = gui.Select(levname, width=150)

        self.sel = sel

        # sel.add("test level","testlevel")
        ## use the import to see what level scripts are available
        ## and add the script filenames to list

        i = j = 1

        while True:
            levelName = "gamelevel" + str(i) + "_" + str(j)

            # this is bit rough way to find out the level scripts
            try:
                exec("from levels import " + levelName)

                sel.add(levelName, levelName)
                j += 1
            except ImportError as err:
                error = str(err)
                pattern = re.compile(rf"cannot import name '{levelName}' .*")
                match = pattern.match(error)
                # filter the other import errors
                if not match:
                    raise BaseException("excepted import error from level script " + levelName + ": " + str(err))
                j = 1
                i += 1

                if i > 72: break

        table.add(sel, colspan=1)
        table.tr()

        selButton = gui.Button("Jump")
        selButton.connect(gui.CLICK, self.onSelect, None)

        table.add(selButton, colspan=1)

        doc.add(table)

        gui.Dialog.__init__(self, title, doc)

    def onSelect(self, value):
        if len(self.sel.value) > 0:
            self.level.nextState = base.GOTOLEVEL
            self.level.gotoLevelName = self.sel.value

        # self.close()
        toggleSelectLevelDialog(self.level)


def toggleSelectLevelDialog(level):
    if level.levelSelDlg.isVisible == True:
        level.guiCont.remove(level.levelSelDlg)
        level.levelSelDlg.isVisible = False
    else:
        level.guiCont.add(level.levelSelDlg, 0, 0)
        level.levelSelDlg.isVisible = True
