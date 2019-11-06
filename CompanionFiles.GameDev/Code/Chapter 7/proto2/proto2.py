import pygame
import math
import struct

# A button widget......................................................
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

# .............................................................................

# A Waypoint ..................................................................
class waypoint:
    def __init__ (self, x, y, index, speed):
        self.posx = x
        self.posy = y
        self.index = index
        self.speed = speed

# .............................................................................

# A boat ..................................................................
class npc :

    def __init__(self, x, y, sprite, speed, angle, index):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.index = index
        self.sound = False    # Engine sound.
        self.volume = 0
        self.targetSpeed = 0   # How fast does the boat want to go?
        self.targetAngle = 90  # What is the course setting?
        self.sprite = sprite     # The image of the boat
        self.wpt = None        # Next waypoint
        self.name = "NPC 1"
        self.NORMAL = 0
        self.AVOID = 1
        self.COLLIDED = 2
        self.state = self.NORMAL
        self.sensor = -1
        self.ccount = 0

    def setSpeed (self, s):
        self.targetSpeed = s

    def setCourse (self, a):
        self.setAngle = a

    def setWaypoint (self, w):
        self.wpt = w
        self.targetSpeed = w.speed

    def setName (self, s):
        self.name = s

    def adjustAngle (self):
        if self.angle > 360.0:
            self.angle = self.angle - 360
        if self.angle < 0:
            self.angle = self.angle + 360
        if self.angle < self.targetAngle:
            self.angle = self.angle + 1
            if self.angle > self.targetAngle:
                self.angle = self.targetAngle
        elif self.angle > self.targetAngle:
            self.angle = self.angle - 1
            if self.angle < 0:
                self.angle = 0

    def adjustSpeed (self):
        if self.speed < self.targetSpeed:
            self.speed = self.speed + 0.1
            if self.speed > self.targetSpeed:
                self.speed = self.targetSpeed
        elif self.speed > self.targetSpeed:
            self.speed = self.speed - 0.1
            if self.speed < 0:
                self.speed = 0


    def distance (self, a, b):
        return math.sqrt ( (a[0]-b[0])*(a[0]-b[0]) + (a[1]-b[1])*(a[1]-b[1]) )

    def side (self, a, b, c):
        return (a[0]-b[0])*(c[1]-b[1]) - (a[1]-b[0])*(c[0]-b[0])

    def escape (self):
        print ("ESCAPE .......",self.ccount,"sssssss......")
        self.ccount = self.ccount + 1
        self.speed = 1
        if self.ccount < 100:
            return

        if self.sensor == 1:
            self.angle -= 90.0
        elif self.sensor == 0:
            self.angle = self.angle + 45.0
        elif self.sensor == 2:
            self.angle = self.angle - 45.0
        self.sensor = -1
        self.state = self.COLLIDED
        return

    def normalize (self, vec):
        leng = math.sqrt((vec[0]*vec[0])+(vec[1]*vec[1]))
        if leng == 0:
            return (0,0)
        return ( (vec[0]/leng, vec[1]/leng) )

    def boatCollision (self, i, ddx, ddy):
        ul = rotate((boats[i].x, boats[i].y), (boats[i].x - 42, boats[i].y - 13), -boats[i].angle)
        ur = rotate((boats[i].x, boats[i].y), (boats[i].x + 42, boats[i].y - 13), -boats[i].angle)
        lr = rotate((boats[i].x, boats[i].y), (boats[i].x + 42, boats[i].y + 13), -boats[i].angle)
        ll = rotate((boats[i].x, boats[i].y), (boats[i].x - 42, boats[i].y + 13), -boats[i].angle)

        ul = terrain_to_screen(ul)
        ur = terrain_to_screen(ur)
        lr = terrain_to_screen(lr)
        ll = terrain_to_screen(ll)

        # Ray cast forward.
        n = self.normalize((ddx, ddy))  # Make length of velocty vector = 1
        ray = (n[0]*200, n[1] * 200)  # Ray is now 100 pixels long

        pygame.draw.line(display, (0, 255, 0), terrain_to_screen((self.x, self.y)),
                         terrain_to_screen((self.x+ray[0], self.y+ray[1])), 2)

        if line_intersect( terrain_to_screen((self.x, self.y)), terrain_to_screen((self.x+ray[0], self.y+ray[1])),
                           (ul[0], ul[1]), (ur[0], ur[1]) ):
            return True
        if line_intersect( terrain_to_screen((self.x, self.y)), terrain_to_screen((self.x+ray[0], self.y+ray[1])),
                            (ur[0], ur[1]), (lr[0], lr[1]) ):
            return True
        if line_intersect( terrain_to_screen((self.x, self.y)), terrain_to_screen((self.x+ray[0], self.y+ray[1])), (lr[0], lr[1]), (ll[0], ll[1]) ):
            return True
        if line_intersect( terrain_to_screen((self.x, self.y)), terrain_to_screen((self.x+ray[0], self.y+ray[1])), (ll[0], ll[1]), (ul[0], ul[1]) ):
            return True
        self.ccount = 0
        return False


    def avoid (self, i, ddx, ddy):
        print ("Avoiding ")
        self.state = self.AVOID
        force = ((self.x+ddx - boats[i].x), (self.y+ddy - boats[i].y))
        force = self.normalize (force)
        ax = self.x + force[0]*15
        ay = self.y + force[1]*15
        self.targetAngle = math.degrees(math.atan2(ay - self.y, self.x - ax) + math.pi)
        return
#        if force[0] > 0:
#            self.targetAngle -= 10
#       else:
#           self.targetAngle += 10


    def nextStep(self):
        global display, boats

        print ("Boat ", self.index, " TS,TA = ",self.targetSpeed, self.targetAngle, "State: ", self.state, self.angle)

# First, move the boat. Water friction will slow it.
        old = (self.x, self.y)            # Save the previous position
        self.speed = self.speed - 0.001   # Slow down
        if self.speed < 0:                # Can't move backwards
            self.speed = 0
            ddx = 0
            ddy = 0
        else:
            ddx = self.speed * math.cos(math.radians(self.angle))
            ddy = -self.speed * math.sin(math.radians(self.angle))

# Collisions? First with shore
        t = shoreCollide (self.index)
        if t:               # and self.NORMAL:       # Collided just now
#            self.x = old[0]
#            self.y = old[1]
            print ("Shore collision.")
            self.speed = 1.0
            self.escape()
            self.state = self.NORMAL


# Collision with another boat?
        elif self.boatCollision (0, ddx, ddy):
            print ("Collision pending")
            self.avoid(0, ddx, ddy)

        else:
        # Move the boat
          self.x = self.x + ddx  # New boat position on the map is (x, y)
          if self.x > 3200:  # Keep the boat on the play area - Too far right
            self.x = 3199
            self.speed = 0
          elif self.x < 0:  # Keep the boat on the play area - Too far left
            self.x = 1
            self.speed = 0
          self.y = self.y + ddy
          if self.y > 2700:  # Keep the boat on the play area - Too far down
            self.y = 2699
            self.speed = 0
          elif self.y < 0:  # Keep the boat on the play area - Too far up
            self.y = 1
            self.speed = 0
          self.state = self.NORMAL


# Waypoint??
        d = self.distance ((self.x, self.y), (self.wpt.posx,self.wpt.posy))
        if  d < 30: # Arrived at waypoint?
            print ("Arrived at ", self.wpt.index)
            k = self.wpt.index+2
            if (k>29):
                k = 28
            self.wpt = waypoints[k]

# Adjust speed and angle
        self.adjustSpeed ()
        self.adjustAngle()

# Steer
        if self.wpt != None and self.state == self.NORMAL:
            self.targetAngle = math.degrees (math.atan2(self.wpt.posy-self.y, self.x-self.wpt.posx) + math.pi)

# Draw
        ccx, ccy = terrain_to_screen((self.x, self.y, self.angle))
        rotboat = pygame.transform.rotate(self.sprite, self.angle)
        ccx = ccx-rotboat.get_width()/2
        ccy = ccy - rotboat.get_height()/2
        display.blit (pygame.transform.rotate(self.sprite, self.angle), (ccx, ccy) )
# .............................................................................


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


def start_engine():
    global engine_on, sound_on, engine1
    engine1.play(1000)
    engine_on = True


def stop_engine ():
    global engine_on, sound_on, engine1
    engine1.stop()
    engine_on = False


def otherBoats ():
    global boats, display
    boats[1].nextStep ()
    boats[2].nextStep ()


def playScreen (event):
    global x, y, xx, yy, speeds, angles, engine_on
    eon = False
    if event.type == pygame.KEYDOWN:
        k = pygame.key.get_pressed()
        if k[pygame.K_s]:
              boats[0].speed = boats[0].speed - .1
              eon = True
        if k[pygame.K_w]:
            boats[0].speed = boats[0].speed + .1
            eon = True
        if k[pygame.K_a]:
              boats[0].angle = boats[0].angle + 5
              eon = True
        if k[pygame.K_d]:
              boats[0].angle = boats[0].angle - 5
              eon = True
    if eon and not engine_on:
        start_engine()
    elif not eon and engine_on:
        stop_engine()

#        Rotate a point counterclockwise by a given angle around a given origin.
#        The angle should be given in radians.
def rotate(origin, point, angle):
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(math.radians(angle)) * (px - ox) - math.sin(math.radians(angle)) * (py - oy)
        qy = oy + math.sin(math.radians(angle)) * (px - ox) + math.cos(math.radians(angle)) * (py - oy)
        return (qx, qy)


# Does the boat collide with the shore?
def shoreCollide (i):
    global angles, x, y, xx, yy, background
# Boat Bounding box: (0,0), (84,0), (84,27), (0,27)
    dx =  math.cos(math.radians(boats[i].angle))
    dy = -math.sin(math.radians(boats[i].angle))
    x1 = boats[i].x+50*dx    # Forward
    y1 = boats[i].y+50*dy
    if x1>0 and x1<3200 and y1>0 and y1<2700:
        c = background.get_at((int(x1),int(y1)))
        if c[0] != 33:
            boats[i].sensor = 1
            return True

    x1 = boats[i].x+18*dx  # Port
    y1 = boats[i].y-18*dy
    if x1>0 and x1<3200 and y1>0 and y1<2700:
        c = background.get_at((int(x1),int(y1)))
        if c[0] != 33:
            boats[i].sensor = 1
            return True

    x1 = boats[i].x-18*dx  # Starboard
    y1 = boats[i].y+18*dy
    if x1>0 and x1<3200 and y1>0 and y1<2700:
        c = background.get_at((int(x1),int(y1)))
        if c[0] != 33:
            boats[i].sensor = 2
            return True
    return False

def ray_box (ray, box):
    for j in range (i,4):
        if line_intersect (ray[0], ray[1], box[j], box[j+1]):
            return True
    return False

def box_intersect (b1, b2):
    for i in range(0,4):
        for j in range (i,4):
            if line_intersect (b1[i], b1[i+1], b2[j], b2[j+1]):
                return True
    return False

def ccw(a, b, c):
	return (c[1]-a[1])*(b[0]-a[0]) > (b[1]-a[1])*(c[0]-a[0])

def line_intersect (p1, p2, p3, p4):
    r1 = ccw(p1, p3, p4) != ccw (p2, p3, p4)
    r2 = ccw(p1, p2, p3) != ccw (p1, p2, p4)
    if r1 and r2:
        return True
    return False

def boatCollide ():
    global angles, boats_x, boats_y

    box = []
    for which in range (0,3):
        ul = rotate ( (boats[which].x, boats[which].y), (boats[which].x-42,  boats[which].y-13), -boats[which].angle)
        ur = rotate ( (boats[which].x, boats[which].y), (boats[which].x+42,  boats[which].y-13), -boats[which].angle)
        lr = rotate ( (boats[which].x, boats[which].y), (boats[which].x+42,  boats[which].y+13), -boats[which].angle)
        ll = rotate ( (boats[which].x, boats[which].y), (boats[which].x-42,  boats[which].y+13), -boats[which].angle)

        ul = terrain_to_screen (ul)
        ur = terrain_to_screen (ur)
        lr = terrain_to_screen (lr)
        ll = terrain_to_screen (ll)
        box.append([ul,ur,lr,ll,ul])

        pygame.draw.line(display, (255, 0, 0), ul, ur, 2)
        pygame.draw.line(display, (255, 0, 0), ur, lr, 2)
        pygame.draw.line(display, (255, 0, 0), lr, ll, 2)
        pygame.draw.line(display, (255, 0, 0), ll, ul, 2)

    if box_intersect (box[1], box[2]):
        print("Collision ", 1, 2)
    if box_intersect (box[0], box[1]):
        print ("Collision ", 0, 1)
    if box_intersect (box[0], box[2]):
        print ("Collision ", 0, 2)


def text (str, xx, yy):
    global display
    font = pygame.font.SysFont("comicsansms", 12)
    txt = font.render(str, True, (255, 128, 65))
    display.blit(txt, (xx, yy))


def terrain_to_screen (a):
    global x, y
    return (a[0] - x, a[1]-y)


def boat_to_screen (xpos, ypos, angle):
    global boats
    dx,dy = 0,0
# Adjust their boat position within the display area
    z = xpos - 250       # Boat is far left.
    if z<0:
        dx = 250-xpos    # dx is offset from centre of window
    elif z > 2700:     # 3200 - 500 is 2700
        dx = 2950-xpos
    z = ypos-200
    if z < 0:
        dy = 200-ypos
    elif z>2300:
        dy = 2500-ypos

    myx = 250-dx        # The final boat position in display area
    myy = 200-dy
    rotboat = pygame.transform.rotate(boats[1].sprite, angle)
    cx = myx - rotboat.get_width()/2
    cy = myy - rotboat.get_height()/2
    return ((cx, cy))


def move ():
    global speeds, angles, x, y, xx, yy, background, boat2
    old = (xx, yy, boats[0].x, boats[0].y, x, y)        # Save the previous position
    boats[0].speed = boats[0].speed - 0.001         # Slow down
    if boats[0].speed < 0:                 # Can't move backwards
        boats[0].speed = 0
        dx = 0
        dy = 0
    else:
        dx = boats[0].speed * math.cos(math.radians(boats[0].angle))
        dy = -boats[0].speed * math.sin(math.radians(boats[0].angle))

# Move the boat
    boats[0].x = boats[0].x + dx       # New boat position on the map is (bx, by)
    if boats[0].x>3200:        # Keep the boat on the play area - Too far right
        boats[0].x = 3199
        boats[0].speed = 0
    elif boats[0].x<0:         # Keep the boat on the play area - Too far left
        boats[0].x = 1
        boats[0].speed = 0
    boats[0].y = boats[0].y + dy
    if boats[0].y>2700:        # Keep the boat on the play area - Too far down
        boats[0].y = 2699
        boats[0].speed = 0
    elif boats[0].y<0:         # Keep the boat on the play area - Too far up
        boats[0].y = 1
        boats[0].speed = 0

    dx = 0
    dy = 0
# Adjust their boat position within the display area
    x = boats[0].x - 250       # Boat is far left.
    if x<0:
        x = 0
        dx = 250-boats[0].x    # dx is offset from centre of window
    elif x > 2700:     # 3200 - 500 is 2700
        x = 2700
        dx = 2950-boats[0].x
    y = boats[0].y-200
    if y < 0:
        y = 0
        dy = 200-boats[0].y
    elif y>2300:
        y = 2300
        dy = 2500-boats[0].y

    xx = 250-dx        # The final boat position in display area
    yy = 200-dy

    display.blit(background, (-x, -y))

# Now - is the boat stll in the water? (collision with shore)?
    if shoreCollide (0):
        xx = old[0]
        yy = old[1]
        boats[0].x = old[2]
        boats[0].y = old[3]
        x = old[4]
        y = old[5]

    ccx, ccy = boat_to_screen (boats[0].x, boats[0].y, boats[0].angle)
    display.blit (pygame.transform.rotate(boats[0].sprite, boats[0].angle), (ccx, ccy) )
    text (str(boats[0].speed), 100, 50)
    boatCollide()
    otherBoats()  # NPC boats


def endScreen(event):
    display.blit(endImage, (0,0))
    if event.type == pygame.MOUSEBUTTONUP :
        exit()


pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((500, 400), pygame.SRCALPHA, 32)

background = pygame.image.load ("xx.png")
boat2 = pygame.image.load ("boat4a.gif")
startImage = pygame.image.load ("startScreen.jpg")
optionImage = pygame.image.load ("optionsScreen.jpg")
endImage = pygame.image.load ("endScreen.jpg")
engine1 = pygame.mixer.Sound ("sounds/engineBoat1.wav")

pygame.key.set_repeat(10, 200)
x = 300           # Screen offset
y = 2100
xx = 250          # Boat screen coordinates
yy = 200

#speeds = [0, 0, 0]                  # Speed of each boat
#angles = [90, 90, 90]                 # Facing direction of each boat
#boats_x = [400, 450, 350]           # Position of each boat
#boats_y = [2650,  2650, 2650]
player = npc (450, 2650, pygame.image.load ("boat4a.gif"), 0, 90, 0)
boat3 = npc (550, 2650, pygame.image.load ("boat2a.gif"), 0, 90, 1)
boat4 = npc (350, 2650, pygame.image.load ("boat5a.gif"), 0, 90, 2)
boats = (player, boat3, boat4)
player.setName ("Player")
boat4.setName ("NPC 2")

soundOn = True                      # User selected (ON or OFF)
engine_on = False                   # Is the engine powering the boat?
STARTSTATE = 0                      # Screen states
OPTIONSTATE = 1
PLAYSTATE = 2
ENDSTATE = 3
screenState = STARTSTATE            # Current screen
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

# Read waypoint file and create a tuple
waypoints = ((0,0,0,0),)
with open("params.txt") as f:
    for data in f:
        i = int(data[0:2])
        ix = float (data[3:7])
        iy = float(data[8:12])
        ispeed = float(data[13:])
        w = waypoint(ix, iy, i, ispeed)
        waypoints += (w,)
boat3.setWaypoint(waypoints[1])
boat4.setWaypoint(waypoints[2])

while True:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          exit()
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

  if screenState == PLAYSTATE:
      move()
  pygame.display.update()

