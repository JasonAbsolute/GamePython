import pygame
import random
import math
import socket
import time
import select

class paddle:
    def __init__(self, disp, x, y):
        self.posx = x     # 100 for left 540 for right
        self.posy = y     # 240, the centre
        self.size = 50
        self.disp = disp
        self.sx = disp.get_width()
        self.sy = disp.get_height()
        self.score = 0
        self.color = pygame.Color(255,255,255)
        if x < 320:
            self.side = 0
        else:
            self.side = 1

    def draw (self):
        global coms, gameover
        pygame.draw.line (self.disp, self.color, (self.posx, self.posy), (self.posx, self.posy-self.size),3)
        pygame.draw.line (self.disp, self.color, (self.posx, self.posy), (self.posx, self.posy+self.size),3)
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.score), 1, (100, 100, 100))
        if self.posx<320:
            self.disp.blit (text, (100, 40))
        else:
            self.disp.blit(text, (550, 40))
        if gameover:
            text = font.render("GAME OVER", 1, (200, 200, 200))
            self.disp.blit(text, (240, 200))
            return
        
    def sety (self, y):
        self.posy = y
        
    def changey (self, y):
        self.posy += y

# This class represents the ball in the pong game. It has a position and speed,
# a color, and a size. It also needs to know about the two paddles and the display.
class ballobj:
    def __init__ (self, disp, l, r):
        global coms
        self.posx = 200              # Current position is (posx, posy)
        self.posy = 300
        self.disp = disp             # The display
        self.size = 5                # Size of the ball
        self.color = (255,255,255)   # Color of the ball
        self.sx = disp.get_width()   # size of the display.
        self.sy = disp.get_height()
        self.left = l                # The left paddle (class instance)
        self.right = r               # Right paddle (class instance)
#        coms.initBall (self.posx, self.posy, self.dx, self.dy)  # Transmit initialization to clients

    def draw (self):                 # Draw the ball at the current position
        pygame.draw.circle (self.disp, self.color, (int(self.posx), int(self.posy)), self.size, 0)

    def move (self, x, y):           # Move the ball to a position.
        global coms
        if gameover:
            return
        self.posx = x
        self.posy = y

class communications:
    def __init__ (self):
        print ("Communication initialize")
        self.PPOS = 1
        self.BPOS = 2
        self.DESI = 0
        self.GOAL = 4
        self.OVER = 8
        self.HOST = "192.168.1.168"
        self.PORT = 9999
        self.svr = None
        self.side = 0
        self.initClient()

    def initClient (self):
        self.svr = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.svr.connect ( (self.HOST, self.PORT) )
        m = self.readMessage ()
        ms = self.getMessage (m)
        if ms[1] == self.DESI:
            self.side = 0
        elif ms[1] == 1:
            self.side = 1
            
    def readf(self):      # Returns an ascii string
        msg = "99999999"
        try:
            msg = self.svr.recv(8)
        except socket.error as err:
            if err == socket.errno.EAGAIN or err == socket.errno.EWOULDBLOCK:  # No data
                time.sleep(0.1)
            else:
                print("ERROR: ",err)
                return msg  # an error occurred
        else:
 #           print (msg, type(msg))
            return msg.decode ("utf-8")  # Data was received

    def makeMessage(self, code, p1, p2):
        return '{:02d}{:03d}{:03d}'.format(code, p1, p2)

    def getMessage(self, s):   # Return a tuple
        code = s[0:2]
        p1 = s[2:5]
        p2 = s[5:8]
#        print (code, p1, p2, type(code), type(p1))
        return (int(code), int(p1), int(p2))

    def readMessage (self):  # Return a string
        m = self.readf ()
        if m == "":
            abort()
        else:
            return m

    def sendPPos(self, x, p):
        try:
            self.svr.send(bytes(self.makeMessage(self.PPOS, x, p), 'utf-8'))
        except:
            abort()

def IAMLEFT ():
        if coms.side == 0:
            return True;
        return False;
    
def IAMRIGHT ():
        return not IAMLEFT()

def abort ():
    print ("Server has shut down.")
    exit()

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((640, 480), pygame.SRCALPHA, 32)

coms = communications()       # Set up client communications
pleft = paddle (display, 100, 242)
pright = paddle (display, 540, 240)
ball = ballobj(display, pleft, pright)
if IAMLEFT():
    pleft.color = (0,255, 0)
    print("I AM Left")
else:
    pright.color = (0, 255, 0)
    print ("I AM RIGHT")

    
gameover = False
background = pygame.image.load("background.png")
rup = False
rdown = False
lup = False
ldown = False

while True:
  clock.tick(50)
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          exit()
      if event.type == pygame.KEYDOWN:       # Right paddle
          if event.key == pygame.K_UP:
              rup = True and IAMRIGHT()
          if event.key == pygame.K_DOWN:
              rdown = True and IAMRIGHT()
          if event.key == pygame.K_w:
              lup = True and IAMLEFT()
          if event.key == pygame.K_s:
              ldown = True and IAMLEFT()

      if event.type == pygame.KEYUP:        # Left paddle
          if event.key == pygame.K_w and IAMLEFT():
              lup = False
          if event.key == pygame.K_s and IAMLEFT():
              ldown = False
          if event.key == pygame.K_UP and IAMRIGHT():
              rup = False
          if event.key == pygame.K_DOWN and IAMRIGHT():
              rdown = False

  if rup:                     # Move right paddle if needed
        pright.changey(-3)
  if rdown:
        pright.changey( 3)
  if lup:                     # Move left paddle if needed
        pleft.changey( -3)
  if ldown:
        pleft.changey( 3)

# -----  Send paddle position to the,server ----------
  if IAMLEFT():
    coms.sendPPos (pleft.posy, 0)
  else:
    coms.sendPPos (pright.posy, 1)

# --------------- Get ball position -------------------
  m1 = coms.readMessage()    # m1 is a string
  xlst = coms.getMessage (m1)  # xlst is a tuple
  ball.move(xlst[1], xlst[2])

# ------------ Get other paddle position --------------
  m1 = coms.readMessage()    # m1 is a string
  xlst = coms.getMessage (m1)  # xlst is a tuple
  if IAMLEFT:
      pright.posy = xlst[2]
#      print ("Right paddle now ", pright.posy)
  else:
      pleft.posy = xlst[1]
#      print ("Left paddle now ", pleft.posy)
  pright.posy = xlst[2]
  pleft.posy = xlst[1]
# ------------ Get the score --------------------------
  m1 = coms.readMessage()    # m1 is a string
  xlst = coms.getMessage (m1)  # xlst is a tuple
  pright.score = xlst[2]
  pleft.score = xlst[1]

  display.blit (background, (0,0)) # Display the background

  if pright.score > 3:
      gameover = True
  if pleft.score > 3:
      gameover = True

  pleft.draw()                # Draw the left paddle
  pright.draw()               # Draw the right paddle
  ball.draw()                 # Draw the ball
  pygame.display.update()     # Refresh the screen
