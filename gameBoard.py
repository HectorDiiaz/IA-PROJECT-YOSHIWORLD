import pygame
import sys
import random
import time
from level import select_level
from settings import clock, screen_size, board_size, square_size, knight_moves, board, screen, yoshi_green_img,yoshi_red_img
from colors import BLACK, WHITE, GREEN, GREY, RED
from nodo import Nodo
from gameOver import finishing
from sound_button import toggle_sound 


pygame.init()

#SONIDO 
sound_icon = pygame.image.load("./imagenes/sound_w.png")
sound_icon = pygame.transform.scale(sound_icon, (50, 50))
stop_sound_icon = pygame.image.load("./imagenes/stop_sound_w.png")
stop_sound_icon = pygame.transform.scale(stop_sound_icon, (50, 50))
sound_on = True 
sound_button_rect = pygame.Rect(5, 0, 50, 50)  
sound_icon_to_draw = stop_sound_icon if sound_on else sound_icon
screen.blit(sound_icon_to_draw, sound_button_rect.topleft)


green_count = 0
red_count = 0
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 22)

background_img = pygame.image.load("./imagenes/fondo.jpeg")
background_img   = pygame.transform.scale(background_img, (500, 550))

central_squares = [(2,2), (2,3), (2,4), (2,5), (3,2), (3,3), (3,4), (3,5), (4,2), (4,3), (4,4), (4,5), (5,2), (5,3), (5,4), (5,5)]


def is_valid_move(row, col, player, yoshi_green, yoshi_red):
    if player == 1:
        current_pos = yoshi_green
    else:
        current_pos = yoshi_red

    possible_moves = [(current_pos[0] + dx, current_pos[1] + dy) for dx, dy in knight_moves]
    return (row, col) in possible_moves and 0 <= row < board_size and 0 <= col < board_size and board[row][col] == 0

def handle_click(x, y, player, yoshi_green, yoshi_red):
    if y < 50:  
        return None, player
    row = (y - 50) // square_size  
    col = x // square_size
    if is_valid_move(row, col, player, yoshi_green, yoshi_red):
        board[row][col] = player
        return (row, col), 3 - player  
    return None, player

def draw_board(turn, yoshi_green, yoshi_red):
    global green_count, red_count, sound_on
    screen.fill(BLACK)  # Limpia la pantalla

    # Dibujar la imagen de fondo
    screen.blit(background_img, (0, 0))

    # Contar casillas pintadas por cada jugador
    green_count = sum(row.count(1) for row in board)
    red_count = sum(row.count(2) for row in board)

    # Mostrar la cantidad de casillas pintadas por cada jugador
    score_text = f"Yoshi Verde: {green_count}  |  Yoshi Rojo: {red_count}"
    score_surface = font.render(score_text, True, BLACK)
    turn_text_rect = score_surface.get_rect(center=(screen_size[0] // 2, 25))
    screen.blit(score_surface, turn_text_rect)

    # Dibuja las casillas del tablero con opacidad para las casillas blancas
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == 0:
                s = pygame.Surface((square_size, square_size))  # Tamaño de la casilla
                s.set_alpha(150)  # Nivel de opacidad
                s.fill(WHITE)  # Rellenar la superficie
                screen.blit(s, (col * square_size, row * square_size + 50))
                # Dibuja el borde gris oscuro
                pygame.draw.rect(screen, GREY, (col * square_size, row * square_size + 50, square_size, square_size), 1)
            else:
                color = GREEN if board[row][col] == 1 else RED
                pygame.draw.rect(screen, color, (col * square_size, row * square_size + 50, square_size, square_size))

    # Dibuja la cuadrícula
    for i in range(board_size + 1):
        pygame.draw.line(screen, BLACK, (0, i * square_size + 50), (screen_size[0], i * square_size + 50))
        pygame.draw.line(screen, BLACK, (i * square_size, 50), (i * square_size, screen_size[0] + 50))

    # Dibuja las imágenes de Yoshi
    screen.blit(yoshi_green_img, (yoshi_green[1] * square_size, yoshi_green[0] * square_size + 50))
    screen.blit(yoshi_red_img, (yoshi_red[1] * square_size, yoshi_red[0] * square_size + 50))

    # Botón de sonido
    sound_button_rect = pygame.Rect(5, 0, 50, 50)
    sound_icon_to_draw = stop_sound_icon if sound_on else sound_icon
    screen.blit(sound_icon_to_draw, sound_button_rect.topleft)

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

def tree(positionRojo, positionVerde, level):
    nodo_inicial = Nodo(positionRojo, utilidad=None, minmax="MAX", tablero=board, estadoContrincante=positionVerde, nodo_padre=None)
    expandirArbol(nodo_inicial, level)
    calcular_utilidad(nodo_inicial)
    # imprimir_nodos_desde_raiz(nodo_inicial)
    return get_next_move(nodo_inicial)[1]

def imprimir_nodos_desde_raiz(nodo):

    print(f"Profundidad: {nodo.profundidad} | Tipo de nodo (min/max): {nodo.minmax} | Estado: {nodo.estado} | Utilidad: {nodo.utilidad} | Nodo padre: {nodo.nodo_padre.estado if nodo.nodo_padre else 'None'}")
    print("--------------------------------------")
    [imprimir_nodos_desde_raiz(hijo) for hijo in nodo.hijos]

def calcular_utilidad(nodo):
    if not nodo.hijos:  # Si el nodo no tiene hijos, es una hoja
        # Movimientos disponibles para cada Yoshi
        verde_movimientos = count_valid_moves2(nodo.estado, nodo.tablero)
        rojo_movimientos = count_valid_moves2(nodo.estadoContrincante, nodo.tablero)

        # Casillas centrales pintadas por cada Yoshi
        verde_centrales = sum(1 for row, col in central_squares if nodo.tablero[row][col] == 1)
        rojo_centrales = sum(1 for row, col in central_squares if nodo.tablero[row][col] == 2)
      
        # print("Movimientos disponibles verde: (",nodo.estado,") ", verde_movimientos, "Movimientos disponibles rojo:  (",nodo.estadoContrincante,") ", rojo_movimientos, "Resultado: ", (verde_movimientos-rojo_movimientos))
        # print("Casillas centrales verde: ", verde_centrales, "Casillas centrales rojo: ", rojo_centrales, "Resultado: ", (verde_centrales-rojo_centrales))
        # Heurística combinada
        nodo.utilidad = (
                        (rojo_movimientos - verde_movimientos ) + 
                        (rojo_centrales - verde_centrales ))
        
        # print("RESULTADO DE LA UTILIDAD: ", (verde_movimientos - rojo_movimientos) + 
                        # (verde_centrales - rojo_centrales))
        
        return nodo.utilidad

    # Llamada recursiva para calcular la utilidad de los hijos
    utilidades_hijos = [calcular_utilidad(hijo) for hijo in nodo.hijos]

    # Asignar la utilidad al nodo actual basado en su tipo (MIN o MAX)
    if nodo.minmax == "MAX":
        nodo.utilidad = max(utilidades_hijos)
    else:
        nodo.utilidad = min(utilidades_hijos)
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
            nodoAExpandir.agregar_hijo(nodo)
            #print("POSICION", nodo.nodo_padre.estado, nodo.estado, nodo.minmax) 
            expandirArbol(nodo, depth - 1)
        else:

            nodo = Nodo(move, utilidad=None, minmax="MAX", tablero=nodoAExpandir.tablero,  estadoContrincante=nodoAExpandir.estado, nodo_padre=nodoAExpandir)
            if nodo.nodo_padre is not None:
                nodo.profundidad = nodo.nodo_padre.profundidad + 1
            nodo.agregarPosicionTablero()
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

def clear_board():
    global board
    # Reset the board
    for row in range(board_size):
        for col in range(board_size):
            board[row][col] = 0

def main():
    global sound_on
    level, difficulty = select_level()
    yoshi_red = (random.randint(0, 7), random.randint(0, 7))
    yoshi_green = (random.randint(0, 7), random.randint(0, 7))
   
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
            time.sleep(0.2)  # Delay for 2 seconds
            yoshi_green = tree(yoshi_green, yoshi_red, difficulty)
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
                    if sound_button_rect.collidepoint(x, y):
                        sound_on = not sound_on
                        if sound_on:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()

        player_pos = yoshi_green if turn == 1 else yoshi_red
        player_valid_moves = any(is_valid_move(player_pos[0] + dx, player_pos[1] + dy, turn, yoshi_green, yoshi_red) for dx, dy in knight_moves)
        if not player_valid_moves:
            turn = 3 - turn
        draw_board(turn, yoshi_green, yoshi_red)
        pygame.display.flip()
        clock.tick(60)
    if not check_valid_moves(yoshi_green, yoshi_red):
        pygame.mixer.music.pause()
        GAME_OVER = 0
        YOU_WIN = 1
        NO_ONE_WINS = 2
        if red_count > green_count:
            print("LOSER GREEN")
            finishing(YOU_WIN, red_count, green_count)
        elif red_count < green_count:
            finishing(GAME_OVER, red_count, green_count)
        else:
            finishing(NO_ONE_WINS, red_count, green_count)
    pygame.quit()
    sys.exit()