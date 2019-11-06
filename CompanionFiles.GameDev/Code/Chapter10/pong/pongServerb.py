import pygame
import random
import math
import socket
import time
import select

class paddle:
    def __init__(self, x, y, client):
        self.posx = x     # 100 for left 540 for right
        self.posy = y     # 240, the centre
        self.size = 50
        self.sx = 640
        self.sy = 480
        self.client = client
        self.score = 0

    def changey (self, dy):
        if gameover:
            return
        if dy < self.size:                # Bumper at the top of the screen
            self.posy = self.size
        elif dy>(self.sy-self.size):      # Bumper at the bottom
            self.posy = self.sy-self.size
        else:
            self.posy = dy  # New y position, centre of the paddle

# This class represents the ball in the pong game. It has a position and speed,
# a color, and a size. It also needs to know about the two paddles and the display.
class ballobj:
    def __init__ (self, disp, l, r):
        global coms
        self.posx = 200              # Current position is (posx, posy)
        self.posy = 300
        self.speed = 5               # Current overall speed
        self.dx = 4                  # Current chane in x and y each frame
        self.dy = 4
        self.disp = disp             # The display
        self.size = 5                # Size of the ball
        self.color = (255,255,255)   # Color of the ball
        self.countdown = -1          # Reamining delay (frames) after score
        self.resetDelay = 50        # Total delay after score
        if disp != None:
          self.sx = disp.get_width()   # size of the display.
          self.sy = disp.get_height()
        else:
            self.sx = 640
            self.sy = 480
        self.left = l                # The left paddle (class instance)
        self.right = r               # Right paddle (class instance)
#        coms.initBall (self.posx, self.posy, self.dx, self.dy)  # Transmit initialization to clients

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
        if self.posx > 560:         # bounce off of the wall
            self.left.score += 1
            self.countdown = self.resetDelay
        if self.posx < 50:
            self.right.score += 1
            self.countdown = self.resetDelay
            self.posy = self.sy
            self.dy = -self.dy
        if self.posy < self.size/2:
            self.posy = self.size/2+1
            self.dy = -self.dy
        if self.posy > 480-self.size/2:
            self.posy = 480-self.size/2
            self.dy = -self.dy
        if self.collision():             # Paddle collision?
            self.dx = self.dx + (random.random ()-0.5)*0.2   # A slight change after bouncing
            self.dy = self.dy + (random.random ()-0.5)*0.2
            d = math.sqrt (self.dx*self.dx + self.dy*self.dy)
            self.dx = (self.dx/d)*self.speed
            self.dy = (self.dy/d)*self.speed

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

def makeMessage(code, p1, p2):
    return '{:02d}{:03d}{:03d}'.format(code, p1, p2)

def getMessage(s):
    try:
      code = s[0:2]
      p1 = s[2:5]
      p2 = s[5:8]
      return (int(code), int(p1), int(p2))
    except:
        abort()
    return None

def readMessage (client):
    m = client.recv(8)
    if m == b'':
        abort()
    else:
        return getMessage (m)

def sendBPos(client, x, y):                # Send ball position
    client.send(bytes(makeMessage(BPOS, x, y), 'utf-8'))

def sendScore (client, lscore, rscore):
        client.send (bytes(makeMessage(GOAL, lscore, rscore), 'utf-8'))

def sendPPos(client,  x):
    global PPOS, ws
    client.send(bytes(makeMessage(PPOS, x, 0), 'utf-8'))
    if client==ls:
        k = 0
    else:
        k = 1

def sendGameOver(client):
        client.send(bytes(makeMessage(OVER, 0, 0), 'utf-8'))

def sendDesi (client, k):
        client.send(bytes(makeMessage(DESI, k, 0), 'utf-8'))

def abort ():
    print ("Abort server - client has shut down.")
    exit ()

def netInit():
    global serversocket
    print("Communication initialize")
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket object
    host = socket.gethostname()  # get local machine name
    port = 9999
    serversocket.bind((host, port))  # bind to the port
    serversocket.listen(2)  # queue up to 2 requests
    print("Server listening...")

def getPlayers():        # Try to connect to two players (clients)
    global ls, rs, serversocket

    print ("Waiting for left player.")
    while True:          # Open the left client
        try:
            ls,laddr = serversocket.accept()
        except:          # Failed
            time.sleep (1)
            continue
        print ("Left player is in.")
        sendDesi(ls, 0)  # Tell the client it is the left player
        break

    print ("Waiting for right player")
    while True:    # Open the right client
        try:
            rs,raddr = serversocket.accept()
        except:
            time.sleep (1)
            continue
        print ("Right player is in.")
        sendDesi (rs, 1)  # Tell the client it is the right player
        break
    return

PPOS = 1       # Message codes
BPOS = 2
DESI = 0
GOAL = 4
OVER = 8
rs = None      # Right and left clients
ls = None
HOST = "192.168.1.168"
PORT = 9999
gameover = False
background = pygame.image.load("background.png")

serversocket = None
pygame.init()
clock = pygame.time.Clock()
display = None

netInit()
getPlayers()                             # Wait for players to connect
pleft = paddle (100, 240, ls)   # Create left player paddle
pright = paddle (540, 240, rs)  # Create right player paddle
ball = ballobj(display, pleft, pright)   # Create the ball.
wstr = ["Left", "Right"]

while True:
    clock.tick(50)
    for event in pygame.event.get():   # Only event should be QUIT.
        if event.type == pygame.QUIT:
            exit()

# ------------------ Get Paddle positions ------------------------------------
    m1 = readMessage(rs)  # Read  paddle message sent by RIGHT client.
    pright.changey(m1[1])  # Also change the position of the paddle
    m1 = readMessage(ls)           # Read  paddle message sent by Left client.
    pleft.changey(m1[1])          # Also change the position of the paddle

# --------------------------- Move ball, send position ---------------------------------
    ball.move()  # Move the ball
    sendBPos(ls, int(ball.posx), int(ball.posy))
    sendBPos(rs, int(ball.posx), int(ball.posy))

# ----------------------------- Send paddle pos to clients -----------------------------
    ls.send(bytes(makeMessage(PPOS, pleft.posy, pright.posy), 'utf-8'))
    rs.send(bytes(makeMessage(PPOS, pleft.posy, pright.posy), 'utf-8'))

# ----------------------------- Send score to both clients -----------------------------
    sendScore(ls, pleft.score, pright.score)
    sendScore (rs, pleft.score, pright.score)
