import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# Variables globales
mapita = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,1,0,1,1,1,1,1,0,1,0,0,0,0,0,0,1,0,1],
    [1,0,0,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [3,3,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,3,3],
    [3,3,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,3,3],
    [3,3,1,0,1,1,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,1,1,0,1,3,3],
    [3,3,1,0,0,1,0,0,1,0,1,1,0,1,0,1,1,0,1,0,0,1,0,0,1,3,3],
    [3,3,1,1,0,1,0,1,1,0,1,1,0,1,0,1,1,0,1,1,0,1,0,1,1,3,3],
    [1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1],
    [3,3,1,0,1,1,1,0,1,0,1,1,1,3,1,1,1,0,1,0,1,1,1,0,1,3,3],
    [1,1,1,0,1,1,1,0,1,0,1,3,3,3,3,3,1,0,1,0,1,1,1,0,1,1,1],
    [3,3,1,0,1,1,1,0,1,0,1,3,3,3,3,3,1,0,1,0,1,1,1,0,1,3,3],
    [3,3,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,3,3],
    [3,3,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,3,3],
    [3,3,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,3,3],
    [3,3,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,3,3],
    [1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,0,1,1,0,1,0,1,1,0,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

CELL_SIZE = 5
ANCHO_MAPA = len(mapita[0])
ALTO_MAPA = len(mapita)

# Posición inicial del Pac-Man
pacman_x, pacman_y = 14.5, 18.5
pacman_starting_x, pacman_starting_y = pacman_x, pacman_y  # Guardar posición inicial
pacman_direction = 0
pacman_next_direction = None
velocidad_de_pacman = 0.1
angulo_de_boca = 0
apertura_de_boca = True
radio_de_pacman = 0.4 * CELL_SIZE
vidas_pacman = 3
game_over = False
invulnerable = False
invulnerable_timer = 0

# Colores
color_pacman = (1.0, 1.0, 0.0)
color_pared = (0.0, 0.4, 0.8)
color_pared_perimetro = (0.0, 0.7, 1.0)

# Definir las direcciones posibles como vectores
DIRECCIONES = {
    "derecha": [1, 0],
    "arriba": [0, -1],
    "izquierda": [-1, 0],
    "abajo": [0, 1]
}

# Convertir a diccionario para acceso más fácil
DIRECCIONES_LISTA = [
    DIRECCIONES["derecha"],
    DIRECCIONES["arriba"],
    DIRECCIONES["izquierda"],
    DIRECCIONES["abajo"]
]

# Direcciones opuestas
DIRECCIONES_OPUESTAS = {
    0: 2,
    1: 3,
    2: 0,
    3: 1
}

fantasmas = [
    {"color": (1.0, 0.0, 0.0), "posicion": [60, -80], "direccion": DIRECCIONES_LISTA[0], "dir_index": 0, "decision_timer": 0, "stuck_count": 0, "last_pos": [60, -80]},
    {"color": (0.0, 1.0, 0.0), "posicion": [65, -80], "direccion": DIRECCIONES_LISTA[0], "dir_index": 0, "decision_timer": 0, "stuck_count": 0, "last_pos": [60, -80]},
    {"color": (0.0, 0.0, 1.0), "posicion": [70, -80], "direccion": DIRECCIONES_LISTA[0], "dir_index": 0, "decision_timer": 0, "stuck_count": 0, "last_pos": [60, -80]},
    {"color": (1.0, 1.0, 0.0), "posicion": [60, -80], "direccion": DIRECCIONES_LISTA[0], "dir_index": 0, "decision_timer": 0, "stuck_count": 0, "last_pos": [60, -80]},
    {"color": (0.0, 1.0, 1.0), "posicion": [60, -80], "direccion": DIRECCIONES_LISTA[0], "dir_index": 0, "decision_timer": 0, "stuck_count": 0, "last_pos": [60, -80]},
]

velocidad = 0.5

def is_wall(x, y):
    col = int(x // CELL_SIZE)
    row = int(abs(y) // CELL_SIZE)
    if 0 <= row < len(mapita) and 0 <= col < len(mapita[0]):
        return mapita[row][col] == 1
    return True

def colision_con_paredes(x, y, radius):
    x_gl = x * CELL_SIZE
    y_gl = -y * CELL_SIZE
    check_points = []
    check_points.append((x_gl + radius, y_gl))
    check_points.append((x_gl, y_gl - radius))
    check_points.append((x_gl - radius, y_gl))
    check_points.append((x_gl, y_gl + radius))
    diagonal_offset = radius * 0.7071
    check_points.append((x_gl + diagonal_offset, y_gl + diagonal_offset))
    check_points.append((x_gl - diagonal_offset, y_gl + diagonal_offset))
    check_points.append((x_gl - diagonal_offset, y_gl - diagonal_offset))
    check_points.append((x_gl + diagonal_offset, y_gl - diagonal_offset))
    for point_x, point_y in check_points:
        if is_wall(point_x, point_y):
            return True
    return False

def can_move(x, y):
    return not colision_con_paredes(x, y, radio_de_pacman)

def toca_bolitas():
    col = int(pacman_x)
    row = int(pacman_y)
    if 0 <= row < len(mapita) and 0 <= col < len(mapita[0]):
        if mapita[row][col] == 0:
            mapita[row][col] = 3
            return True
        
    return False

def colision_de_fantasmas():
    global vidas_pacman, pacman_x, pacman_y, invulnerable, invulnerable_timer, game_over

    if invulnerable:
        return False

    pacman_gl_x = pacman_x * CELL_SIZE
    pacman_gl_y = -pacman_y * CELL_SIZE

    for fantasma in fantasmas:
        ghost_x, ghost_y = fantasma["posicion"]
        distance = math.sqrt((pacman_gl_x - ghost_x)**2 + (pacman_gl_y - ghost_y)**2)

        if distance < (radio_de_pacman + 2):
            vidas_pacman -= 1
            if vidas_pacman <= 0:
                return True  # Game over
            else:
                pacman_x, pacman_y = pacman_starting_x, pacman_starting_y
                pacman_direction = 0
                pacman_next_direction = None
                invulnerable = True
                invulnerable_timer = 180
                return False
    return False

def pon_pared(col, row):
    if not is_wall(col * CELL_SIZE, -row * CELL_SIZE):
        return

    x = col * CELL_SIZE
    y = -row * CELL_SIZE

    glColor3fv(color_pared)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + CELL_SIZE, y)
    glVertex2f(x + CELL_SIZE, y - CELL_SIZE)
    glVertex2f(x, y - CELL_SIZE)
    glEnd()

    glColor3fv(color_pared_perimetro)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x + CELL_SIZE, y)
    glVertex2f(x + CELL_SIZE, y - CELL_SIZE)
    glVertex2f(x, y - CELL_SIZE)
    glEnd()

def dibujar_bolitas(x, y, big=False):
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(6 if big else 2)
    glBegin(GL_POINTS)
    glVertex2f(x + CELL_SIZE / 2, y - CELL_SIZE / 2)
    glEnd()

def hacer_mapa():
    for row_idx, row in enumerate(mapita):
        for col_idx, cell in enumerate(row):
            x = col_idx * CELL_SIZE
            y = -row_idx * CELL_SIZE
            if cell == 1:
                pon_pared(col_idx, row_idx)
            elif cell == 0:
                dibujar_bolitas(x, y, big=False)

def draw_pacman():
    global angulo_de_boca, apertura_de_boca

    if invulnerable and invulnerable_timer % 10 >= 5:
        return

    if apertura_de_boca:
        angulo_de_boca += 3
        if angulo_de_boca >= 45:
            apertura_de_boca = False
    else:
        angulo_de_boca -= 3
        if angulo_de_boca <= 5:
            apertura_de_boca = True

    glPushMatrix()
    glTranslatef(pacman_x * CELL_SIZE, -pacman_y * CELL_SIZE, 0)

    rotation = 0
    if pacman_direction == 0:
        rotation = 0
    elif pacman_direction == 1:
        rotation = 90
    elif pacman_direction == 2:
        rotation = 180
    elif pacman_direction == 3:
        rotation = 270

    glRotatef(rotation, 0, 0, 1)

    glColor3fv(color_pacman)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0, 0)
    for angle in range(angulo_de_boca, 360 - angulo_de_boca + 1, 10):
        x = radio_de_pacman * math.cos(math.radians(angle))
        y = radio_de_pacman * math.sin(math.radians(angle))
        glVertex2f(x, y)
    glEnd()

    glPopMatrix()

def actualizar_pacman():
    global pacman_x, pacman_y, pacman_direction, pacman_next_direction

    current_cell_x = int(pacman_x)
    current_cell_y = int(pacman_y)
    cell_center_x = current_cell_x + 0.5
    cell_center_y = current_cell_y + 0.5

    is_centered_x = abs(pacman_x - cell_center_x) < 0.3
    is_centered_y = abs(pacman_y - cell_center_y) < 0.3

    if pacman_next_direction is not None:
        can_turn = False

        if ((pacman_direction == 0 or pacman_direction == 2) and
            (pacman_next_direction == 1 or pacman_next_direction == 3)):
            can_turn = is_centered_x
        elif ((pacman_direction == 1 or pacman_direction == 3) and
            (pacman_next_direction == 0 or pacman_next_direction == 2)):
            can_turn = is_centered_y
        else:
            can_turn = True

        if can_turn:
            test_x, test_y = pacman_x, pacman_y

            if pacman_next_direction == 0:
                test_x += velocidad_de_pacman
            elif pacman_next_direction == 1:
                test_y -= velocidad_de_pacman
            elif pacman_next_direction == 2:
                test_x -= velocidad_de_pacman
            elif pacman_next_direction == 3:
                test_y += velocidad_de_pacman

            if can_move(test_x, test_y):
                if pacman_next_direction == 0 or pacman_next_direction == 2:
                    if is_centered_y:
                        pacman_y = cell_center_y
                else:
                    if is_centered_x:
                        pacman_x = cell_center_x

                pacman_direction = pacman_next_direction
                pacman_next_direction = None

    next_x, next_y = pacman_x, pacman_y

    if pacman_direction == 0:
        next_x = pacman_x + velocidad_de_pacman
    elif pacman_direction == 1:
        next_y = pacman_y - velocidad_de_pacman
    elif pacman_direction == 2:
        next_x = pacman_x - velocidad_de_pacman
    elif pacman_direction == 3:
        next_y = pacman_y + velocidad_de_pacman

    if can_move(next_x, next_y):
        pacman_x, pacman_y = next_x, next_y
    else:
        if pacman_direction == 0 or pacman_direction == 2:
            if abs(pacman_y - int(pacman_y) - 0.5) < 0.3:
                pacman_y = int(pacman_y) + 0.5
        else:
            if abs(pacman_x - int(pacman_x) - 0.5) < 0.3:
                pacman_x = int(pacman_x) + 0.5

    toca_bolitas()

def posicion_a_celda(x, y):
    col = int(x / CELL_SIZE)
    row = int(abs(y) / CELL_SIZE)
    return col, row

def movimiento_de_fantasmas(x, y):
    return not colision_con_paredes(x / CELL_SIZE, -y / CELL_SIZE, radio_de_pacman)

def intersecciones_situacion(x, y):
    col, row = posicion_a_celda(x, y)
    cell_center_x = col * CELL_SIZE + CELL_SIZE / 2
    cell_center_y = -row * CELL_SIZE - CELL_SIZE / 2

    if abs(x - cell_center_x) > 0.8 or abs(y - cell_center_y) > 0.8:
        return False

    directions_available = 0
    for dx, dy in DIRECCIONES_LISTA:
        next_x = x + dx * CELL_SIZE
        next_y = y + dy * CELL_SIZE
        if movimiento_de_fantasmas(next_x, next_y):
            directions_available += 1

    return directions_available > 2

def direccionamiento_de_fantasmas(x, y, current_dir_index):
    possible_dirs = []
    opposite_dir = DIRECCIONES_OPUESTAS[current_dir_index]

    for i, (dx, dy) in enumerate(DIRECCIONES_LISTA):
        if i == opposite_dir:
            continue

        next_x = x + dx * velocidad * 2
        next_y = y + dy * velocidad * 2

        if movimiento_de_fantasmas(next_x, next_y):
            possible_dirs.append(i)

    if not possible_dirs:
        next_x = x + DIRECCIONES_LISTA[opposite_dir][0] * velocidad * 2
        next_y = y + DIRECCIONES_LISTA[opposite_dir][1] * velocidad * 2

        if movimiento_de_fantasmas(next_x, next_y):
            possible_dirs.append(opposite_dir)

    return possible_dirs

def actualizar_fantasmas():
    for fantasma in fantasmas:
        posicion = fantasma["posicion"]
        dir_index = fantasma["dir_index"]
        direccion = fantasma["direccion"]
        decision_timer = fantasma["decision_timer"]
        last_pos = fantasma["last_pos"]
        stuck_count = fantasma["stuck_count"]

        dist_moved = math.sqrt((posicion[0] - last_pos[0])**2 + (posicion[1] - last_pos[1])**2)
        if dist_moved < 0.1:
            fantasma["stuck_count"] = stuck_count + 1
        else:
            fantasma["stuck_count"] = 0

        fantasma["last_pos"] = posicion.copy()

        if fantasma["stuck_count"] > 5:
            new_dir_index = random.randint(0, 3)
            fantasma["dir_index"] = new_dir_index
            fantasma["direccion"] = DIRECCIONES_LISTA[new_dir_index]
            fantasma["stuck_count"] = 0
            fantasma["decision_timer"] = 0

        if decision_timer > 0:
            fantasma["decision_timer"] = decision_timer - 1

        en_interseccion = intersecciones_situacion(posicion[0], posicion[1])

        if en_interseccion and decision_timer <= 0:
            possible_dirs = direccionamiento_de_fantasmas(posicion[0], posicion[1], dir_index)

            if possible_dirs:
                if len(possible_dirs) >= 3 or random.random() < 0.7:
                    new_dir_index = random.choice(possible_dirs)
                    fantasma["dir_index"] = new_dir_index
                    fantasma["direccion"] = DIRECCIONES_LISTA[new_dir_index]
                    fantasma["decision_timer"] = 10

        next_x = posicion[0] + direccion[0] * velocidad
        next_y = posicion[1] + direccion[1] * velocidad

        if movimiento_de_fantasmas(next_x, next_y):
            posicion[0] = next_x
            posicion[1] = next_y
        else:
            possible_dirs = direccionamiento_de_fantasmas(posicion[0], posicion[1], dir_index)
            if possible_dirs:
                new_dir_index = random.choice(possible_dirs)
                fantasma["dir_index"] = new_dir_index
                fantasma["direccion"] = DIRECCIONES_LISTA[new_dir_index]
                fantasma["decision_timer"] = 10

def draw_fantasma(x, y, color):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glRotatef(180, 0, 0, 1)
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0, 0)
    for angle in range(0, 361, 10):
        x = 2 * math.cos(math.radians(angle))
        y = 2 * math.sin(math.radians(angle))
        glVertex2f(x, y)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(-2, 0)
    glVertex2f(2, 0)
    glVertex2f(2, 2)
    glVertex2f(-2, 2)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(-0.6, -0.6)
    for angle in range(0, 361, 10):
        x = 0.4 * math.cos(math.radians(angle))
        y = 0.4 * math.sin(math.radians(angle))
        glVertex2f(-0.6 + x, -0.6 + y)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0.6, -0.6)
    for angle in range(0, 361, 10):
        x = 0.4 * math.cos(math.radians(angle))
        y = 0.4 * math.sin(math.radians(angle))
        glVertex2f(0.6 + x, -0.6 + y)
    glEnd()

    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(-0.6, -0.6)
    for angle in range(0, 361, 10):
        x = 0.2 * math.cos(math.radians(angle))
        y = 0.2 * math.sin(math.radians(angle))
        glVertex2f(-0.6 + x, -0.6 + y)
    glEnd()
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0.6, -0.6)
    for angle in range(0, 361, 10):
        x = 0.2 * math.cos(math.radians(angle))
        y = 0.2 * math.sin(math.radians(angle))
        glVertex2f(0.6 + x, -0.6 + y)
    glEnd()
    glPopMatrix()

def draw_all_fantasmas():
    for fantasma in fantasmas:
        draw_fantasma(fantasma["posicion"][0], fantasma["posicion"][1], fantasma["color"])

def contador_de_vidas():
    for i in range(vidas_pacman):
        glPushMatrix()
        glTranslatef(3 + i * 5, -3, 0)

        glColor3fv(color_pacman)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)
        for angle in range(30, 330 + 1, 10):
            x = 2 * math.cos(math.radians(angle))
            y = 2 * math.sin(math.radians(angle))
            glVertex2f(x, y)
        glEnd()

        glPopMatrix()

def draw_game_over():
    # Posicionar el texto en el centro del mapa
    center_x = ANCHO_MAPA * CELL_SIZE / 2
    center_y = -ALTO_MAPA * CELL_SIZE / 2
    
    glPushMatrix()
    glTranslatef(center_x - 40, center_y, 0)
    glColor3f(1.0, 0.0, 0.0)  # Color rojo
    
    # Dibujar "GAME OVER" usando primitivas
    
    # Letra G
    glBegin(GL_LINE_STRIP)
    glVertex2f(5, 0)
    glVertex2f(0, 0)
    glVertex2f(0, -10)
    glVertex2f(5, -10)
    glVertex2f(5, -5)
    glVertex2f(3, -5)
    glVertex2f(3, -8)
    
    
    glEnd()
    
    # Letra A
    glBegin(GL_LINES)
    glVertex2f(7, -10)
    glVertex2f(9, 0)
    glVertex2f(9, 0)
    glVertex2f(11, 0)
    glVertex2f(11, 0)
    glVertex2f(13, -10)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(8, -5)
    glVertex2f(12, -5)
    glEnd()
    
    # Letra M
    glBegin(GL_LINE_STRIP)
    glVertex2f(15, -10)
    glVertex2f(15, 0)
    glVertex2f(17, -5)
    glVertex2f(19, 0)
    glVertex2f(19, -10)
    glEnd()
    
    # Letra E
    glBegin(GL_LINE_STRIP)
    glVertex2f(21, -10)
    glVertex2f(21, 0)
    glVertex2f(25, 0)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(21, -5)
    glVertex2f(24, -5)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(21, -10)
    glVertex2f(25, -10)
    glEnd()
    
    # Espacio entre palabras
    
    # Letra O
    glBegin(GL_LINE_LOOP)
    glVertex2f(30, 0)
    glVertex2f(30, -10)
    glVertex2f(34, -10)
    glVertex2f(34, 0)
    glEnd()
    
    # Letra V
    glBegin(GL_LINE_STRIP)
    glVertex2f(36, 0)
    glVertex2f(38, -10)
    glVertex2f(40, 0)
    glEnd()
    
    # Letra E
    glBegin(GL_LINE_STRIP)
    glVertex2f(42, -10)
    glVertex2f(42, 0)
    glVertex2f(46, 0)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(42, -5)
    glVertex2f(45, -5)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(42, -10)
    glVertex2f(46, -10)
    glEnd()
    
    # Letra R
    glBegin(GL_LINE_STRIP)
    glVertex2f(48, -10)
    glVertex2f(48, 0)
    glVertex2f(52, 0)
    glVertex2f(52, -5)
    glVertex2f(48, -5)
    glEnd()
    glBegin(GL_LINE_STRIP)
    glVertex2f(48, -5)
    glVertex2f(52, -10)
    glEnd()
    
    glPopMatrix()
    


def main():
    global pacman_next_direction, invulnerable, invulnerable_timer, game_over

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Pac-Man")

    glClearColor(0.0, 0.0, 0.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, ANCHO_MAPA * CELL_SIZE, -(ALTO_MAPA * CELL_SIZE), 0)
    glMatrixMode(GL_MODELVIEW)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    pacman_next_direction = 0
                elif event.key == K_UP:
                    pacman_next_direction = 1
                elif event.key == K_LEFT:
                    pacman_next_direction = 2
                elif event.key == K_DOWN:
                    pacman_next_direction = 3
                elif event.key == K_ESCAPE:
                    running = False
                elif event.key == K_r and game_over:
                    game_over = False
                    vidas_pacman = 3
                    pacman_x, pacman_y = pacman_starting_x, pacman_starting_y
                    pacman_direction = 0
                    pacman_next_direction = None
                    invulnerable = True
                    invulnerable_timer = 180

        if not game_over:
            actualizar_pacman()
            actualizar_fantasmas()

            if invulnerable:
                invulnerable_timer -= 1
                if invulnerable_timer <= 0:
                    invulnerable = False

            game_over = colision_de_fantasmas()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        hacer_mapa()
        draw_pacman()
        draw_all_fantasmas()
        contador_de_vidas()

        if game_over:
            draw_game_over()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()