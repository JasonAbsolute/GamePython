# Volume set and pan audio
import pygame
import math

def pan (a):
  global leftAmp, rightAmp, chan, v

  if a < 0:  a = 0
  if a > 1:  a = 1
  leftAmp = (1 - a)*v
  rightAmp =  a*v
  chan.set_volume(leftAmp, rightAmp)

pygame.init()
canvas = pygame.display.set_mode( (200, 100) )
m = pygame.mixer.Sound("song.wav")
chan = pygame.mixer.find_channel()

chan.play(m)
chan.set_volume(1, 1)

v = 1.0
p = 0.5
leftAmp = 1.0
rightAmp = 1.0
pan(0.5)

while True:
  for event in pygame.event.get():
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_DOWN:
        v = v - 0.1
        if v < 0:  v = 0
        pan(p)
      if event.key == pygame.K_UP:
        v = v + 0.1
        if v > 1:  v = 1
        pan(p)
      if event.key == pygame.K_LEFT:
        p = p - .1
        if p<0: p = 0
        pan(p)
      if event.key == pygame.K_RIGHT:
        p = p + .1
        if (p>1):  p = 1
        pan(p)

      print (leftAmp, rightAmp, p)
  pygame.display.update()




