import pygame
import sys
import random
from level import select_level
from settings import clock, screen_size, board_size, square_size, knight_moves, board, screen, yoshi_green_img,yoshi_red_img
from colors import BLACK, WHITE, GREEN, GREY, RED
from nodo import Nodo

pygame.init()

font = pygame.font.Font(None, 36)

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
#Prueba terminal
def check_valid_moves(yoshi_green, yoshi_red):
    green_valid_moves = any(is_valid_move(yoshi_green[0] + dx, yoshi_green[1] + dy, 1, yoshi_green, yoshi_red) for dx, dy in knight_moves)
    red_valid_moves = any(is_valid_move(yoshi_red[0] + dx, yoshi_red[1] + dy, 2, yoshi_green, yoshi_red) for dx, dy in knight_moves)
    return green_valid_moves or red_valid_moves

def valid_moves(position, current_board, current_player, other_yoshi_pos):
    positionMov = []
    yoshi_pos = position if current_player == 2 else other_yoshi_pos
    
    for dx, dy in knight_moves:
        new_row = yoshi_pos[0] + dx
        new_col = yoshi_pos[1] + dy
        if 0 <= new_row < board_size and 0 <= new_col < board_size and current_board[new_row][new_col] == 0:
            positionMov.append((new_row, new_col))
            
    return positionMov

def expand_node(node, depth, current_board, current_player, other_yoshi_pos):
    if depth == 0:
        return
    
    movimientos = valid_moves(node.estado, current_board, current_player, other_yoshi_pos)
    next_player = 1 if current_player == 2 else 2  # Alternar entre los jugadores
    for move in movimientos:
        child_node = Nodo(estado=move, utilidad=None, minmax="Min" if next_player == 1 else "Max", nodo_padre=node, profundidad=node.profundidad + 1)
        node.agregar_hijo(child_node)
        # Crear una copia del tablero antes de hacer el próximo movimiento
        next_board = [row[:] for row in current_board]
        next_board[move[0]][move[1]] = next_player

        next_yoshi_pos = node.estado if next_player == current_player else other_yoshi_pos

        expand_node(child_node, depth - 1, next_board, next_player, next_yoshi_pos)
    

def tree(position, depth,other_yoshi_pos ):
    root = Nodo(estado=position, utilidad=None, minmax="Max", profundidad=0)
    initial_board = [row[:] for row in board]
    expand_node(root, depth, initial_board, current_player=2, other_yoshi_pos=other_yoshi_pos)
    return root

# def heuristica(yoshi_act, yoshi_riv):
#     yoshi_act = count_valid_moves(yoshi_act)
#     yoshi_riv = count_valid_moves(yoshi_riv)

#     return yoshi_act - yoshi_riv

def obtener_nodos_hoja(nodo):
    if not nodo.hijos:  # Si el nodo no tiene hijos, es una hoja
        return [nodo.estado]
    nodos_hoja = []
    for hijo in nodo.hijos:
        nodos_hoja.extend(obtener_nodos_hoja(hijo))
    return nodos_hoja

def main():
    level = select_level()
    print(f"Selected Level: {level}")
    # Initial positions for both Yoshis
    yoshi_green = (1, 3)
    # yoshi_green = (random.randint(0, 7), random.randint(0, 7))
    # yoshi_red = (random.randint(0, 7), random.randint(0, 7))
    yoshi_red = (1,7)
    while yoshi_red == yoshi_green:
        yoshi_red = (random.randint(0, 7), random.randint(0, 7))
    board[yoshi_green[0]][yoshi_green[1]] = 1
    board[yoshi_red[0]][yoshi_red[1]] = 2

    turn = 2  # Red starts

    running = True
    while running:
        if turn == 2:
            raiz = tree(yoshi_red, depth=2, other_yoshi_pos=yoshi_green)
            nodos_hoja = obtener_nodos_hoja(raiz)
            print("Nodos hoja:", nodos_hoja)  # Imprimir los nodos hoja para propósitos de prueba
            turn = 1
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