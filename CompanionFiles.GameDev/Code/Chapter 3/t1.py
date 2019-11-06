import pygame

pygame.init()
surf = pygame.display.set_mode((400, 400))
surf.fill ((255,255,255))
s1 = pygame.Surface((200,200), pygame.SRCALPHA, 32)
s1.fill ((255,255,255, 0))
pygame.draw.rect (s1, (230,230, 0), (50, 50, 100, 100), 1)
s2 = pygame.Surface((200,200), pygame.SRCALPHA, 32)
s2.fill ((255,255,255, 0))
pygame.draw.circle (s2, (0,200, 50), (60, 60), 50)
surf.blit (s1, (0,0))
surf.blit (s2, (100,100))
pygame.display.update()
input()

