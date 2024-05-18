import pygame
import sys
from settings import clock, screen
from colors import BLACK, WHITE, GREY, BLUE1, BLUE2, BLUE3
# Inicialización de Pygame
pygame.init()

pygame.display.set_caption("Yoshi's World")
font = pygame.font.Font(None, 36)
background_image = pygame.image.load("./imagenes/inicio.jpg")
new_width = 500  # Nueva anchura deseada
new_height = 550  # Nueva altura deseada
background_image = pygame.transform.scale(background_image, (new_width, new_height))
pygame.mixer.music.load("./audios/play.mp3")

sound_icon = pygame.image.load("./imagenes/sound.png")
sound_icon = pygame.transform.scale(sound_icon, (50, 50))
stop_sound_icon = pygame.image.load("./imagenes/stop_sound.png")
stop_sound_icon = pygame.transform.scale(stop_sound_icon, (50, 50))


def select_level():
    levels = {"Principiante": 2, "Amateur": 4, "Experto": 6}
    level_rects = []
    for index, (level, difficulty) in enumerate(levels.items()):
        rect = pygame.Rect(50, 300 + index * 60, 400, 50)
        level_rects.append((level, difficulty, rect))

    pygame.mixer.music.play(-1) 
    sound_on = True
    blue_colors = [BLUE1, BLUE2, BLUE3]

    while True:
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
        for level, difficulty, rect in level_rects:
            color_index = (difficulty // 2) % len(blue_colors)  # Ajustar índice para acceder a la lista
            pygame.draw.rect(screen, blue_colors[color_index], rect)
            text_surf = font.render(f"{level}", True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)


        sound_button_rect = pygame.Rect(10, 10, 50, 50)  # Tamaño del botón igual al tamaño del icono
        sound_icon_to_draw = stop_sound_icon if sound_on else sound_icon
        screen.blit(sound_icon_to_draw, sound_button_rect.topleft)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Silenciar/escuchar música al hacer clic en el botón
                if sound_button_rect.collidepoint(x, y):
                    if sound_on:
                        pygame.mixer.music.pause()
                        sound_on = False
                    else:
                        pygame.mixer.music.unpause()
                        sound_on = True
                else:
                    for level, difficulty, rect in level_rects:
                        if rect.collidepoint(x, y):
                            return level, difficulty

        pygame.display.flip()
        clock.tick(60)