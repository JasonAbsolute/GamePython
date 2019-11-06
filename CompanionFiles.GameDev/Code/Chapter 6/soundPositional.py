# Volume set and pan audio
import pygame
import math


def angle_3pt(x1, y1, x2, y2, x3, y3):
    ax = x2 - x3
    ay = y2 - y3
    da = math.sqrt(ax * ax + ay * ay); #  Length of a
    bx = x2 - x1
    by = y2 - y1
    db = math.sqrt(bx * bx + by * by); # Length of b
    dot = ax * bx + ay * by;           # Dot product
    if (da * db == 0):
        r = 10000.
    else:
        r = dot / (da * db)
    theta = math.acos(r);
    return (theta * 180.0 / 3.1415926)

def pan (a):
  global leftAmp, rightAmp, chan, v

  if a < 0:  a = 0
  if a > 1:  a = 1
  leftAmp = (1 - a)*v
  rightAmp =  a*v
  chan.set_volume(leftAmp, rightAmp)

def distance (a, b):
    x = (a[0]-b[0])
    y = (a[1]-b[1])
    return math.sqrt(x*x+y*y)

# Return - 1 if (cx, cy) is on the left of the line, 1 otherwise.
def  whichSide(ax, ay, bx, by, cx, cy):
    LEFT = -1
    RIGHT = 1

# Test to see if the line is vertical.If so, slope is infinite!
    if (ax == bx):
        if (cx < bx):
            if (by > ay):
                return RIGHT
            else:
                return LEFT
        if (cx > bx):
            if (by > ay):
                return LEFT
            else:
                return RIGHT
        return LEFT

# If the slope is 0 then line is horizontal, and test is also easy.
    if (ay == by):
        if (cy < by):
            if (bx > ax):
                return LEFT
            else:
                return RIGHT

        if (cy > by):
            if (bx > ax):
                return RIGHT
            else:
                return LEFT
            return LEFT


# Now calculate the line equation parameters
    m = float(by - ay) / float(bx - ax)
    b = float(ay) - ax * m;

# Plug in test point to see what the equation says.
    res = (m * cx) + b

    if (m != 0):
        if (cy > res):
            if (bx > ax):
                return RIGHT
            else:
                return LEFT
        if (cy < res):
            if (bx > ax):
                return LEFT
            else:
                return RIGHT
            return RIGHT
    return RIGHT

def positionSound ():
    global leftchan, rightchan, chan, v, w, x, y, facex, facey, left, right, ang
    d = distance ((x,y), (250, 150))         # Distance, source to listener
    a = (d/maxSoundDistance)                 # Attenuation due to distance

    ang = angle_3pt (facex, facey, x, y, 250, 150)  # Angle between listener and source
    w = whichSide (facex, facey, x, y, 250, 150)  # what side of the line defined by the listener
                                          # and the facing point is the sound source is on.d
    v = 1-a
    ang = ang * w
    if (v<0):
        v = 0
    if ang < 360:
        ang = ang + 360
    if ang > 360:
        ang = ang - 360
    right = rightchan[int(ang/9) % 40]
    left =  leftchan[int(ang/9) % 40]
    chan.set_volume(left*v, right*v)

pygame.init()
canvas = pygame.display.set_mode( (200, 100) )
m = pygame.mixer.Sound("song.wav")
chan = pygame.mixer.find_channel()
chan.play(m)
x = 150
y = 150
facex = 0
facey = 0
maxSoundDistance = 150        # Past this distance, sound can't be heard

radius = 5
angle = 0.0
v = 0
ang = 0
w = 0
leftchan =  (.60, .64, .68, .72, .76, .80, .84, .88, .92, .96, 1.0, .96, .92, .88, .84, .80, .76, .72, .68, .64, .60, .55, .50, .45, .40, .35, .30, .25, .20, .15, .10, .15, .20, .25, .30, .35,
.40, .45, .50, .55, .60)
rightchan = (.60, .55, .50, .45, .40, .35, .30, .25, .20, .15, .10, .15, .20, .25, .30, .35, .40, .45, .50, .55, .60, .64, .68, .72, .76, .80, .84, .88, .92, .96, 1.0, .96, .92, .88, .84, .80,
.76, .72, .68, .64, .60)
positionSound()

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((500, 300), pygame.SRCALPHA, 32)
while True:
    clock.tick(30)  # Make sure 1/30 second has passed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x = event.pos[0]
            y = event.pos[1]
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                angle = angle - (10)
            elif event.key == pygame.K_d:
                angle = angle + (10)
            if angle > math.radians(360):
                angle = angle - (360)
            if angle < 0:
                angle = angle + (360)
    facex = 100 * math.cos(math.radians(angle)) + x
    facey = 100 * math.sin(math.radians(angle)) + y
    if angle>360:
        angle = angle-360

    display.fill((100, 100, 100))    # Clear the screen
    pygame.draw.circle(display, (200, 200, 200), (x, y), radius)  # Draw the listener
    pygame.draw.circle(display, (100, 200, 100), (250, 150), radius)  # Draw the listener
    pygame.draw.line(display, (0, 100, 250), (x, y), (facex, facey), 2)
    positionSound()  # Set pan and volume for new listener
    pygame.display.update()




