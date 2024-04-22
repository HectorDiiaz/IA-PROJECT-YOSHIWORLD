import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Configuración del tamaño de la ventana
screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Yoshi's World")

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)  # Color para la cuadrícula
# Configuración de la fuente
font = pygame.font.Font(None, 36)  # None usa la fuente predeterminada de Pygame

# Configuración del reloj
clock = pygame.time.Clock()

# Dimensiones del tablero
board_size = 8
square_size = screen_size[0] // board_size

# Estado del tablero, 0 = sin pintar, 1 = verde, 2 = rojo
board = [[0] * board_size for _ in range(board_size)]

# Movimientos en L como un caballo de ajedrez
knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

yoshi_green_img = pygame.image.load('./imagenes/green.png').convert_alpha()
yoshi_red_img = pygame.image.load('./imagenes/red.png').convert_alpha()
yoshi_green_img = pygame.transform.scale(yoshi_green_img, (square_size, square_size))
yoshi_red_img = pygame.transform.scale(yoshi_red_img, (square_size, square_size))

def draw_board(turn):
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

    # Dibujar Yoshis
    green_x = yoshi_green[1] * square_size
    green_y = yoshi_green[0] * square_size
    red_x = yoshi_red[1] * square_size
    red_y = yoshi_red[0] * square_size
    screen.blit(yoshi_green_img, (green_x, green_y))
    screen.blit(yoshi_red_img, (red_x, red_y))


def is_valid_move(row, col, player):
    if player == 1:
        current_pos = yoshi_green
    else:
        current_pos = yoshi_red

    valid_moves = [(current_pos[0] + dx, current_pos[1] + dy) for dx, dy in knight_moves]
    return (row, col) in valid_moves and 0 <= row < board_size and 0 <= col < board_size and board[row][col] == 0

def handle_click(x, y, player):
    row = y // square_size
    col = x // square_size
    if is_valid_move(row, col, player):
        board[row][col] = player
        if player == 1:
            return (row, col), 2  # Return new position and next player
        else:
            return (row, col), 1
    return None, player  # No change if move is not valid

# Asignación inicial aleatoria para los dos Yoshi
import random
yoshi_green = (random.randint(0, 7), random.randint(0, 7))
yoshi_red = (random.randint(0, 7), random.randint(0, 7))
while yoshi_red == yoshi_green:
    yoshi_red = (random.randint(0, 7), random.randint(0, 7))

board[yoshi_green[0]][yoshi_green[1]] = 1
board[yoshi_red[0]][yoshi_red[1]] = 2

# Control del turno: 1 = verde, 2 = rojo. Ahora comenzará el rojo.
turn = 2

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            new_pos, turn = handle_click(x, y, turn)
            print("Turno: ", turn)
            if new_pos:
                if turn == 2:
                    yoshi_green = new_pos
                else:
                    yoshi_red = new_pos

    # Rellenar el fondo
    screen.fill(BLACK)

    # Dibujar el tablero y la cuadrícula
    draw_board(turn)

    # Actualizar la pantalla
    pygame.display.flip()

    # Mantener la tasa de refresco
    clock.tick(60)

# Salir de Pygame
pygame.quit()
sys.exit()
