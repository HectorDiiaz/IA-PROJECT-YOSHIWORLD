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

def count_valid_moves(position, board_act):
    positionMov = []
    for dx, dy in knight_moves:
        new_row = position[0] + dx
        new_col = position[1] + dy
        if 0 <= new_row < board_size and 0 <= new_col < board_size and board_act[new_row][new_col] == 0:
            positionMov.append((new_row, new_col))        
    return positionMov

def count_valid_moves2(position, board_act):
    positionMov = 0
    for dx, dy in knight_moves:
        new_row = position[0] + dx
        new_col = position[1] + dy
        if 0 <= new_row < board_size and 0 <= new_col < board_size and board_act[new_row][new_col] == 0:
            positionMov += 1         
    return positionMov

minmaxListPorExpandir = []
minmaxList2 = []
minmaxlist = []
def tree(positionRojo, positionVerde, level):
    nodo_inicial = Nodo(positionRojo, utilidad=None, minmax="MAX", tablero=board, estadoContrincante=positionVerde, nodo_padre=None)
    # print("Matriz inicial", nodo_inicial.tablero)
    minmaxListPorExpandir.append(nodo_inicial)
    expandirArbol(nodo_inicial, level)
    # print("NODOS", obtener_nodos_hoja(nodo_inicial))
    utilidad(nodo_inicial)
    calcular_utilidad(nodo_inicial)
    # print("New move", get_next_move(nodo_inicial)[1])
    return get_next_move(nodo_inicial)[1]


def calcular_utilidad(nodo):
    if not nodo.hijos:  # Si el nodo no tiene hijos, es una hoja
        verde = count_valid_moves2(nodo.estado, nodo.tablero)
        rojo = count_valid_moves2(nodo.estadoContrincante, nodo.tablero)
        nodo.utilidad = rojo - verde
        
        #nodo.utilidad = rojom - verdem
        # print("Hoja -> Nodo: ", nodo.estado, "Movimientos validos (Verde):", verde, " - Movimientos validos (Rojo):", rojo, " Utilidad: ", nodo.utilidad)
        return nodo.utilidad
    # Llamada recursiva para calcular la utilidad de los hijos
    utilidades_hijos = [calcular_utilidad(hijo) for hijo in nodo.hijos]
    # Asignar la utilidad al nodo actual basado en su tipo (MIN o MAX)
    if nodo.minmax == "MAX":
        nodo.utilidad = max(utilidades_hijos)
    else:
        nodo.utilidad = min(utilidades_hijos)
    #print("Nodo: ", nodo.estado, " Tipo: ", nodo.minmax, " Utilidad calculada: ", nodo.utilidad)
    return nodo.utilidad

def get_next_move(nodo_inicial):
    if not nodo_inicial.hijos:
        return None, None 

    max_utilidad = float('-inf')
    max_node = None
    
    for hijo in nodo_inicial.hijos:
        if hijo.utilidad > max_utilidad:
            max_utilidad = hijo.utilidad
            max_node = hijo
    
    return max_utilidad, max_node.estado
def utilidad(nodo_inicial):
    for hijo in obtener_nodos_hoja(nodo_inicial):
        verde = count_valid_moves2(hijo.estado, hijo.tablero) 
        rojo = count_valid_moves2(hijo.estadoContrincante, hijo.tablero)
        hijo.utilidad = rojo - verde
        #print("Padre: ", hijo.nodo_padre.estado, "nodo: ",
               #hijo.estado,"movimientos validos: ",verde," - ", "contrincante : ", hijo.estadoContrincante, "numeros validos: ",rojo, "Utilidad: ", hijo.utilidad)


def expandirArbol(nodoAExpandir, depth=0):
    if depth == 0:
        return 
    # 1. Obtener posiciones validad para ese nodo
    if(nodoAExpandir.minmax=="MAX"):
        valid_moves = count_valid_moves(nodoAExpandir.estado, nodoAExpandir.tablero)
    else:
        valid_moves = count_valid_moves(nodoAExpandir.estadoContrincante, nodoAExpandir.tablero)
    # 2. Crear los nodos para esas posiciones validas y añadirlos a las listas
    for move in valid_moves:
        if(nodoAExpandir.minmax=="MAX"):
         
            nodo = Nodo(move, utilidad=None, minmax="MIN", tablero=nodoAExpandir.tablero, estadoContrincante=nodoAExpandir.estadoContrincante, nodo_padre=nodoAExpandir)
            if nodo.nodo_padre is not None:
                nodo.profundidad = nodo.nodo_padre.profundidad + 1
            nodo.agregarPosicionTablero()
            minmaxList2.append(nodo)
            nodoAExpandir.agregar_hijo(nodo)
            #print("POSICION", nodo.nodo_padre.estado, nodo.estado, nodo.minmax) 
            expandirArbol(nodo, depth - 1)
        else:

            nodo = Nodo(move, utilidad=None, minmax="MAX", tablero=nodoAExpandir.tablero,  estadoContrincante=nodoAExpandir.estado, nodo_padre=nodoAExpandir)
            if nodo.nodo_padre is not None:
                nodo.profundidad = nodo.nodo_padre.profundidad + 1
            nodo.agregarPosicionTablero()
            minmaxList2.append(nodo)
            nodoAExpandir.agregar_hijo(nodo)
            #print("POSICION", nodo.nodo_padre.estado, nodo.estado, nodo.minmax)
            expandirArbol(nodo, depth - 1) 

def obtener_nodos_hoja(nodo):
    if not nodo.hijos:  # Si el nodo no tiene hijos, es una hoja
        return [nodo]
    nodos_hoja = []
    for hijo in nodo.hijos:
        nodos_hoja.extend(obtener_nodos_hoja(hijo))
    return nodos_hoja

def main():
    level, difficulty = select_level()
    yoshi_green = (0, 0)
    yoshi_red = (0, 7)
    while yoshi_red == yoshi_green:
        yoshi_red = (random.randint(0, 7), random.randint(0, 7))
    board[yoshi_green[0]][yoshi_green[1]] = 1
    board[yoshi_red[0]][yoshi_red[1]] = 2

    turn = 1  # Green starts

    running = True
    while running:
        if not check_valid_moves(yoshi_green, yoshi_red):
            running = False
            continue
        if turn == 1:
            yoshi_green = tree(yoshi_green,yoshi_red, difficulty)
            board[yoshi_green[0]][yoshi_green[1]] = 1
            turn = 2
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    new_pos, new_turn = handle_click(x, y, turn, yoshi_green, yoshi_red)
                    if new_pos:
                        turn = new_turn
                        if turn == 2:
                            yoshi_green = new_pos
                        else:
                            yoshi_red = new_pos

        player_pos = yoshi_green if turn == 1 else yoshi_red
        player_valid_moves = any(is_valid_move(player_pos[0] + dx, player_pos[1] + dy, turn, yoshi_green, yoshi_red) for dx, dy in knight_moves)
        if not player_valid_moves:
            turn = 3 - turn
        draw_board(turn, yoshi_green, yoshi_red)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

