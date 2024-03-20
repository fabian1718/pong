import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la ventana
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Velocidad de las paletas
PADDLE_SPEED = 60

# Velocidad de la pelota
BALL_SPEED_X = 0.5
BALL_SPEED_Y = 0.5

# Posiciones y velocidades de las paletas y la pelota
player1_y = height // 2
player2_y = height // 2
ball_x = width // 2
ball_y = height // 2
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y

# Contadores de puntos
player1_score = 0
player2_score = 0

# Función para reiniciar la posición de la pelota
def reset_ball(direction):
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = width // 2
    ball_y = height // 2
    ball_speed_x = BALL_SPEED_X * direction
    ball_speed_y = BALL_SPEED_Y

# Función para mostrar un mensaje en la ventana y obtener la entrada del usuario
def get_player_name(prompt):
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(200, 200, 400, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        window.fill((30, 30, 30))
        txt_surface = font.render(prompt, True, WHITE)  # Mostrar el prompt
        window.blit(txt_surface, (200, 150))
        txt_surface = font.render(text, True, color)
        width = max(400, txt_surface.get_width()+10)
        input_box.w = width
        window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(window, color, input_box, 2)
        pygame.display.flip()

# Obtener los nombres de los jugadores
player1_name = get_player_name("Ingrese el nombre del Jugador 1:")
player2_name = get_player_name("Ingrese el nombre del Jugador 2:")

# Loop principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Controlar la paleta del jugador 1
            if event.key == pygame.K_w:
                player1_y -= PADDLE_SPEED
            elif event.key == pygame.K_s:
                player1_y += PADDLE_SPEED
            # Controlar la paleta del jugador 2
            elif event.key == pygame.K_UP:
                player2_y -= PADDLE_SPEED
            elif event.key == pygame.K_DOWN:
                player2_y += PADDLE_SPEED

    # Limitar las paletas dentro de la ventana
    player1_y = max(0, min(player1_y, height - 100))
    player2_y = max(0, min(player2_y, height - 100))

    # Mover la pelota
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Rebotar la pelota si toca el borde superior o inferior
    if ball_y <= 0 or ball_y >= height:
        ball_speed_y *= -1

    # Rebotar la pelota si toca las paletas
    if ball_x <= 50 and player1_y <= ball_y <= player1_y + 100:
        ball_speed_x *= -1
    elif ball_x >= width - 70 and player2_y <= ball_y <= player2_y + 100:
        ball_speed_x *= -1

    # Puntuación y reinicio de la pelota si sale de la pantalla
    if ball_x <= 0:
        # Puntuación para el jugador 2
        player2_score += 1
        reset_ball(1)
    elif ball_x >= width:
        # Puntuación para el jugador 1
        player1_score += 1
        reset_ball(-1)

    # Verificar si algún jugador ha ganado
    if player1_score == 5:
        font = pygame.font.Font(None, 50)
        winner_text = font.render(f"{player1_name} ha ganado!", True, WHITE)
        window.blit(winner_text, ((width - winner_text.get_width()) // 2, (height - winner_text.get_height()) // 2))
        pygame.display.update()
        pygame.time.wait(3000)
        break
    elif player2_score == 5:
        font = pygame.font.Font(None, 50)
        winner_text = font.render(f"{player2_name} ha ganado!", True, WHITE)
        window.blit(winner_text, ((width - winner_text.get_width()) // 2, (height - winner_text.get_height()) // 2))
        pygame.display.update()
        pygame.time.wait(3000)
        break

    # Limpiar la pantalla
    window.fill(BLACK)

    # Dibujar las paletas y la pelota
    pygame.draw.rect(window, WHITE, pygame.Rect(50, player1_y, 20, 100))
    pygame.draw.rect(window, WHITE, pygame.Rect(width - 70, player2_y, 20, 100))
    pygame.draw.ellipse(window, WHITE, pygame.Rect(ball_x - 15, ball_y - 15, 30, 30))

    # Mostrar los marcadores de puntos
    font = pygame.font.Font(None, 36)
    player1_text = font.render(f"{player1_name}: {player1_score}", True, WHITE)
    player2_text = font.render(f"{player2_name}: {player2_score}", True, WHITE)
    window.blit(player1_text, (20, 20))
    window.blit(player2_text, (width - 160, 20))

    # Actualizar la ventana
    pygame.display.update()
