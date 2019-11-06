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
        self.color = (255,255,255)
        self.size = 50
        self.disp = disp
        self.sx = disp.get_width()
        self.sy = disp.get_height()
        self.score = 0
        if x < 320:
            self.initLeft()
        else:
            self.initRight()

    def initLeft (self):
        print ("[IL]")
    def initRight(self):
        print ("[IR]")

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
        if self.score > 3:
         #   text = font.render("GAME OVER", 1, (200, 200, 200))
         #   self.disp.blit(text, (240, 200))
            gameover = True
#            coms.sendGameOver()

    def changey (self, dy):
        global coms
        if gameover:
            return
        self.posy = self.posy + dy         # New y position, centre of the paddle
        if self.posy<self.size:                # Bumper at the top of the screen
            self.posy = self.size
        if self.posy>(self.sy-self.size):      # Bumper at the bottom
            self.posy = self.sy-self.size
#        coms.sendNewPos (self.posx, self.posy)



# This class represents the ball in the pong game. It has a position and speed,
# a color, and a size. It also needs to know about the two paddles and the display.
class ballobj:
    def __init__ (self, disp, l, r):
        global coms
        self.posx = 200              # Current position is (posx, posy)
        self.posy = 300
        self.speed = 1               # Current overall speed
        self.dx = 1                  # Current chane in x and y each frame
        self.dy = 1
        self.disp = disp             # The display
        self.size = 5                # Size of the ball
        self.color = (255,255,255)   # Color of the ball
        self.countdown = -1          # Reamining delay (frames) after score
        self.resetDelay = 200        # Total delay after score
        self.sx = disp.get_width()   # size of the display.
        self.sy = disp.get_height()
        self.left = l                # The left paddle (class instance)
        self.right = r               # Right paddle (class instance)
#        coms.initBall (self.posx, self.posy, self.dx, self.dy)  # Transmit initialization to clients

    def draw (self):                 # Draw the ball at the current position
        pygame.draw.circle (self.disp, self.color, (int(self.posx), int(self.posy)), self.size, 0)

    def move (self):                 # Move the ball one step. Check collisions
        global coms
        if gameover:
            return
        if self.countdown > 0:       # delay after a score
            self.countdown -= 1
            return
        if self.countdown == 0:
            self.posx = 240
            self.posy = random.random ()*100 + 200
            self.countdown = -1

        self.posx = self.posx + self.dx
        self.posy = self.posy + self.dy
        if self.posx > self.sx:          # bounce off of the wall
            self.left.score += 1
            self.countdown = self.resetDelay
#            coms.sendScore (self.left)
        if self.posx < 0:
            self.right.score += 1
            self.countdown = self.resetDelay
#            coms.sendScore(self.right)
        if self.posy > self.sy:
            self.posy = self.sy
            self.dy = -self.dy
        if self.posy < 0:
            self.posy = 0
            self.dy = -self.dy

        if self.collision():             # Paddle collision?
            self.dx = self.dx + (random.random ()-0.5)*0.2   # A slight change after bouncing
            self.dy = self.dy + (random.random ()-0.5)*0.2
            d = math.sqrt (self.dx*self.dx + self.dy*self.dy)
            self.dx = (self.dx/d)*self.speed
            self.dy = (self.dy/d)*self.speed
#        coms.sendNewPos(self.posx, self.posy)                # Send new posdition to client/server

    def collision (self):                # Does the ball collide with a paddle?
        if self.posx <= self.left.posx and self.posy<self.left.posy+self.left.size \
                  and self.posy>self.left.posy-self.left.size:
            if self.posx < self.left.posx-2:
                return False
            self.dx = -self.dx
            return True

        if self.posx >= self.right.posx and self.posy<self.right.posy+self.right.size and \
                  self.posy>self.right.posy-self.right.size:
            if self.posx > self.right.posx+2:
                return False
            self.dx = -self.dx
            return True
        return False

    def sendNewPos(self):                # Send ball position
        print("[B", self.posx, self.posy, "]")

    def sendScore (self, paddle):
        if paddle.posx < 320:
            print("[LS ", paddle.score, "]")
        else:
            print ("[RS ", paddle.score, "]")

class communications:
    def __init__ (self, kind):
        print ("Communication initialize")
        self.PPOS = 1
        self.BPOS = 2
        self.DESI = 0
        self.GOAL = 4
        self.OVER = 8
        self.cs = kind
        self.HOST = "192.168.1.134"
        self.PORT = 9999
        if kind == 0:   # This is a server
            self.initServer()
        else:           # this is a client
            self.initClient()

    def initServer (self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # create a socket object
        serversocket.setblocking(0)
        host = socket.gethostname()          # get local machine name
        port = 9999
        serversocket.bind((host, port))      # bind to the port
        connection_list = []
        serversocket.listen(2)              # queue up to 2 requests
        self.client = host

    def initClient (self):
        self.client = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect ( (HOST, PORT) )

    def readf(self, s):
        msg = "error "
        try:
            msg = s.recv(8)
        except socket.error as err:
            if err == socket.errno.EAGAIN or err == socket.errno.EWOULDBLOCK:  # No data
                return ""
            else:
                print(err)
                return msg  # an error occurred
        else:
            return msg  # Data was received

    def makeMessage(code, p1, p2):
        return '{:02d}{:03d}{:03d}'.format(code, p1, p2)

    def getMessage(s):
        code = s[0:2]
        p1 = s[2:5]
        p2 = s[5:8]
        return ([int(code)], [int(p1)], [int(p2)])

    def sendBPOS(self, x, y):                # Send ball position
        client.send(makeMessage(BPOS, x, y))
    def sendScore (self, lscore, rscore):
        client.send (makeMessage(GOAL, lscore, rscore))
    def sendPPos(self, x):
        client.send(makeMessage(PPOS, x, 0))
    def sendGameOver(self):
        client.send(makeMessage(OVER, 0, 0))
    def sendDesi (self, k):
        client.send(makeMessage(DESI, k, 0))

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((640, 480), pygame.SRCALPHA, 32)

coms = communications(0)
pleft = paddle (display, 100, 240)
pright = paddle (display, 540, 240)
ball = ballobj(display, pleft, pright)

gameover = False
background = pygame.image.load("background.png")
rup = False
rdown = False
lup = False
ldown = False
while True:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          exit()
      if event.type == pygame.KEYDOWN:       # Right paddle
          if event.key == pygame.K_UP:
              rup = True
          if event.key == pygame.K_DOWN:
              rdown = True
          if event.key == pygame.K_w:
              lup = True
          if event.key == pygame.K_s:
              ldown = True
      if event.type == pygame.KEYUP:        # Left paddle
          if event.key == pygame.K_w:
              lup = False
          if event.key == pygame.K_s:
              ldown = False
          if event.key == pygame.K_UP:
              rup = False
          if event.key == pygame.K_DOWN:
              rdown = False

  if rup:                                 # Move right if needed
        pright.changey(-1)
#        coms.sendNewPos (pright.posx, pright.posy)
  if rdown:
        pright.changey(1)
 #       coms.sendNewPos (pright.posx, pright.posy)
  if lup:                                 # Move left if needed
        pleft.changey(-1)
 #       coms.sendNewPos(pleft.posx, pleft.posy)
  if ldown:
        pleft.changey(1)
 #       coms.sendNewPos(pleft.posx, pleft.posy)

  display.blit (background, (0,0))        # Display the background
  pleft.draw()                            # Draw the left paddle
  pright.draw()                           # Draw the right paddle
  ball.draw()                             # Draw the ball
  ball.move()                             # Move the ball
  pygame.display.update()                 # Refresh the screen
