# Animation class
import pygame

class animate:

    def __init__ (self, xx, yy):
        self.xpos = xx          # Position to place the animation
        self.ypos = yy
        self.frames = ()        # Images for this animation
        self.nextFrame = 0      # Next frame to be played
        self.Nframes = 0        # Total number of frames
        self.soundName = ""     # Name of the sound file for this animation
        self.playing = False

    def play (self):
        self.playing = True

    def stop (self):
        self.playing = False
        self.nextFrame = 0

    def pause (self):
        self.playing = False

    def setPosition (self, x, y):
        self.xpos = x
        self.ypos = y

    def getPosition (self):
        return (self.xpos, self.ypos)

    def setSoundName (self, s):
        self.soundName = s

    def addFrame (self, p):
        self.frames = self.frames + (p,)
        self.Nframes = self.Nframes + 1

    def draw (self):
        if self.playing:
            display.blit(self.frames[self.nextFrame], (self.xpos, self.ypos))
            self.nextFrame = (self.nextFrame + 1) % self.Nframes

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((320, 240), pygame.SRCALPHA, 32)

ac = animate (20, 30)
for i in range(1,12):  # Read the 11 images that represent the animation
    if i<10:
        im = pygame.image.load("gait/a00"+str(i)+".bmp")
    else:
        im = pygame.image.load("gait/a0"+str(i)+".bmp")
    ac.addFrame (im)

ac.play()
while True:
    clock.tick(10)                   # Make sure 1/30 second has passed
    display.fill((100, 100, 100))    # Clear the screen
    ac.draw()
#    nxt = ac.getPosition()
#    ac.setPosition (nxt[0]+1, nxt[1])
    pygame.display.update()          # Update the screen