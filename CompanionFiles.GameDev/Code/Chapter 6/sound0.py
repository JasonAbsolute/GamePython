# Volume set
import pygame

pygame.init()                                   # Initialization
canvas = pygame.display.set_mode( (200, 100) )
m = pygame.mixer.Sound("song.wav")              # Read the sound file
m.play()                                        # Begin playing the sound

v = 1.0             # Initial volume is maximum (1.0)
while True:
  for event in pygame.event.get():
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_DOWN: # Down key lowers the volume
        v = v - 0.1                # Decrease the volume by the standard amount
        if v < 0:                  # Check bounds
          v = 0
        m.set_volume (v)           # Set the volume to v

      if event.key == pygame.K_UP: # The Up key increases the volume
        v = v + 0.1                # Increase the volume by the standard amount
        if v > 1:                      # Check bounds
          v = 1
        m.set_volume(v)                # Set the volume to v
  print (v, m.get_volume(), m.get_length())
  pygame.display.update()
