import pygame
pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((500, 250), pygame.SRCALPHA, 32)
while True:
    clock.tick(30)
    pygame.draw.rect(display, (0,255, 255),(100,100,100,50))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            if (mouseX >= 100) and (mouseX <= 100 + 100) and (mouseY >= 100) and (mouseY <= 100 + 50):
                display.fill ((255,0,0))
    pygame.display.update()          # Update the screen
