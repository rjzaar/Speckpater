import pygame
from pygame.locals import *
import gui


screen = pygame.display.set_mode(
    (640, 480), FULLSCREEN  ) # try adding DOUBLEBUF | HWSURFACE 
# pygame.mouse.set_visible(0)


app = gui.App()
c = gui.Container(width=640,height=480)


##
## dialog 1
##

t1 = gui.Table()
t1.tr()
t1.add(gui.Label("Gal Test"))

t2 = gui.Table()

t2.tr()
t2.add(gui.Label("Gui Widgets"))
t2.add(gui.Input())

t2.tr()
t2.add(gui.Label("Button"))
t2.add(gui.Button("Click Me!"))

d1 = gui.Dialog(t1, t2)
c.add(d1, 50, 150)


##
## dialog 2
##

t3 = gui.Table()
t3.tr()
t3.add(gui.Label("Another one"))

t4 = gui.Table()

t4.tr()
t4.add(gui.Label("Name"))
t4.add(gui.Input())

t4.tr()
t4.add(gui.Label("Ohh"))
b1 = gui.Button("OK")
t4.add(b1)

d2 = gui.Dialog(t3, t4)
c.add(d2, 50, 300)


##
## some labels
##

l1 = gui.Label("Suppose this is a menu", color=(255, 255, 255) )
c.add(l1, 50, 50)

l2 = gui.Label("Click <SPACE> to hide top dialog", color=(255, 255, 
255) )
c.add(l2, 50, 75)

l3 = gui.Label("Opps... Did it happen?", color=(255, 255, 255) )

##
## app begins
##


app.init(widget=c,screen=screen)


FRAME_EVT = USEREVENT + 1

pygame.event.Event(FRAME_EVT)

pygame.time.set_timer(FRAME_EVT, 30)


_quit = 0

while _quit == 0:
    event = pygame.event.wait()

    if event.type == FRAME_EVT:
        pygame.display.flip()
        continue
        
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            _quit = 1
            continue
        elif event.key == K_SPACE:
            d1.close()
            c.add(l3, 100, 100)
        
    app._event(event)
    screen.fill((0,0,0))
    app.paint(screen)

