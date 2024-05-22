import pygame
import sys
import colors

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 550

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Interface")

# Fonts
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 22)

background_image_winner = pygame.image.load("./imagenes/Winner.jpg")
background_image_gameover = pygame.image.load("./imagenes/gameOve.jpg")
background_image_empate = pygame.image.load("./imagenes/empate.jpg")
background_image_winner = pygame.transform.scale(background_image_winner, (WIDTH, HEIGHT))
background_image_gameover = pygame.transform.scale(background_image_gameover, (WIDTH, HEIGHT))
background_image_empate = pygame.transform.scale(background_image_empate, (WIDTH, HEIGHT))

# Game states
GAME_OVER = 0
YOU_WIN = 1
NO_ONE_WINS = 2

# Sample game outcome
# game_outcome = GAME_OVER  # Change this value to YOU_WIN or NO_ONE_WINS to test different outcomes

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_rounded_rect(surface, color, rect, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

def finishing(game_outcome, red_count, green_count):
    clock = pygame.time.Clock()
    running = True
    textGreen = f'Yoshi Verde: {green_count}'
    textRed = f'Yoshi Rojo: {red_count}'
    
    if game_outcome == GAME_OVER:
        pygame.mixer.music.load("./audios/game_over.mp3")
        pygame.mixer.music.play()
    elif game_outcome == YOU_WIN:
        pygame.mixer.music.load("./audios/winner.mp3")
        pygame.mixer.music.play()
    elif game_outcome == NO_ONE_WINS:
        pygame.mixer.music.load("./audios/emp.mp3")
        pygame.mixer.music.play()
    
    while running:
        screen.fill(colors.WHITE)
        rect_width, rect_height = 350, 240
        rect_x, rect_y = WIDTH // 2 - rect_width // 2, HEIGHT // 2 - rect_height // 2 + 140
        if game_outcome == GAME_OVER:
            screen.blit(background_image_gameover, (0, 0))
            draw_text('Game Over', font_large, colors.RED, screen, WIDTH // 2, HEIGHT // 2 - 220)
            draw_text(textGreen, font_small, colors.NARANJA, screen, WIDTH // 2, HEIGHT // 2 + 115)
            draw_text(textRed, font_small, colors.NARANJA, screen, WIDTH // 2, HEIGHT // 2 + 150)
        elif game_outcome == YOU_WIN:
            screen.blit(background_image_winner, (0, 0))
            draw_text('You Win', font_large, colors.WHITE, screen, WIDTH // 2, HEIGHT // 2 - 220)
            draw_text(textGreen, font_small, colors.WHITE, screen, WIDTH // 2, HEIGHT // 2 + 115)
            draw_text(textRed, font_small, colors.WHITE, screen, WIDTH // 2, HEIGHT // 2 + 150)
        elif game_outcome == NO_ONE_WINS:
            screen.blit(background_image_empate, (0, 0))
            

            
            bg = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
            bg.fill((0, 0, 0, 217))  # Rellenar con el color negro con 85% de opacidad (255 * 0.85 = 217)

        
            draw_rounded_rect(bg, (0, 0, 0, 217), bg.get_rect(), 0)
            screen.blit(bg, (rect_x, rect_y))
            
            margin_top = 20

            draw_text('No One Wins', font_large, colors.RED, screen, WIDTH // 2, rect_y + margin_top + 10)
            draw_text(textGreen, font_small, colors.WHITE, screen, WIDTH // 2, rect_y + margin_top + 70)
            draw_text(textRed, font_small, colors.WHITE, screen, WIDTH // 2, rect_y + margin_top + 115)

        # Draw button
        button_rect = pygame.Rect(WIDTH // 2 - 150, rect_y + rect_height - 80, 300, 75)
        pygame.draw.rect(screen, colors.RED, button_rect, border_radius=0)
        draw_text('Jugar de nuevo', font_small, colors.WHITE, screen, WIDTH // 2, rect_y + rect_height - 40)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Reset game or restart logic goes here
                    from gameBoard import main
                    from gameBoard import clear_board
                    pygame.mixer.music.load("./audios/play.mp3")
                    pygame.mixer.music.play()
                    clear_board()
                    main()
                    print("Button clicked, reset the game!")

        pygame.display.flip()
        clock.tick(30)

# Ejemplo de llamada a la función finishing con NO_ONE_WINS
# finishing(NO_ONE_WINS, 10, 8)
