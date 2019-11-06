# Display animation of a character walking (gait)
import pygame
pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((320, 240), pygame.SRCALPHA, 32)
images = ()
N = 12

for i in range(1,N):  # Read the 11 images thaht represent the animation
    if i<10:
        im = pygame.image.load("gait/a00"+str(i)+".bmp")
    else:
        im = pygame.image.load("gait/a0"+str(i)+".bmp")
    images = images + (im,)    # The tuple images holds all frames.

i = 0
while True:
    clock.tick(10)                   # Make sure 1/30 second has passed
    display.fill((100, 100, 100))    # Clear the screen
    display.blit(images[i], (0, 0))  # Write current frame (image) to screen
    i = (i+1)%11                     # Index for the next frame
    pygame.display.update()          # Update the screen
