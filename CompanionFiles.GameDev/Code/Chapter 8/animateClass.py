# Animation class
import pygame
import math

class animate:

    def __init__ (self, xx, yy, disp):
        self.xpos = xx          # Position to place the animation
        self.ypos = yy
        self.frames = ()        # Images for this animation
        self.nextFrame = 0      # Next frame to be played
        self.Nframes = 0        # Total number of frames
        self.soundName = ""     # Name of the sound file for this animation
        self.playing = False    # Is the animation currently being displayed?
        self.disp = disp        # Display on which to render
        self.rate = 1           # Frame rate
        self.counter = 0        # Calls of draw for the current frame
        self.warp = False       # The image is rectangular
        self.wx1 = xx           # Warped image corrdinates
        self.wx2 = xx
        self.wx3 = xx
        self.wx4 = xx
        self.wy1 = yy; self.wy2 = yy; self.wy3 = yy; self.wy4 = yy
        self.width = 0
        self.height = 0

    def play (self):            # Starting playing this animation
        self.playing = True

    def stop (self):            # Stop playing, reset counter
        self.playing = False
        self.nextFrame = 0

    def pause (self):           # Stop playing, don't reset counter
        self.playing = False

    def setPosition (self, x, y):  # Draw this animation at location (x,y_) on the display
        self.xpos = x
        self.ypos = y
        warp = False

    def getPosition (self):     # return the current position as a tuple.
        if (warp):
            return (wx1,wy1, wx2,wy2, wx3,wy3, wx4,wy4)
        return (self.xpos, self.ypos)

    def setSoundName (self, s):  # Name of any associate audio file
        self.soundName = s

    def addFrame (self, p):       # Add a frame (image) to the tuple 'frames'
        self.frames = self.frames + (p,)
        if (self.width == 0):
            self.width = p.get_width()
            self.height = p.get_height()
        self.Nframes = self.Nframes + 1


    def draw (self):              # Draw this frame and increment count
        if self.playing:
            if (self.warp):
                x = self.reShape (self.frames[self.nextFrame])
            else:
                self.disp.blit(self.frames[self.nextFrame], (self.xpos, self.ypos))
            if (self.counter == 0):
                self.nextFrame = (self.nextFrame + 1) % self.Nframes
            self.counter = (self.counter + 1) % self.rate

    def reShape (self, im):
# Bounding box
        xmin = min(self.wx1, self.wx2, self.wx3,self. wx4)
        ymin = min(self.wy1, self.wy2, self.wy3, self.wy4)
        xmax = max(self.wx1, self.wx2, self.wx3, self.wx4)
        ymax = max(self.wy1, self.wy2, self.wy3, self.wy4)

        pygame.draw.line (self.disp, (255, 255, 255), (self.wx1, self.wy1), (self.wx2, self.wy2), 2)
        pygame.draw.line (self.disp, (255, 255, 255), (self.wx2, self.wy2), (self.wx3, self.wy3), 2)
        pygame.draw.line (self.disp, (255, 255, 255), (self.wx3, self.wy3), (self.wx4, self.wy4), 2)
        pygame.draw.line (self.disp, (255, 255, 255), (self.wx4, self.wy4), (self.wx1, self.wy1), 2)

        for X in range (xmin, xmax):
            for Y in range (ymin, ymax):
                C = (self.wy1 - Y) * (self.wx4- X) - (self.wx1 - X) * (self.wy4 - Y)
                B = (self.wy1 - Y) * (self.wx3 - self.wx4) + (self.wy2 - self.wy1) * (self.wx4 - X) - (self.wx1 - X) * (self.wy3 - self.wy4) - (self.wx2 - self.wx1) * (self.wy4 - Y)
                A = (self.wy2 - self.wy1) * (self.wx3 - self.wx4) - (self.wx2 - self.wx1) * (self.wy3 - self.wy4)
                D = B * B - 4 * A * C
                if D>=0 and (A*A>0.00001):
                    u = (-B - math.sqrt(D)) / (2 * A)
                else:
                    u = -1
                p1x = self.wx1 + (self.wx2 - self.wx1) * u
                p2x = self.wx4 + (self.wx3 - self.wx4) * u
                px = X
                if p2x!=p1x:
                    v = (px - p1x) / (p2x - p1x)
                else:
                    v = -1
                if v>=0 and v<1 and u>=0 and u<1:
                    self.disp.set_at((int(X), int(Y)), im.get_at((int(u*self.width), int(v*self.height))))

    def setNext (self, n):         # Set the next frame to be played to 'n'.
        if self.Nframes > 0:
            self.nextFrame = (n % self.Nframes)

    def setRate (self, n):
        if (n>0):
            self.rate = n

    def setSize (self, x1, y1, x2, y2, x3, y3, x4, y4):
        if  (x4-x1)+(x3-x2)+(y2-y2)+(y4-y3) < 5:  # Must not be a rectangle
            x1 = x1 - 1; y1 = y1 + 1
            x2 = x2 + 1; y2 = y2 - 1
            x3 = x3 - 1; y3 = y3 + 1
            x4 = x4 + 1; y4 = y4 - 1
        self.wx1 = x1  # Warped image coordinates
        self.wx2 = x2
        self.wx3 = x3
        self.wx4 = x4
        self.wy1 = y1
        self.wy2 = y2
        self.wy3 = y3
        self.wy4 = y4
        self.warp = True
