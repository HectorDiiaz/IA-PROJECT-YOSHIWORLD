import pygame
import sys
from settings import clock, screen
from colors import BLACK, WHITE, GREY
# Inicialización de Pygame
pygame.init()

pygame.display.set_caption("Yoshi's World")
font = pygame.font.Font(None, 36)


def select_level():
    levels = ["Principiante", "Amateur", "Experto"]
    level_rects = []
    for index, level in enumerate(levels):
        rect = pygame.Rect(50, 150 + index * 60, 400, 50)
        level_rects.append((level, rect))

    while True:
        screen.fill(BLACK)
        for level, rect in level_rects:
            pygame.draw.rect(screen, GREY, rect)
            text_surf = font.render(level, True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for level, rect in level_rects:
                    if rect.collidepoint(x, y):
                        return level

        pygame.display.flip()
        clock.tick(60)