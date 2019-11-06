import pygame
pygame.init()
im = pygame.image.load ("charlie.png")
width = im.get_width()
height = im.get_height()

for i in range (0,width):
    for j in range(0,height):
        pix = im.get_at ((i,j))
        grey = (pix[0]+pix[1]+pix[2])/3
        grey = 255-grey
        im.set_at ((i,j), (grey, grey, grey))
surf = pygame.display.set_mode((width, height), pygame.SRCALPHA)
surf.blit (im, (0,0))
pygame.display.update()
input()
