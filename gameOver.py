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
small_font = pygame.font.Font(None, 22)
# Fonts
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 50)

background_image_winner = pygame.image.load("./imagenes/Winner.jpg")
background_image_gameover = pygame.image.load("./imagenes/gameOve.jpg")
background_image_winner   = pygame.transform.scale(background_image_winner, (WIDTH, HEIGHT))
background_image_gameover = pygame.transform.scale(background_image_gameover, (WIDTH, HEIGHT))


# Game states
GAME_OVER = 0
YOU_WIN = 1
NO_ONE_WINS = 2

# Sample game outcome
#game_outcome = GAME_OVER  # Change this value to YOU_WIN or NO_ONE_WINS to test different outcomes

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def finishing(game_outcome, red_count, green_count):
    clock = pygame.time.Clock()
    running = True
    textGreen = f'Yoshi Verde: {green_count}'
    textRed = f'Yoshi Rojo: {red_count}'
    while running:
        screen.fill(colors.WHITE)
        if game_outcome == GAME_OVER:

            screen.blit(background_image_gameover, (0, 0))
            draw_text('Game Over', font_large, colors.RED, screen, WIDTH // 2, HEIGHT // 2 - 220)
            draw_text(textGreen, font_small, colors.NARANJA, screen, WIDTH // 2, HEIGHT // 2 + 115)
            draw_text(textRed, font_small, colors.NARANJA, screen, WIDTH // 2, HEIGHT // 2 + 150)
        elif game_outcome == YOU_WIN:
            screen.blit(background_image_winner, (0, 0))
            draw_text('You Win', font_large, colors.GREEN, screen, WIDTH // 2, HEIGHT // 2 - 220)
            draw_text(textGreen, font_small, colors.WHITE, screen, WIDTH // 2, HEIGHT // 2 + 115)
            draw_text(textRed, font_small, colors.WHITE, screen, WIDTH // 2, HEIGHT // 2 + 150)
        elif game_outcome == NO_ONE_WINS:
            screen.blit(background_image_winner, (0, 0))
            draw_text('No One Wins', font_large, colors.GREY, screen, WIDTH // 2, HEIGHT // 2 - 220)
            draw_text(textGreen, font_small, colors.BLACK, screen, WIDTH // 2, HEIGHT // 2 - 115)
            draw_text(textRed, font_small, colors.BLACK, screen, WIDTH // 2, HEIGHT // 2 - 150)
        # Draw button
        button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 180, 300, 75)
        pygame.draw.rect(screen, colors.RED, button_rect)
        draw_text('Jugar de nuevo', font_small, colors.WHITE, screen, WIDTH // 2, HEIGHT // 2 + 215)
        
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
                    clear_board()
                    main()

                    print("Button clicked, reset the game!")

        pygame.display.flip()
        clock.tick(30)