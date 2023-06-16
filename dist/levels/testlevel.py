from __future__ import division
from __future__ import print_function
from past.utils import old_div
import basegamelevel
from pgu import tilevid


class GameLevel(basegamelevel.GameLevel):
    # these should be set even though this is just a test level
    level_maj = 1
    level_min = 1

    blockArrayOne = []

    def OnRunSpecial8(self, g, t, a):
        self.blockArrayOne.append(copy.copy(t))  # Append each block to the list of blocks
        self.removeBlocks(blockArrayOne)

    def addBlocks(self, blocks):
        for currTile in blocks:
            game.tlayer[old_div(currTile.rect.y, TILE_SIZE)][old_div(currTile.rect.x, TILE_SIZE)] = currTile

    def removeBlocks(self, blocks):
        for currTile in blocks:
            game.tlayer[old_div(currTile.rect.y, TILE_SIZE)][old_div(currTile.rect.x, TILE_SIZE)] = copy.copy(
                game.tlayer[0][0])

    def OnStart(self):
        print("on start")

    def OnRunSpecial1(self, g, t, a):
        def special_hit1(g, s, a):
            print("trigger 1")
            s.agroups = None  ## Remove the groups from colliding with this object in the future

        s = tilevid.Sprite(g.images['blank'], t.rect)
        g.sprites.append(s)
        s.agroups = g.string2groups('player')  ## Set the 'player' group to collide with this object
        s.hit = special_hit1

    def OnRunSpecial2(self, g, t, a):
        print("trigger 2")

    def OnRunSpecial3(self, g, t, a):
        print("trigger 3")

    def OnRunSpecial4(self, g, t, a):
        print("trigger 4")

    def OnRunSpecial5(self, g, t, a):
        print("trigger 5")

    def OnRunSpecial6(self, g, t, a):
        print("trigger 6")

    def OnRunSpecial7(self, g, t, a):
        print("trigger 7")

    def OnExit(self):
        print("on exit")
