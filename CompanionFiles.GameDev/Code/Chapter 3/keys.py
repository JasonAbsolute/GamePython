import pygame
pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((500, 250), pygame.SRCALPHA, 32)
forward = False
backward = False
while True:
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            forward = True
        elif event.key == pygame.K_s:
            backward = True
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
            forward = False
        elif event.key == pygame.K_s:
            backward = False
  if forward:
        print ("Forward")
  if backward:
        print ("Backward")
  print (pygame.key.get_pressed()[pygame.K_w])
  pygame.display.update()          # Update the screen