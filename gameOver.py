import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 550
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Interface")

# Fonts
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 50)

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

def finishing(game_outcome):
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill(WHITE)
        
        if game_outcome == GAME_OVER:
            draw_text('Game Over', font_large, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
        elif game_outcome == YOU_WIN:
            draw_text('You Win', font_large, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
        elif game_outcome == NO_ONE_WINS:
            draw_text('No One Wins', font_large, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
        
        # Draw button
        button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 75)
        pygame.draw.rect(screen, RED, button_rect)
        draw_text('Jugar de nuevo', font_small, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 87)
        
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