import pygame
import random

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((500, 300), pygame.SRCALPHA, 32)
images = ()
N = 12
j = 0

im = pygame.image.load("wakes.png")
i,j = 0,0
k = 0
while True:
    clock.tick(30)                   # Make sure 1/10 second has passed
    display.fill((100, 100, 100))    # Clear the screen
    display.blit(im, (100, 100), (i*35, j*83, 35, 83) )
    k = int(random.random()*18)
    i = k%9
    j = k//9
    print (i,j)
#    i = int(random.random()*9)
#    j = int (random.random()*2)
    pygame.display.update()          # Update the screen