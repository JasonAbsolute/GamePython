import pygame

# y = 60
# for n in range(0, 27):
#     pygame.draw.line(surf, (0, 0, 255), (0, y), (width, y))
#     y = y + 10
# pygame.draw.line(surf, (255, 0, 0), (25, 0), (25, hieght))
# # pygame.draw.arc (surf, c, box, start_angle, end_angle)
# pygame.draw.rect(surf, (0, 200, 50), (100, 100, 200, 300))

# font = pygame.font.Font(None, 36)
# text = font.render("PyGame is cool", 1, (0, 0, 0))
# surf.blit(text, (100, 50))
#
# s1 = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
# s1.fill((200, 200, 200, 0))
# pygame.draw.rect(s1, (0, 0, 255), (10, 10, 50, 50), 5)
#
# s2 = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
# s2.fill((100, 200, 255, 0))
# pygame.draw.rect(s2, (0, 0, 255), (10, 10, 25, 25), 5)

# surf.blit(s1, (0, 0))
# surf.blit(s2, (100, 100))
im = pygame.image.load("64SmashMario.png")
pygame.init()
height = im.get_height()
width = im.get_width()
surf = pygame.display.set_mode((width, height), pygame.SRCALPHA)
for i in range(0, height):
    for r in range(0, width):
        pix = im.get_at((r, i))
        negR = 255 - pix[0]
        negB = 255 - pix[1]
        negG = 255 - pix[2]

        im.set_at((r, i), (negR, negB, negG))

surf.blit(im, (0, 0))

pygame.display.update()
input()
