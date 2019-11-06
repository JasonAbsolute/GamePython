import pygame
import math
import struct
import random

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
        self.EXPLODING = 4
        self.state = self.NORMAL
        self.sensor = -1
        self.ccount = 0
        self.estate = 0
        self.wframe = 0
        self.wake = pygame.Surface((166, 35), pygame.SRCALPHA)
        self.r = None
        self.player = False
        self.ul = [1,1]
        self.ur = [1,1]
        self.lr = [1,1]
        self.ll = [1,1]
        self.sternx = 0
        self.sterny = 0
        self.prowx = 0
        self.prowy = 0
        self.centrex = 0
        self.centery = 0

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
        println ("Escape.")
        if self.estate < 20:           # Back up
            ddx = self.speed * math.cos(math.radians(self.angle))
            ddy = -self.speed * math.sin(math.radians(self.angle))
            self.x -= ddx
            self.y -= ddy
            println ("Backing up.")
        elif self.estate < 40:
            if self.sensor == 1:
                self.angle -= 4.0
            elif self.sensor == 0:
                self.angle += 2.0
            elif self.sensor == 2:
                self.angle -= 2.0
            self.state = self.COLLIDED
        else:
            self.state = self.NORMAL
        self.estate = self.estate + 1

    def normalize (self, vec):
        leng = math.sqrt((vec[0]*vec[0])+(vec[1]*vec[1]))
        if leng == 0:
            return (0,0)
        return ( (vec[0]/leng, vec[1]/leng) )

    def boatCollision (self, i, ddx, ddy):
        print (self.name, " moving to other boat ", boats[i].name)
        if self.index == i:
            print ("same boat ", self.index, i)
            print ()
            return False

        print (self.name, " collision with ", boats[i].name)
        ul = rotate((boats[i].x, boats[i].y), (boats[i].x, boats[i].y - 13), -boats[i].angle)
        ur = rotate((boats[i].x, boats[i].y), (boats[i].x + 83, boats[i].y - 13), -boats[i].angle)
        lr = rotate((boats[i].x, boats[i].y), (boats[i].x + 83, boats[i].y + 13), -boats[i].angle)
        ll = rotate((boats[i].x, boats[i].y), (boats[i].x, boats[i].y + 13), -boats[i].angle)

        ul = terrain_to_screen(ul)
        ur = terrain_to_screen(ur)
        lr = terrain_to_screen(lr)
        ll = terrain_to_screen(ll)

        pygame.draw.line(display, (255, 0, 255), (ul[0], ul[1]), (ur[0], ur[1]), 2)
        pygame.draw.line(display, (255, 0, 0), (ll[0], ll[1]), (lr[0], lr[1]), 2)
        pygame.draw.line(display, (255, 255, 0), (lr[0], lr[1]), (ur[0], ur[1]), 2)
        # Ray cast forward.
        n = self.normalize((ddx, ddy))  # Make length of velocty vector = 1
        print ("Normalized motion is ", n)

        ray = (n[0]*200, n[1] * 200)    # Ray is now 100 pixels long
        tsme = terrain_to_screen ((self.x, self.y))
        tsray = terrain_to_screen ((self.x+ray[0], self.y+ray[1]))
        pygame.draw.line(display, (0, 255, 0), terrain_to_screen((self.x, self.y)),
                         terrain_to_screen((self.x+ray[0], self.y+ray[1])), 2)

        if line_intersect( terrain_to_screen((self.x, self.y)), terrain_to_screen((self.x+ray[0], self.y+ray[1])),
                           (ul[0], ul[1]), (ur[0], ur[1]) ):
            pygame.draw.line(display, (255, 0, 255), tsme, tsray, 2)
            pygame.draw.line(display, (255, 0, 255), (ul[0], ul[1]), (ur[0], ur[1]), 2)
            print ("intersected top of box. (Purple)")
            return True

        if line_intersect( terrain_to_screen((self.x, self.y)), terrain_to_screen((self.x+ray[0], self.y+ray[1])),
                            (ur[0], ur[1]), (lr[0], lr[1]) ):
            pygame.draw.line(display, (255, 0, 255), tsme, tsray, 2)
            pygame.draw.line(display, (255, 0, 0), (ur[0], ur[1]), (lr[0], lr[1]), 2)
            print ("intersected right side of box. (yellow)")
            return True

        if line_intersect( terrain_to_screen((self.x, self.y)), terrain_to_screen((self.x+ray[0], self.y+ray[1])), (lr[0], lr[1]), (ll[0], ll[1]) ):
            pygame.draw.line(display, (255, 0, 255), tsme, tsray, 2)
            pygame.draw.line(display, (255, 0, 255), (lr[0], lr[1]), (ll[0], ll[1]), 2)
            print ("intersected lower side of box. yellow")
            return True

        if line_intersect( terrain_to_screen((self.x, self.y)), terrain_to_screen((self.x+ray[0], self.y+ray[1])), (ll[0], ll[1]), (ul[0], ul[1]) ):
            pygame.draw.line(display, (255, 0, 255), tsme, tsray, 2)
            pygame.draw.line(display, (255, 0, 255), (ul[0], ul[1]), (ll[0], ll[1]), 2)
            print ("intersected left side of box.  none")
            return True
        print ("No collision")
        return False

    def avoid (self, i, ddx, ddy): # NEEDS WORK
#        ahead = (self.x, self.y) + (self.speed*math.cos(self.angle)*MAX_AHEAD, self.speed*math.sin(self.angle)*MAX_AHEAD)
#        ahead2 = (self.x, self.y) + (self.speed*math.cos(self.angle)*MAX_AHEAD/2, self.speed*math.sin(self.angle)*MAX_AHEAD/2)

        print (self.name, "Avoiding ")
        self.state = self.AVOID
     #   zangle = self.targetAngle = math.degrees(math.atan2(ddy - self.y, ddx - self.x) - math.radians(180.0))


        zangle = math.degrees(math.atan2(ddy - self.y, ddx - self.x) - math.radians(180.0))
        if zangle < 0:
            zangle = zangle + 360.0
        elif zangle > 350:
            zangle = zangle - 360
        print ("Angle to ship is ", zangle, " course is ", self.angle)
        if self.angle < zangle*1.3:
            self.angle = self.angle + 1
        else:
            self.angle = self.angle - 1
        print ("New course is ", self.angle)
        return

    def nextStep (self):
        global display, boats

        ddx = self.speed * math.cos(math.radians(self.angle))
        ddy = -self.speed * math.sin(math.radians(self.angle))

# STATE ------- Collisions? First with shore --------------------------
        if self.state == self.COLLIDED:
                self.escape()
        else:                       # First, move the boat. Water friction will slow it.
            self.speed = self.speed  # - 0.001   # Slow down
            if self.speed < 0:                # Can't move backwards
                self.speed = 0
                ddx = 0
                ddy = 0
            else:
                ddx = self.speed * math.cos(math.radians(self.angle))
                ddy = -self.speed * math.sin(math.radians(self.angle))


# Collision with another boat?
        print ("Calling boat collision with self = ", self.index, self.name, " and other is ", boats[0].index, boats[0].name)
        if self.boatCollision (0, ddx, ddy):
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

# Adjust speed and angle
            if self.state == self.NORMAL:
                self.adjustSpeed ()
                self.adjustAngle()

# Steer
        if self.wpt != None and self.state == self.NORMAL:
            self.targetAngle = math.degrees (math.atan2(self.wpt.posy-self.y, self.x-self.wpt.posx) + math.pi)
        elif self.state == self.AVOID:
            if abs(self.targetAngle - self.angle) < .5:
                self.state = self.NORMAL
# Draw
        ccx, ccy = terrain_to_screen((self.x, self.y, self.angle))                # Compute the bounding box
        newy = self.y - math.sin(math.radians(self.angle))*83
        newx = self.x + math.cos(math.radians(self.angle))*83
        self.prowx, self.prowy = terrain_to_screen ((newx, newy, self.angle))     # Screen location of prow

        k = int(random.random() * 18)                                   # Select a wake image
        j = k % 9
        i = k // 9
        if self.r == None:
            self.r = pygame.Surface((166, 35), pygame.SRCALPHA)         # Create new surface
        self.r.blit (self.sprite, (83,6))                               # Draw the boat
        rotboat = pygame.transform.rotate(self.r, self.angle)           # Need the size of the rotated BB
        self.sternx = ccx                                               # Screen location of stern
        self.sterny = ccy
        ccx = ccx-rotboat.get_width()/2          # Centre of the joint box holding
        ccy = ccy-rotboat.get_height()/2         # the boat AND the wake. At the stern.
        self.centrex = (self.sternx + self.prowx)/2
        self.centrey = (self.sterny + self.prowy)/2
        display.blit (pygame.transform.rotate(self.r, self.angle), (ccx, ccy) )
        pygame.draw.rect(display, (255, 255, 255), (self.centrex-3, self.centrey-3, 6, 6), 0)
# ................................................................................................

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
    boats[0].nextStep ()
    boats[1].nextStep ()

def playScreen (event):
    global x, y, xx, yy, speeds, angles, engine_on, player
    eon = False
    if event.type == pygame.KEYDOWN:
        k = pygame.key.get_pressed()
        if k[pygame.K_s]:
              player.speed = player.speed - .15
              eon = True
        if k[pygame.K_w]:
            player.speed = player.speed + .15
            eon = True
        if k[pygame.K_a]:
              player.angle = player.angle + 5
              eon = True
        if k[pygame.K_d]:
              player.angle = player.angle - 5
              eon = True
    if eon and not engine_on:
        start_engine()
    elif not eon and engine_on:
        stop_engine()
    if engine_on and player.speed <=0:
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

def boatCollidexx ():
    global angles, boats_x, boats_y

    box = []
    if box == []:
        return
    for which in range (0,2):
        ul = rotate ( (boats[which].x, boats[which].y), (boats[which].x,  boats[which].y-13), -boats[which].angle)
        ur = rotate ( (boats[which].x, boats[which].y), (boats[which].x+83,  boats[which].y-13), -boats[which].angle)
        lr = rotate ( (boats[which].x, boats[which].y), (boats[which].x+83,  boats[which].y+13), -boats[which].angle)
        ll = rotate ( (boats[which].x, boats[which].y), (boats[which].x,  boats[which].y+13), -boats[which].angle)
#        ul = rotate ( (boats[which].x, boats[which].y), (boats[which].x-42,  boats[which].y-13), -boats[which].angle)
#        ur = rotate ( (boats[which].x, boats[which].y), (boats[which].x+42,  boats[which].y-13), -boats[which].angle)
#        lr = rotate ( (boats[which].x, boats[which].y), (boats[which].x+42,  boats[which].y+13), -boats[which].angle)
#        ll = rotate ( (boats[which].x, boats[which].y), (boats[which].x-42,  boats[which].y+13), -boats[which].angle)
        ul = terrain_to_screen (ul)
        ur = terrain_to_screen (ur)
        lr = terrain_to_screen (lr)
        ll = terrain_to_screen (ll)
        box.append([ul,ur,lr,ll,ul])

        pygame.draw.line(display, (255, 0, 0), ul, ur, 2)
        pygame.draw.line(display, (255, 0, 0), ur, lr, 2)
        pygame.draw.line(display, (255, 0, 0), lr, ll, 2)
        pygame.draw.line(display, (255, 0, 0), ll, ul, 2)

    if box_intersect (box[0], box[1]):
        print ("Collision ", 0, 1)


def text (str, xx, yy):
    global display
    font = pygame.font.SysFont("comicsansms", 12)
    txt = font.render(str, True, (255, 128, 65))
    display.blit(txt, (xx, yy))


def terrain_to_screen (a):
    global x, y
    return (a[0] - x, a[1]-y)

def screen_to_terrain (a):
    global x, y
    return (a[0]+x, a[1]+y)

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
    global speeds, angles, x, y, xx, yy, background, boat2, player
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

    otherBoats()  # NPC boats
#    boatCollide()



pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((600, 400), pygame.SRCALPHA, 32)

background = pygame.image.load ("xxx.png")
engine1 = pygame.mixer.Sound ("sounds/engineBoat1.wav")
r = None
pygame.key.set_repeat(10, 200)
x = 200           # Screen offset
y = 300
xx = 250          # Boat screen coordinates
yy = 100

boat4 = npc (400, 300, pygame.image.load ("boat4a.gif"), 0, 90, 0)
boat3 = npc (200, 500, pygame.image.load ("boat2a.gif"), 0, 90, 1)
boat3.angle = 45
boat3.speed = 0.25
boat3.setName ("NPC 3")
boat4.setName ("NPC 4")
boats = (boat4, boat3)

soundOn = True                      # User selected (ON or OFF)
engine_on = False                   # Is the engine powering the boat?
STARTSTATE = 0                      # Screen states
OPTIONSTATE = 1
PLAYSTATE = 2
ENDSTATE = 3
screenState = PLAYSTATE            # Current screen
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
      if event.type == pygame.QUIT:
          exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
          boat3.x, boat3.y = pygame.mouse.get_pos()
      playScreen (event)

  if screenState == PLAYSTATE:
      move()
  pygame.display.update()

