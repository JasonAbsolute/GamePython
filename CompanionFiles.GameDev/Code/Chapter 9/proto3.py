import pygame
import math
import struct
import random
import time

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
        self.ccount = 0
        self.estate = 0
        self.delta = 0
        self.wake = pygame.Surface((166, 35), pygame.SRCALPHA)
        self.frame = 0
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
        self.done = False
        self.kimage = int(random.random ()*5)
        self.savedx = x
        self.savedy = y

    def display(self):
        ccx, ccy = terrain_to_screen((self.x, self.y, self.angle))  # Compute the bounding box
        newy = self.y - math.sin(math.radians(self.angle)) * 83
        newx = self.x + math.cos(math.radians(self.angle)) * 83
        self.prowx, self.prowy = terrain_to_screen((newx, newy, self.angle))  # Screen location of prow

        k = int(random.random() * 18)  # Select a wake image
        j = k % 9
        i = k // 9
        if self.r == None:
            self.r = pygame.Surface((166, 35), pygame.SRCALPHA)  # Create new surface
        self.r.blit(wakes, (-1, 6), (i * 83, j * 35, 83, 35))  # Draw the wake
        self.r.blit(self.sprite, (83, 6))  # Draw the boat
        rotboat = pygame.transform.rotate(self.r, self.angle)  # Need the size of the rotated BB
        self.sternx = ccx  # Screen location of stern
        self.sterny = ccy
        ccx = ccx - rotboat.get_width() / 2  # Centre of the joint box holding
        ccy = ccy - rotboat.get_height() / 2  # the boat AND the wake. At the stern.
        self.centrex = (self.sternx + self.prowx) / 2
        self.centrey = (self.sterny + self.prowy) / 2
        if self.state == self.EXPLODING:
            if self.frame == 0:
                self.savedx = ccx
                self.savedy = ccy
            self.showNextExFrame(self.savedx, self.savedy)
        else:
            display.blit(pygame.transform.rotate(self.r, self.angle), (ccx, ccy))
        pygame.draw.line(display, (255, 255, 255), (self.ul[0], self.ul[1]), (self.ur[0], self.ur[1]), 0)
        pygame.draw.line(display, (255, 255, 255), (self.ll[0], self.ll[1]), (self.lr[0], self.lr[1]), 0)

    def showNextExFrame (self, x, y):
        print ("Next frame for ", self.name, " is ", self.frame)
        global im, s1, kimage
        i = self.frame//4
        j = self.frame%4
        display.blit(im[self.kimage], (x - 32, y - 32), (i * 64, j * 64, 64, 64))
        self.frame = self.frame + 1
        if self.frame >= 16:
            self.state = self.NORMAL
            self.reset()

    def reset (self):
        global kimage
        if self.index == 0: # Player
            self.x = 450
            self.setWaypoint(waypoints[2])
        elif self.index == 1:
            self.x = 550
            self.setWaypoint(waypoints[1])
        else:
            self.x = 350
            self.setWaypoint(waypoints[2])
        self.y = 2650
        self.speed = 0
        self.angle = 90
        kimage = (kimage + 1) % 4
        self.update_box()


    def setSpeed (self, s):
        self.targetSpeed = s

    def setCourse (self, a):
        self.setAngle = a

    def setWaypoint (self, w):
        self.wpt = w
        self.targetSpeed = w.speed

    def setName (self, s):
        self.name = s

    def fabs(self, x):
        if x<0:
            return -x
        return x

    def adjustAngle (self):
        if self.angle > 360.0:
            self.angle = self.angle - 360
        if self.angle < 0:
            self.angle = self.angle + 360
        dap = abs(self.targetAngle - self.angle)            # Target - course
        dan = abs((self.targetAngle-360.0) - self.angle)    # target-360-course
        if dan < dap:
            da = -dan
        else:
            da = dap
        if self.angle < self.targetAngle:
            self.angle = self.angle+ da
        else:
            self.angle = self.angle - da

    def adjustSpeed (self):
        if self.speed < self.targetSpeed:
            self.speed = self.speed + 0.2
            if self.speed > self.targetSpeed:
                self.speed = self.targetSpeed
        elif self.speed > self.targetSpeed:
            self.speed = self.speed - 0.2
            if self.speed < 0:
                self.speed = 0

    def distance (self, a, b):
        return math.sqrt ( (a[0]-b[0])*(a[0]-b[0]) + (a[1]-b[1])*(a[1]-b[1]) )

    def escape (self):
        if self.estate < 30:           # Back up
            ddx = self.speed * math.cos(math.radians(self.angle))
            ddy = -self.speed * math.sin(math.radians(self.angle))
            self.x -= ddx*2
            self.y -= ddy*2
        elif self.estate < 40:
                self.angle += 2.0
        else:
            self.state = self.NORMAL
            self.targetSpeed = 1
        self.estate = self.estate + 1

    def normalize (self, vec):
        leng = math.sqrt((vec[0]*vec[0])+(vec[1]*vec[1]))
        if leng == 0:
            return (0,0)
        return ( (vec[0]/leng, vec[1]/leng) )

    def boatCollision(self, i, ddx, ddy):
        if self.index == i:
            return False
        ul = rotate((boats[i].x, boats[i].y), (boats[i].x, boats[i].y - 13), -boats[i].angle)
        ur = rotate((boats[i].x, boats[i].y), (boats[i].x + 83, boats[i].y - 13), -boats[i].angle)
        lr = rotate((boats[i].x, boats[i].y), (boats[i].x + 83, boats[i].y + 13), -boats[i].angle)
        ll = rotate((boats[i].x, boats[i].y), (boats[i].x, boats[i].y + 13), -boats[i].angle)

        ul = terrain_to_screen(ul)
        ur = terrain_to_screen(ur)
        lr = terrain_to_screen(lr)
        ll = terrain_to_screen(ll)

#        pygame.draw.line(display, (255, 0, 255), (ul[0], ul[1]), (ur[0], ur[1]), 2)
#        pygame.draw.line(display, (255, 0, 0), (ll[0], ll[1]), (lr[0], lr[1]), 2)
#        pygame.draw.line(display, (255, 255, 0), (lr[0], lr[1]), (ur[0], ur[1]), 2)
        # Ray cast forward.
        n = self.normalize((ddx, ddy))  # Make length of velocty vector = 1

        ray = (n[0] * 200, n[1] * 200)  # Ray is now 100 pixels long
        tsme = terrain_to_screen((self.x, self.y))
        tsray = terrain_to_screen((self.x + ray[0], self.y + ray[1]))
#        pygame.draw.line(display, (0, 255, 0), terrain_to_screen((self.x, self.y)),
#                         terrain_to_screen((self.x + ray[0], self.y + ray[1])), 2)

        if line_intersect(terrain_to_screen((self.x, self.y)), terrain_to_screen((self.x + ray[0], self.y + ray[1])),
                          (ul[0], ul[1]), (ur[0], ur[1])):
#            pygame.draw.line(display, (255, 0, 255), tsme, tsray, 2)
#            pygame.draw.line(display, (255, 0, 255), (ul[0], ul[1]), (ur[0], ur[1]), 2)

            return True

        if line_intersect(terrain_to_screen((self.x, self.y)), terrain_to_screen((self.x + ray[0], self.y + ray[1])),
                          (ur[0], ur[1]), (lr[0], lr[1])):
#            pygame.draw.line(display, (255, 0, 255), tsme, tsray, 2)
#            pygame.draw.line(display, (255, 0, 0), (ur[0], ur[1]), (lr[0], lr[1]), 2)
            return True

        if line_intersect(terrain_to_screen((self.x, self.y)), terrain_to_screen((self.x + ray[0], self.y + ray[1])),
                          (lr[0], lr[1]), (ll[0], ll[1])):
#            pygame.draw.line(display, (255, 0, 255), tsme, tsray, 2)
#            pygame.draw.line(display, (255, 0, 255), (lr[0], lr[1]), (ll[0], ll[1]), 2)
            return True

        if line_intersect(terrain_to_screen((self.x, self.y)), terrain_to_screen((self.x + ray[0], self.y + ray[1])),
                          (ll[0], ll[1]), (ul[0], ul[1])):
#            pygame.draw.line(display, (255, 0, 255), tsme, tsray, 2)
#            pygame.draw.line(display, (255, 0, 255), (ul[0], ul[1]), (ll[0], ll[1]), 2)
            return True
        return False

    def avoid(self, i, ddx, ddy):  # NEEDS WORK
        if self.state == self.AVOID:
            self.ccount -= 1
            self.angle += self.delta
            if self.ccount <=0:
                self.ccount = 0
                self.state = self.NORMAL
                self.delta = 0
                return
        else:
            self.ccount = 100
            self.state = self.AVOID

            zangle = math.degrees(math.atan2(ddy - self.y, ddx - self.x) - math.radians(180.0))
            if zangle < 0:
                zangle = zangle + 360.0
            elif zangle > 360:
                zangle = zangle - 360.0
            if self.angle < zangle * 1.3:
                self.delta = 0.25
            else:
                self.delta = -0.25
                self.speed = 0.2
            return

    def update_box(self):
        self.ul = rotate((self.x, self.y), (self.x, self.y - 9), -self.angle)
        self.ur = rotate((self.x, self.y), (self.x + 55, self.y - 9), -self.angle)
        self.lr = rotate((self.x, self.y), (self.x + 55, self.y + 9), -self.angle)
        self.ll = rotate((self.x, self.y), (self.x, self.y + 9), -self.angle)

        self.ul = terrain_to_screen(self.ul)
        self.ur = terrain_to_screen(self.ur)
        self.lr = terrain_to_screen(self.lr)
        self.ll = terrain_to_screen(self.ll)

    def playerStep(self):
        global display, boats
        if self.done:
            return

# First, move the boat. Water friction will slow it.
        self.speed = self.speed - 0.001  # Slow down
        if self.speed < 0:  # Can't move backwards
            self.speed = 0
            ddx = 0
            ddy = 0
        else:
            ddx = self.speed * math.cos(math.radians(self.angle))
            ddy = -self.speed * math.sin(math.radians(self.angle))
        self.update_box()

        t = shoreCollide(self.index)
        if t:  # Collided just now
            self.speed = 0

# Move the boat
        else:
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

        if (self.wpt != None):
            d = self.distance ((self.x, self.y), (self.wpt.posx,self.wpt.posy))
            if  d < 200: # Arrived at waypoint?
                k = self.wpt.index+2
                bing.play()
                if (k>28)and (self.x>2000 and self.y>=2624):
                    k=29
                    record (0)
                    self.done = true
                self.wpt = waypoints[k]
        self.display()

    def nextStep (self):
        global display, boats

        if self.player:
            self.playerStep()
            return

        if self.done:
            return

        self.update_box()
# STATE ------- Collisions? First with shore --------------------------
        if self.state == self.COLLIDED:
                self.escape()
                self.speed = 1
                self.escape()
                ddx = 0
                ddy = 0
        else:                       # First, move the boat. Water friction will slow it.
            self.speed = self.speed - 0.001   # Slow down
            if self.speed < 0:                # Can't move backwards
                self.speed = 0
                ddx = 0
                ddy = 0
            else:
                ddx = self.speed * math.cos(math.radians(self.angle)) *2
                ddy = -self.speed * math.sin(math.radians(self.angle))*2

            if not self.state == self.EXPLODING:
                t = shoreCollide(self.index)
                if t and (self.state == self.NORMAL):       # Collided just now
                    self.state = self.COLLIDED
                    self.estate = 0

# Collision with another boat?

        if (self.boatCollision(0, ddx, ddy) or self.ccount>0) and (not self.state == self.EXPLODING):
                self.avoid(0, ddx, ddy)
                self.speed += 0.001
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

# Waypoint??
        if (self.wpt != None):
            d = self.distance ((self.x, self.y), (self.wpt.posx,self.wpt.posy))
            if  d < 100: # Arrived at waypoint?
                k = self.wpt.index+2
                if (k>30):
                    k = 29
                    self.done = True
                    self.speed = 0
                    record (self.index)
                self.wpt = waypoints[k]

# Adjust speed and angle
        if self.state == self.NORMAL:
                self.adjustSpeed ()
                self.adjustAngle()

# Steer
        if self.wpt != None and self.state == self.NORMAL:
            self.targetAngle = math.degrees (math.atan2(self.wpt.posy-self.y, self.x-self.wpt.posx) + math.pi)

# Draw
        self.display()
# ................................................................................................


def startScreen (ev):
    global screenState, PLAYSTATE, OPTIONSTATE, ENDSTATE, starting, initialTime
    display.blit(startImage, (0, 0))
    playButton.draw()
    if ev.type == pygame.MOUSEBUTTONUP and playButton.isArmed():
        screenState = PLAYSTATE
        starting = True
        initialTime = time.time()
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
    engine1.play(-1)
    engine1.set_volume (0.4)
    engine_on = True

def stop_engine ():
    global engine_on, sound_on, engine1
    engine1.stop()
    engine_on = False

def boatCollided (a, b):
    if boats[a].done or boats[b].done:
        return False
    boat1 = boats[a]
    if boat1.state == boat1.EXPLODING:
        return False
    boat2 = boats[b]
    if boat2.state == boat2.EXPLODING:
        return False
    return box_intersect ( (boat1.ul, boat1.ur, boat1.lr, boat1.ll), (boat2.ul, boat2.ur, boat2.lr, boat2.ll) )

def otherBoats ():
    global boats, display
    boats[1].nextStep ()
    boats[2].nextStep ()

def playScreen (event):
    global x, y, xx, yy, speeds, angles, engine_on, player, starting
    eon = False
    if starting:
        return
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

def test_point (x, y):
    if x < 50 or x > 3150:
        return True
    if y < 50 or y > 2660:
        return True
    return False

# Does the boat collide with the shore?
def shoreCollide(i):
        global background
        boat = boats[i]
        if boat.lr == [1, 1]:    # A new boat
            return False
        ulx, uly = screen_to_terrain(boat.ul)
        if test_point (ulx, uly):
            return True
        lrx, lry = screen_to_terrain(boat.lr)
        if test_point (lrx, lry):
            return True
        urx, ury = screen_to_terrain(boat.ur)
        if test_point (urx, ury):
            return True
        llx, lly = screen_to_terrain(boat.ll)
        if test_point (llx, lly):
            return True
#        pygame.draw.line(display, (0, 255, 0), (boat.ul[0], boat.ul[1]), (boat.ur[0], boat.ur[1]), 3)
#        pygame.draw.line(display, (255, 0, 0), (boat.ur[0], boat.ur[1]), (boat.lr[0], boat.lr[1]), 3)

        c = background.get_at((int(ulx), int(uly)))   # Upper left corner
        if c[0] != 33:
            return True
        c = background.get_at((int(llx), int(lly)))   # lower left
        if c[0] != 33:
            return True
        c = background.get_at((int(urx), int(ury)))   # Upper right
        if c[0] != 33:
            return True
        c = background.get_at((int(lrx), int(lry)))   # Lower right
        if c[0] != 33:
            return True
        return False

def ray_box (ray, box):
    for j in range (i,4):
        if line_intersect (ray[0], ray[1], box[j], box[j+1]):
            return True
    return False

def box_intersect (b1, b2):
    if b1[0] == [1,1]:
        return False
    for i in range(0,3):
        for j in range (i,3):
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

def record (i):
    global places
    places = places + [i,]
    finish.play()
    finish.set_volume (0.5)

def countdown ():
    global initialTime, starting, start
    diff = time.time() - initialTime
    if 10-diff <= 1:
        starting = False
        initialTime = time.time()
        gun.play()
        ambiance.play(loops = -1)
        ambiance.set_volume (0.1)
        return 0
    else:
        return int(10-diff)

def drawWaypoints ():
    global redFlag, blueFlag
    for i in range (1, 31):
        x = waypoints[i].posx
        y = waypoints[i].posy
        if i%2 == 0:
            display.blit (blueFlag, terrain_to_screen((x, y)))
        else:
            display.blit (redFlag,  terrain_to_screen((x, y)))

def move ():
    global x, y, xx, yy, background, boat3, boat4, player, bk2, initialTime
    old = (xx, yy, boats[0].x, boats[0].y, x, y)        # Save the previous position
    boats[0].speed = boats[0].speed - 0.001         # Slow down
    if boats[0].speed < 0:                 # Can't move backwards
        boats[0].speed = 0
        dx = 0
        dy = 0
    else:
        dx = boats[0].speed * math.cos(math.radians(boats[0].angle))
        dy = -boats[0].speed * math.sin(math.radians(boats[0].angle))

# Check the player's boat, adjust the viewport

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

    if starting:
        k = countdown()
        player.display()
        boat3.display()
        boat4.display()
        pygame.draw.rect(display, (0, 0, 0), (500, 0, 200, 400), 0)
        text("Start in     " + str(k) + "  seconds", 520, 100)
        return
    else:
        drawWaypoints()
        otherBoats()  # NPC boats
        player.nextStep()
        pygame.draw.rect(display, (0, 0, 0), (500, 0, 200, 400), 0)

    text ("Player     "+str(int(player.x))+"  "+str(int(player.y)), 520, 100)
    text ("    Speed: "+ str(int(player.speed*10))+ " Course: "+ str(int(player.angle)), 520, 115)
    text ("NPC 3     "+str(int(boat3.x))+"  "+str(int(boat3.y)), 520, 130)
    text ("    Speed: "+ str(int(boat3.speed*10))+ " Course: "+ str(int(boat3.angle)), 520, 145)
    text ("NPC 4     "+str(int(boat4.x))+"  "+str(int(player.y)), 520, 160)
    text ("    Speed: "+ str(int(boat4.speed*10))+ " Course: "+ str(int(boat4.angle)), 520, 175)
    text("OFFICIAL RACE TIME: "+str(int(time.time()-initialTime)), 520, 50)
    display.blit(bk2, (500,220))
    pygame.draw.circle(display, (255, 0, 0), (int(500+player.x/16), int(220+player.y/16)), 2, 0)
    pygame.draw.circle(display, (0, 255, 0), (int(500+boat3.x/16), int(220+boat3.y/16)), 2, 0)
    pygame.draw.circle(display, (0, 255, 0), (int(500+boat4.x/16), int(220+boat4.y/16)), 2, 0)

def endScreen(event):
    display.blit(endImage, (0,0))
    if event.type == pygame.MOUSEBUTTONUP :
        exit()

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((700, 400), pygame.SRCALPHA, 32)
d2 = pygame.Surface ((200, 169))
initialTime = 0
# ----------------------- Graphics ----------------------------------
background = pygame.image.load ("xx.png")             # Terrain map
bk2 = pygame.transform.scale(background, (200,169))   # Mini-map 1/16 scale
#boat2 = pygame.image.load ("boat4a.gif")
startImage = pygame.image.load ("startScreen.jpg")    # The start screen
optionImage = pygame.image.load ("optionsScreen.jpg") # Options screen
wakes = pygame.image.load("wakes2.gif")               # Wake animations
endImage = pygame.image.load ("endScreen.jpg")        # End screen
im1 = pygame.image.load("explode1.gif")               # Explosion animations
im2 = pygame.image.load("explode2.gif")
im3 = pygame.image.load("explode3.gif")
im4 = pygame.image.load("explode4.gif")
im5 = pygame.image.load("explode5.png")
kimage = 0                                         # Index of the enxt explosion to play
im = (im1, im2, im3, im4, im5)                     # All five explosion animation
redFlag = pygame.image.load("redFlag.png")
blueFlag = pygame.image.load("blueFlag.png")

# ----------------------- Sounds ----------------------------------
engine1 = pygame.mixer.Sound ("sounds/engineBoat1.wav")   # Engine
s1 = pygame.mixer.Sound("sounds/exp1.wav")             # Explosion sounds
s2 = pygame.mixer.Sound("sounds/exp2.wav")
snd = (s1, s2)                                         # List of all explosion sounds
gun = pygame.mixer.Sound("sounds/start.wav")           # Starting gun
finish = pygame.mixer.Sound("sounds/finish.wav")       # Finish line cheer
ambiance = pygame.mixer.Sound("sounds/audience.wav")   # Background crowd
bing =  pygame.mixer.Sound("sounds/bing.wav")          # Player arrives at checkpoint

r = None
pygame.key.set_repeat(10, 200)
x = 300           # Screen offset
y = 2100
xx = 250          # Boat screen coordinates
yy = 200

# -----------------------------Boats ----------------------------
player = npc (450, 2650, pygame.image.load ("boat4a.gif"), 0, 90, 0)
player.player = True
places = []
boat3 = npc (550, 2650, pygame.image.load ("boat2a.gif"), 0, 90, 1)
boat4 = npc (350, 2650, pygame.image.load ("boat5a.gif"), 0, 90, 2)
boats = (player, boat3, boat4)
player.setName ("Player")
boat4.setName ("NPC 4")
boat3.setName ("NPC 3")
starting = False                    # Game is in the countdown state
soundOn = True                      # User selected (ON or OFF)
engine_on = False                   # Is the engine powering the boat?
STARTSTATE = 0                      # Screen states
OPTIONSTATE = 1
PLAYSTATE = 2
ENDSTATE = 3
screenState = STARTSTATE            # Current screen
playButton = button (100, 200, 100, 30)  # Buttons on the active screens
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
with open("params.txt") as f:            # Waypoint parameters are in this file
    for data in f:
        i = int(data[0:2])
        ix = float (data[3:7])
        iy = float(data[8:12])
        ispeed = float(data[13:])
        w = waypoint(ix, iy, i, ispeed)
        waypoints += (w,)
boat3.setWaypoint(waypoints[1])
boat4.setWaypoint(waypoints[2])
player.setWaypoint(waypoints[2])

while True:
  clock.tick(50)  # Make sure rate is 50/second
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
      for i in range (0,3):                       # Check boat collisions
          for j in range (i+1,3):
              if boatCollided (i,j):              # Boom
                  boats[i].savedx = boats[i].x
                  boats[i].savedy = boats[i].y
                  boats[j].savedx = boats[j].x
                  boats[j].savedy = boats[j].y
                  boats[i].state = boats[i].EXPLODING  # Change boat states
                  boats[j].state = boats[j].EXPLODING
                  boats[i].frame = 0
                  boats[j].frame = 0
                  snd[int(random.random()*2)].play()   # Play explosion sound

  pygame.display.update()

