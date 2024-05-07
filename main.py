import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración del tamaño de la ventana
screen_size = (500, 500)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Yoshi's World")

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)

# Configuración de la fuente
font = pygame.font.Font(None, 36)

# Configuración del reloj
clock = pygame.time.Clock()

# Dimensiones del tablero
board_size = 8
square_size = screen_size[0] // board_size

# Estado del tablero, 0 = sin pintar, 1 = verde, 2 = rojo
board = [[0] * board_size for _ in range(board_size)]

# Movimientos en L como un caballo de ajedrez
knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

# Carga y escala imágenes
yoshi_green_img = pygame.image.load('./imagenes/green.png').convert_alpha()
yoshi_red_img = pygame.image.load('./imagenes/red.png').convert_alpha()
yoshi_green_img = pygame.transform.scale(yoshi_green_img, (square_size, square_size))
yoshi_red_img = pygame.transform.scale(yoshi_red_img, (square_size, square_size))

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

def draw_board(turn, yoshi_green, yoshi_red):
    screen.fill(BLACK)  # Limpia la pantalla
    # Dibuja las casillas del tablero
    for row in range(board_size):
        for col in range(board_size):
            color = WHITE if board[row][col] == 0 else GREEN if board[row][col] == 1 else RED
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))
    # Dibuja la cuadrícula
    for i in range(board_size + 1):
        pygame.draw.line(screen, GREY, (0, i * square_size), (screen_size[0], i * square_size))
        pygame.draw.line(screen, GREY, (i * square_size, 0), (i * square_size, screen_size[0]))
    # Dibuja las imágenes de Yoshi
    screen.blit(yoshi_green_img, (yoshi_green[1] * square_size, yoshi_green[0] * square_size))
    screen.blit(yoshi_red_img, (yoshi_red[1] * square_size, yoshi_red[0] * square_size))
    # Renderiza y dibuja el texto del turno
    turn_text = "Turno de Yoshi Verde" if turn == 1 else "Turno de Yoshi Rojo"
    text_surface = font.render(turn_text, True, GREEN if turn == 1 else RED)
    screen.blit(text_surface, (10, 10))  # Ajusta la posición según necesites

def is_valid_move(row, col, player, yoshi_green, yoshi_red):
    if player == 1:
        current_pos = yoshi_green
    else:
        current_pos = yoshi_red

    possible_moves = [(current_pos[0] + dx, current_pos[1] + dy) for dx, dy in knight_moves]
    return (row, col) in possible_moves and 0 <= row < board_size and 0 <= col < board_size and board[row][col] == 0

def handle_click(x, y, player, yoshi_green, yoshi_red):
    row = y // square_size
    col = x // square_size
    if is_valid_move(row, col, player, yoshi_green, yoshi_red):
        board[row][col] = player
        return (row, col), 3 - player  # Alternates between 1 and 2
    return None, player

#Prueba terminal
def check_valid_moves(yoshi_green, yoshi_red):
    green_valid_moves = any(is_valid_move(yoshi_green[0] + dx, yoshi_green[1] + dy, 1, yoshi_green, yoshi_red) for dx, dy in knight_moves)
    red_valid_moves = any(is_valid_move(yoshi_red[0] + dx, yoshi_red[1] + dy, 2, yoshi_green, yoshi_red) for dx, dy in knight_moves)
    return green_valid_moves or red_valid_moves

def count_valid_moves(position):
    count = 0
    for dx, dy in knight_moves:
        new_row = position[0] + dx
        new_col = position[1] + dy
        if 0 <= new_row < board_size and 0 <= new_col < board_size and board[new_row][new_col] == 0:
            count += 1
    return count

def heuristica(yoshi_act, yoshi_riv):
    yoshi_act = count_valid_moves(yoshi_act)
    yoshi_riv = count_valid_moves(yoshi_riv)

    return yoshi_act - yoshi_riv
    
def main():
    level = select_level()
    print(f"Selected Level: {level}")

    # Initial positions for both Yoshis
    yoshi_green = (random.randint(0, 7), random.randint(0, 7))
    yoshi_red = (random.randint(0, 7), random.randint(0, 7))
    while yoshi_red == yoshi_green:
        yoshi_red = (random.randint(0, 7), random.randint(0, 7))

    board[yoshi_green[0]][yoshi_green[1]] = 1
    board[yoshi_red[0]][yoshi_red[1]] = 2

    turn = 2  # Red starts

    running = True
    while running:
        if not check_valid_moves(yoshi_green, yoshi_red):
            running = False
            continue
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                new_pos, new_turn = handle_click(x, y, turn, yoshi_green, yoshi_red)
                if new_pos:
                    turn = new_turn  # Update the turn
                    if turn == 2:
                        yoshi_green = new_pos
                    else:
                        yoshi_red = new_pos

                    if turn == 1:
                        player_pos = yoshi_green
                    else:
                        player_pos = yoshi_red

                    player_valid_moves = any(is_valid_move(player_pos[0] + dx, player_pos[1] + dy, turn, yoshi_green, yoshi_red) for dx, dy in knight_moves)
                    if not player_valid_moves:
                        # If the current player has no valid moves, switch the turn to the other player
                        turn = 3 - turn

        draw_board(turn, yoshi_green, yoshi_red)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()