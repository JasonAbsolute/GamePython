import pygame

pygame.init()

display = pygame.display.set_mode((500, 150), pygame.SRCALPHA, 32)
display.fill ((255,255,255))

pygame.draw.circle (display, (255, 0,0, 255), (50, 50), 30)
pygame.draw.circle (display, (0, 255,0, 255), (75, 75), 30)

surf = pygame.Surface((60,60), flags=pygame.SRCALPHA)
pygame.draw.circle (display, (255, 0,0), (150, 50), 30)
pygame.draw.circle (surf, (0, 255, 0, 200), (30,30), 30)
display.blit(surf,(150,40))

surf = pygame.Surface((60,60), flags=pygame.SRCALPHA)
pygame.draw.circle (display, (255, 0,0), (250, 50), 30)
pygame.draw.circle (surf, (0, 255, 0, 128), (30,30), 30)
display.blit (surf, (250, 40))

surf = pygame.Surface((60,60), flags=pygame.SRCALPHA)
pygame.draw.circle (display, (255, 0,0), (350, 50), 30)
pygame.draw.circle (surf, (0, 255, 0, 96), (30,30), 30)
display.blit (surf, (350, 40))

pygame.display.update()
input()
