import pygame

clock = pygame.time.Clock()

# Ajusta la altura de la pantalla para incluir el recuadro negro
board_size = 8
square_size = 500 // board_size
header_height = square_size  # Altura del recuadro negro
screen_size = (500, 500 + header_height)

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Yoshi's World")

# Estado del tablero, 0 = sin pintar, 1 = verde, 2 = rojo
board = [[0] * board_size for _ in range(board_size)]

# Movimientos en L como un caballo de ajedrez
knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

yoshi_green_img = pygame.image.load('./imagenes/green.png').convert_alpha()
yoshi_red_img = pygame.image.load('./imagenes/red.png').convert_alpha()
yoshi_green_img = pygame.transform.scale(yoshi_green_img, (square_size, square_size))
yoshi_red_img = pygame.transform.scale(yoshi_red_img, (square_size, square_size))
