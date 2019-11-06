import pygame
import random

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((500, 300), pygame.SRCALPHA, 32)
images = ()
N = 12
j = 0

im1 = pygame.image.load("explode1.gif")
im2 = pygame.image.load("explode2.gif")
im3 = pygame.image.load("explode3.gif")
im4 = pygame.image.load("explode4.gif")
im5 = pygame.image.load("explode5.png")
im = (im1, im2, im3, im4, im5)
i,j = 0,0
k = 0
while True:
    clock.tick(15)                   # Make sure 1/10 second has passed
    display.fill((100, 100, 100))    # Clear the screen
    if k<5:
        display.blit(im[k], (100, 100), (i*64, j*64, 64, 64) )
        k = k + 1
    else:
        k = int(random.random() * 5)
        i,j = 0,0
        continue
    i = i + 1
    if i>3:
        i = 0
        j = j + 1
        if j>3:
            i,j=0,0
    pygame.display.update()          # Update the screen
