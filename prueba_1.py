import time
import pygame
from pygame.locals import *

# Inicializar pygame
pygame.init()

# Inicializar el mezclador de sonido
pygame.mixer.init()

# Cargar la canción (debe estar en la carpeta del proyecto o indicar la ruta completa)
pygame.mixer.music.load("assets/music/Apatrullando.mp3")  # Reemplaza con la ruta correcta

# Ajustar volumen (opcional, valor entre 0.0 y 1.0)
pygame.mixer.music.set_volume(0.2)

# Reproducir la música en bucle infinito (-1)
pygame.mixer.music.play(-1)

# Tamaño de ventana
VIEW_WIDTH = 1366
VIEW_HEIGHT = 768

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Iniciar ventana
pantalla = pygame.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
pygame.display.set_caption("Torrente Vice")

# Fuentes (deben inicializarse después de pygame.init())
titulo_font = pygame.font.SysFont("georgia", 74, bold=True)
menu_font = pygame.font.Font(None, 36)

# Cargar imagen de fondo una sola vez
background_image = pygame.image.load('assets/background_images/mapa.jpg').convert()
background_width = background_image.get_width()
background_height = background_image.get_height()

# Configuración del personaje
player_image = pygame.image.load('assets/sprites/down0.png')
protagonist_speed = 4
player_rect = player_image.get_rect(midbottom=(VIEW_WIDTH // 2, VIEW_HEIGHT // 2))

# Posiciones iniciales del fondo
bg_x, bg_y = 0, 0
MARGIN_X, MARGIN_Y = VIEW_WIDTH // 2, VIEW_HEIGHT // 2

# Control de FPS
clock = pygame.time.Clock()
fps = 30

# Animación del personaje
sprite_direction = "down"
sprite_index = 0
animation_protagonist_speed = 200
sprite_frame_number = 3
last_change_frame_time = 0
idle = False


def imprimir_pantalla_fons(x, y):
    pantalla.blit(background_image, (x, y))


def mostrar_menu():
    pantalla.fill(NEGRO)

    title_text = titulo_font.render("Torrente Vice", True, BLANCO)
    menu_text_1 = menu_font.render("1. Salir", True, BLANCO)
    menu_text_2 = menu_font.render("2. Continuar", True, BLANCO)

    pantalla.blit(title_text, (VIEW_WIDTH // 2 - title_text.get_width() // 2, 100))
    pantalla.blit(menu_text_1, (VIEW_WIDTH // 2 - 50, VIEW_HEIGHT // 2 - 20))
    pantalla.blit(menu_text_2, (VIEW_WIDTH // 2 - 50, VIEW_HEIGHT // 2 + 20))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pygame.quit()
                    import os
                    os.system("python3 main.py")
                    exit()
                elif event.key == pygame.K_2:
                    return


# Loop principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            mostrar_menu()

    current_time = pygame.time.get_ticks()

    idle = True
    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        idle = False
        sprite_direction = "up"
        if player_rect.y > MARGIN_Y or bg_y >= 0:
            player_rect.y = max(player_rect.y - protagonist_speed, player_rect.height // 2)
        else:
            bg_y = min(bg_y + protagonist_speed, 0)

    if keys[K_DOWN]:
        idle = False
        sprite_direction = "down"
        if player_rect.y < VIEW_HEIGHT - MARGIN_Y or bg_y <= VIEW_HEIGHT - background_height:
            player_rect.y = min(player_rect.y + protagonist_speed, VIEW_HEIGHT - player_rect.height // 2)
        else:
            bg_y = max(bg_y - protagonist_speed, VIEW_HEIGHT - background_height)

    if keys[K_RIGHT]:
        idle = False
        sprite_direction = "right"
        if player_rect.x < VIEW_WIDTH - MARGIN_X or bg_x <= VIEW_WIDTH - background_width:
            player_rect.x = min(player_rect.x + protagonist_speed, VIEW_WIDTH - player_rect.width // 2)
        else:
            bg_x = max(bg_x - protagonist_speed, VIEW_WIDTH - background_width)

    if keys[K_LEFT]:
        idle = False
        sprite_direction = "left"
        if player_rect.x > MARGIN_X or bg_x >= 0:
            player_rect.x = max(player_rect.x - protagonist_speed, player_rect.width // 2)
        else:
            bg_x = min(bg_x + protagonist_speed, 0)

    imprimir_pantalla_fons(bg_x, bg_y)

    if not idle:
        if current_time - last_change_frame_time >= animation_protagonist_speed:
            last_change_frame_time = current_time
            sprite_index = (sprite_index + 1) % sprite_frame_number
    else:
        sprite_index = 0

    player_image = pygame.image.load(f'assets/sprites/{sprite_direction}{sprite_index}.png')
    pantalla.blit(player_image, player_rect)
    player_rect.clamp_ip(pantalla.get_rect())

    pygame.display.update()
    clock.tick(fps)
