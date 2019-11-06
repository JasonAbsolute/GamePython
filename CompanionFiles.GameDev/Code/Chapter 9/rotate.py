import pygame

boat = pygame.image.load ("boat4a.gif")
wakes = pygame.image.load("wakes.png")
angle = 0
pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((500, 400), pygame.SRCALPHA, 32)
boatr = pygame.Surface ((90, 90), pygame.SRCALPHA)

while True:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          exit()

  display.fill ((255,255,255))
  boatr.blit (boat, (0,0))
  boatr = pygame.transform.rotate(boat, angle)
  sx = boatr.get_width()
  sy = boatr.get_height()
  display.blit(boatr, (250-sx/2, 200-sy/2))

  pygame.draw.line (display, (0,0,0), (250,0), (250,400))
  pygame.draw.line (display, (0,0,0), (0,200), (500,200))
  pygame.display.update()
  angle = angle + 0.001