import pygame
pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((500, 300), pygame.SRCALPHA, 32)

while True:
    clock.tick(30)                   # Make sure 1/30 second has passed
    display.fill((100, 100, 100))    # Clear the screen


    pygame.display.update()          # Update the screen
