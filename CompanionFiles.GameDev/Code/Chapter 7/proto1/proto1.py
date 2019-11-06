import pygame
import math

class button:

    def __init__ (self, x, y, w, h):
        self.posx = x
        self.posy = y
        self.width = w
        self.height = h
        self.text = ""
        self.size = 34
        self.font = None
        self.color = (255, 255, 0)
        self.col = self.color
        self.armed = (255,0,0)
        self.family = None

    def setText (self, t):
        self.text = t

    def isArmed (self):
        t = pygame.mouse.get_pos()
        xx = t[0]
        yy = t[1]
        if self.posx <=xx and (self.posx+self.width)>=xx and \
           self.posy<=yy and   (self.posy+self.height)>=yy:
            return True
        return False

    def draw (self):
        if self.isArmed():
            self.col = (self.armed[0], self.armed[1], self.armed[2])
        else:
            self.col = (self.color[0], self.color[1], self.color[2])
        self.drawText (self.text, self.posx+4, self.posy+self.height-2)

    def setfont(s):
            global family, size
            font = pygame.font.SysFont(self.family, self.size)

    def textsize(self, n):
            global family, size, weight, font
            self.size = n
            font = pygame.font.SysFont(self.family, self.size)

    def drawText(self, s, x, y):
            global display, font

            if self.font == None:  # Create a font if needed
                self.font = pygame.font.Font(self.family, self.size)
            text = self.font.render(s, 1, self.col)  # Render the string in the fill color
            textpos = text.get_rect()  # Get the rectangle that encloses the text
            textpos.bottomleft = [x, y]
            display.blit(text, textpos)

    def setcolor(r, g=1000, b=1000, a=255):
        if g == 1000:
            self.color = (r, r, r, a)
        else:
            self.color = (r, g, b, a)

    def setarmed(r, g=1000, b=1000, a=255):
        if g == 1000:
            self.armed = (r, r, r, a)
        else:
            self.armed = (r, g, b, a)


def startScreen (ev):
    global screenState, PLAYSTATE, OPTIONSTATE, ENDSTATE
    display.blit(startImage, (0, 0))
    playButton.draw()
    if ev.type == pygame.MOUSEBUTTONUP and playButton.isArmed():
        screenState = PLAYSTATE
        playScreen(ev)
        return
    optionButton.draw()
    if ev.type == pygame.MOUSEBUTTONUP and optionButton.isArmed():
        screenState = OPTIONSTATE
        optionScreen(ev)
        return
    quitButton.draw()
    if ev.type == pygame.MOUSEBUTTONUP and quitButton.isArmed():
        screenState = ENDSTATE

def optionScreen (ev):
    global screenState, STARTSTATE, soundOn
    display.blit (optionImage, (0,0))
    soundButton.draw()
    if ev.type == pygame.MOUSEBUTTONUP and soundButton.isArmed():
        if soundOn:
            soundOn = False
            soundButton.setText("No")
            display.blit(optionImage, (0, 0))
            soundButton.draw()
        else:
            soundOn = True
            soundButton.setText ("Yes")
            display.blit(optionImage, (0, 0))
            soundButton.draw()
    backButton.draw()
    if ev.type == pygame.MOUSEBUTTONUP and backButton.isArmed():
        screenState = STARTSTATE
        startScreen(ev)


def playScreen (event):
    global x, y
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_s:
        if (y<2300):  # 1350 size = 950 max
            y = y + 10
      if event.key == pygame.K_w:
        if (y>10):
            y = y - 10
      if event.key == pygame.K_a:
          if (x > 10):
              x = x - 10
      if event.key == pygame.K_d:
          if (x < 2700):   #1600 size = 1100 max
              x = x + 10
    display.blit(background, (-x, -y))
    display.blit (boat2, (xx, yy))

def endScreen(event):
    display.blit(endImage, (0,0))
    if event.type == pygame.MOUSEBUTTONUP :
        exit()

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((500, 400), pygame.SRCALPHA, 32)
# print (pygame.image.get_extended())

background = pygame.image.load ("finall.png")
boat2 = pygame.image.load ("boat4.gif")
startImage = pygame.image.load ("startScreen.jpg")
optionImage = pygame.image.load ("optionsScreen.jpg")
endImage = pygame.image.load ("endScreen.jpg")

pygame.key.set_repeat(10, 200)
x = 800
y = 100
xx = 100
yy = 200
soundOn = True
STARTSTATE = 0
OPTIONSTATE = 1
PLAYSTATE = 2
ENDSTATE = 3
screenState = STARTSTATE
playButton = button (100, 200, 100, 30)
playButton.setText ("Play")
optionButton = button (300,250,100, 30)
optionButton.setText ("Options")
quitButton = button (100, 300, 100, 30)
quitButton.setText ("Quit")
soundButton = button (200, 135, 100, 30)
soundButton.setText ("Yes")
backButton = button (200, 300, 100, 30)
backButton.setText ("Back")

while True:
  for event in pygame.event.get():
      if screenState == STARTSTATE:
          startScreen (event)
      elif screenState == OPTIONSTATE:
          optionScreen (event)
      elif screenState == PLAYSTATE:
          playScreen (event)
      elif screenState == ENDSTATE:
          endScreen (event)
      else:
          print ("ERROR: Bad state in main loop.")
          exit()
  pygame.display.update()

