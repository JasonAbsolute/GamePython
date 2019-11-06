# Game 1 - Pop the bouncing ball
import pygame
import math

def distance (a, b):
    x = (a[0]-b[0])
    y = (a[1]-b[1])
    return math.sqrt(x*x+y*y)

dx = 3     # Speed in X direction
dy = 4     # Speed in Y direction
x = 100    # X position
y = 100    # Y position
radius = 20
pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((500, 300), pygame.SRCALPHA, 32)
while True:
    clock.tick(30)                   # Make sure 1/30 second has passed
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            if distance((mouseX, mouseY), (x, y)) <= radius:
                x = 100  # X position
                y = 100  # Y position

    display.fill((100, 100, 100))    # Clear the screen
    x = x + dx                       # Move objects
    y = y + dy
    pygame.draw.circle (display, (200,200,200), (x,y), radius) # Draw the ball
    if (x< radius or x>500- radius): # Outside of the screen in x?
        dx = -dx                     # Change the motion direction in x
    if (y< radius) or (y>300- radius):  # Outside of the screen in y?
        dy = -dy                     # Change the motion direction in x


    pygame.display.update()          # Update the screen
