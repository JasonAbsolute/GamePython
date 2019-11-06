import pygame
pygame.init()
im = pygame.image.load ("charlie.png")
width = im.get_width()
height = im.get_height()

surf = pygame.display.set_mode((width, height), pygame.SRCALPHA)
A = width/height
newx = 100
newy = int(newx/A)
s = pygame.transform.scale (im, (newx, newy))
surf.blit (s, (0,0))
surf.blit (s, (width//2,0))
surf.blit (s, (0,height//2))
surf.blit (s, (width//2, height//2))
pygame.display.update()
input()