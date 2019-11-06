import pygame
import random

boat = pygame.image.load ("boat4a.gif")
wakes = pygame.image.load("wakesv.png")
angle = 0
pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((500, 400), pygame.SRCALPHA, 32)
r = pygame.Surface ((251, 35), pygame.SRCALPHA)
#wake = pygame.Surface ((83, 35), pygame.SRCALPHA)

while True:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          exit()
  pygame.draw.rect (display, (50, 50,200), (0, 0, display.get_width(), display.get_height()), 0)
  k = int(random.random() * 18)
  i = k // 9
  j = k % 9

#  wake.blit(wakes, (0, 0), (i*83, j*35, 83, 35))
  pygame.draw.rect (r, (50, 50,200), (0, 0, r.get_width(), r.get_height()), 0)

  for k in range(0,60):
      ii = int(random.random ()*120)
      jj = int(random.random()*30)+5
      di = int(random.random()*5)-3
      dj = int(random.random()*5)-3
      c = int(255-(120-ii)*1.6)
      pygame.draw.line (r, (c,c,c), (ii,jj), (ii+di,jj+dj))
  r.blit (boat, (83,6))
#      pygame.draw.circle (r, (c,c,c), (ii,jj), 0, 0)

#  r.blit (wakes, (0,6), (i*83, j*35, 83, 35))
  boatr = pygame.transform.rotate(r, angle)

  sx = boatr.get_width()
  sy = boatr.get_height()
  display.blit(boatr, (250-sx/2, 200-sy/2))
  pygame.draw.line (display, (0,0,0), (250,0), (250,400))
  pygame.draw.line (display, (0,0,0), (0,200), (500,200))
  pygame.display.update()
  angle = angle + 0.01
