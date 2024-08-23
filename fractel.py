import pygame
from pygame.locals import *
from pygame.surfarray import make_surface
import random
import time
import math

version = "1.0.4"

pygame.init()
pygame.mixer.init()

# Загрузка звуковых файлов
pygame.mixer.music.load("media/mp3/music/background_music_1.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)

collision_sound = pygame.mixer.Sound("media/mp3/sfx/collision.mp3")
rocket_jump_sound = pygame.mixer.Sound("media/mp3/sfx/rocket_jump.mp3")
new_stage_sound = pygame.mixer.Sound("media/mp3/sfx/new_stage.mp3")
new_life_sound = pygame.mixer.Sound("media/mp3/sfx/new_life.mp3")
new_score_sound = pygame.mixer.Sound("media/mp3/sfx/new_score.mp3")
laser_sound = pygame.mixer.Sound("media/mp3/sfx/laser.mp3")
laser_empty = pygame.mixer.Sound("media/mp3/sfx/laser_empty.mp3")
shot_sound = pygame.mixer.Sound("media/mp3/sfx/shot.mp3")

#Проверка выиграл или проиграл
winner = 0

# Инициализация окна
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("FRACTEL " + version)

# Определение коротких имён для цветов
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Создаем списки для хранения координат и скоростей частиц
particles = []
speeds = []

# Цвета частиц в RGB
p_pr = 7
p_pg = 121
p_pb = 212

# Параметры частиц, возникающих от столкновения с энергошарами (препятствиями)
cparticles = []
cparticle_count = 20
cmax_distance = 50
cparticle_sizes = [1, 2, 3]

# Параметры частиц, возникающих от столкновения энергошаров с границей экрана
ocparticles = []
ocparticle_count = 10
ocmax_distance = 100
ocparticle_sizes = [1, 2]

# Генерируем случайные частицы и их скорости
for _ in range(100):
    x = random.randint(0, width)
    y = random.randint(0, height)
    particles.append((x, y))
    speed = random.randint(1, 5)
    speeds.append(speed)


# Стадия игры
stage = 1

# Начальные условия выстрела
shots = []  # Список выстрелов
shot_speed = 10  # Скорость выстрела
gun_shell = 3 # Обойма

# Загружаем картинку выстрела
shot_img = pygame.image.load("media/png/particles/shot.png").convert_alpha()
shot_img = pygame.transform.scale(shot_img, (16, 16))

# Загружаем фоны главного экрана
if (stage == 1):
    back_img = pygame.image.load("media/png/back/back_1.png").convert_alpha()
    back_img = pygame.transform.scale(back_img, (width, height))
    const_img = pygame.image.load("media/png/const/const_1.png").convert_alpha()
    const_img = pygame.transform.scale(const_img, (width, height))
if (stage == 2):
    back_img = pygame.image.load("media/png/back/back_2.png").convert_alpha()
    back_img = pygame.transform.scale(back_img, (width, height))
    const_img = pygame.image.load("media/png/const/const_2.png").convert_alpha()
    const_img = pygame.transform.scale(const_img, (width, height))
if (stage == 3):
    back_img = pygame.image.load("media/png/back/back_3.png").convert_alpha()
    back_img = pygame.transform.scale(back_img, (width, height))
    const_img = pygame.image.load("media/png/const/const_3.png").convert_alpha()
    const_img = pygame.transform.scale(const_img, (width, height))
if (stage == 4):
    back_img = pygame.image.load("media/png/back/back_4.png").convert_alpha()
    back_img = pygame.transform.scale(back_img, (width, height))
    const_img = pygame.image.load("media/png/const/const_4.png").convert_alpha()
    const_img = pygame.transform.scale(const_img, (width, height))
if (stage == 5):
    back_img = pygame.image.load("media/png/back/back_5.png").convert_alpha()
    back_img = pygame.transform.scale(back_img, (width, height))
    const_img = pygame.image.load("media/png/const/const_5.png").convert_alpha()
    const_img = pygame.transform.scale(const_img, (width, height))


# Создание массива значений цвета для затемнения
data = pygame.surfarray.pixels3d(const_img)
darkened_data = (data * 0.4)
# Создание затемненной поверхности из массива
darkened_img = make_surface(darkened_data)
# Переменная для отслеживания позиции фона
x_offset = 0

# Параметры земли и игрока
ground_height = 63
player_size = 30
player_pos = [width / 2, height - player_size - (ground_height + 4)]
jump_height = 150
jump_velocity = 10
gravity = 1

# Параметры препятствий
obstacle_min_size = 30
obstacle_max_size = 30
obstacle_pos = [width / 2, height - obstacle_max_size - (ground_height + 1)]

# Параметры объекта Танк
tank_min_size = 64
tank_max_size = 64
tank_pos = [width / 2, height - tank_max_size - (ground_height + 1)]

# Параметры скроллинга и игрового процесса
scrolling_speed = 2
obstacle_speed = random.randint(4, 6)
tank_speed = 5
score = 1
lives = 3
second_chance = 0
bomb_ready = 0
gun_ready = 0

# Параметры фоновых блоков
tile_size = 32
tiles_per_row = width // tile_size + 1
tiles_per_col = ground_height // tile_size + 1
ground_tiles = []

# Загрузка изображений танка
tank_img = pygame.image.load("media/png/objects/tank.png")
tank_img = pygame.transform.scale(tank_img, (128, tank_max_size))

tile_4 = "media/png/ground/def/solid_4_"+str(stage)+".png"
tile_2 = "media/png/ground/def/solid_2_"+str(stage)+".png"
tile_3 = "media/png/ground/def/solid_3_"+str(stage)+".png"
tile_1 = "media/png/ground/def/solid_1_"+str(stage)+".png"

# Загрузка изображений, формирующих полотно дороги
count_col = 0
for row in range(tiles_per_col):
    count_col += 1
    for col in range(tiles_per_row):
        row_var = random.randint(1, 2)
        if (count_col == 1):
            if (row_var == 1):
                ground_tile = pygame.image.load(tile_4).convert_alpha()
            if (row_var == 2):
                ground_tile = pygame.image.load(tile_2).convert_alpha()
                
        if (count_col == 2):
            if (row_var == 1):
                ground_tile = pygame.image.load(tile_3).convert_alpha()
            if (row_var == 2):
                ground_tile = pygame.image.load(tile_1).convert_alpha()

        if (row_var != 1):
            row_var = random.randint(1, 2)
        
        ground_tile = pygame.transform.scale(ground_tile, (tile_size, tile_size))
        ground_tiles.append((ground_tile, (col * tile_size, height - (row + 1) * tile_size)))

    if (count_col > 1):
        count_col = 1

# Скины для энергошаров
obstacle_img_def = pygame.image.load("media/png/obs/obst.png").convert_alpha()
obstacle_img_def = pygame.transform.scale(obstacle_img_def, (obstacle_max_size, obstacle_max_size))
obstacle_img_g = pygame.image.load("media/png/obs/obst_green.png").convert_alpha()
obstacle_img_g = pygame.transform.scale(obstacle_img_g, (obstacle_max_size, obstacle_max_size))
obstacle_img_y = pygame.image.load("media/png/obs/obst_yellow.png").convert_alpha()
obstacle_img_y = pygame.transform.scale(obstacle_img_y, (obstacle_max_size, obstacle_max_size))
obstacle_img_r = pygame.image.load("media/png/obs/obst_red.png").convert_alpha()
obstacle_img_r = pygame.transform.scale(obstacle_img_r, (obstacle_max_size, obstacle_max_size))
obstacle_img_f = pygame.image.load("media/png/obs/obst_final.png").convert_alpha()
obstacle_img_f = pygame.transform.scale(obstacle_img_f, (obstacle_max_size, obstacle_max_size))
obstacle_img_ex_2 = pygame.image.load("media/png/obs/obst_explosed_2.png").convert_alpha()
obstacle_img_ex_2 = pygame.transform.scale(obstacle_img_ex_2, (obstacle_max_size, obstacle_max_size))

# Иконки для интерфейса
obstacle_img_ex = pygame.image.load("media/png/interface/obst_explosed.png").convert_alpha()
obstacle_img_ex = pygame.transform.scale(obstacle_img_ex, (obstacle_max_size, obstacle_max_size))
interface_img_gun = pygame.image.load("media/png/interface/gun_shell.png").convert_alpha()
interface_img_gun = pygame.transform.scale(interface_img_gun, (obstacle_max_size, obstacle_max_size))


obstacle_img = obstacle_img_def
obstacle_img_prev  = obstacle_img_def

# Функция для изменения размера изображения
def resize_image(image, new_size):
    return pygame.transform.scale(image, new_size)

resize_speed = 1  # Скорость изменения размера
resize_speed_shot = 3  # Скорость изменения размера
resizing = False  # Флаг, отвечающий за изменение размера
current_size = obstacle_max_size
wanted_size = 31
current_size_shot = 16
wanted_size_shot = 20


# Загрузка изображений игрока
pi_dir = "media/png/player/"
player_images = [pi_dir+'Player_stand_1.png', pi_dir+'Player_stand_2.png', pi_dir+'Player_jump_1.png', pi_dir+'Player_jump_2.png', pi_dir+'Player_1.png', pi_dir+'Player_2.png']
player_imgs = []
for img_name in player_images:
    player_img = pygame.image.load(img_name).convert_alpha()
    player_imgs.append(pygame.transform.scale(player_img, (player_size, player_size)))
# Переменная для отслеживания текущего изображения
current_img_index = 0
# Таймер для смены изображений
tiktak = 0

# Статусы игрока 0 - норма, 1 - прыжок, 2 - отключение ранца
player_state = 0

# Статусы игрока 0 - норма, 1 - уничтожено игроком
obstacle_state = 0


# Загрузка изображения столкновения
eximage_path = "media/png/mask/expl.png"
eximage = pygame.image.load(eximage_path)

# Шрифт для отображения счета и жизней
font = pygame.font.Font(None, 36)

# Переменная состояния паузы
paused = False

# Отображение текста
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    surface.blit(text_surface, (x, y))

def draw_text_pause(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, RED)
    surface.blit(text_surface, (x, y))

# Функции для отображения счета, жизней и текстовых сообщений
def display_score(score):
    score_text = font.render("Счет: " + str(score-1), True, WHITE)
    screen.blit(score_text, (10, 10))

def display_lives(lives):
    lives_text = font.render("Энергия: " + str(lives), True, WHITE)
    screen.blit(lives_text, (width - lives_text.get_width() - 10, 10))

def display_text(text, y):
    text_render = font.render(text, True, WHITE)
    screen.blit(text_render, (width // 2 - text_render.get_width() // 2, y))

# Функция сброса игры
def reset_game(new_stage, is_winner):
    global player_pos, is_jumping, is_moving_left, is_moving_right, move_velocity, jump_velocity, obstacle_pos, score, lives, game_over, const_img, back_img, darkened_data, darkened_img, data, stage, winner, bomb_ready, wanted_size, gun_ready, tile_1, tile_2, tile_3, tile_4, ground_tile
    player_pos = [width / 2, height - player_size - ground_height]
    is_jumping = False
    is_moving_left = True
    is_moving_right = False
    move_velocity = 2
    jump_velocity = 10
    obstacle_pos[0] = width
    score = 1
    lives = 3
    game_over = False
    bomb_ready = 0
    gun_ready = 1
    if (new_stage==1): wanted_size = 31
    if (new_stage==2): wanted_size = 32
    if (new_stage==3): wanted_size = 33
    if (new_stage==4): wanted_size = 34
    if (new_stage==5): wanted_size = 35


    # Сброс заднего фона
    if (is_winner == 1):
        if (new_stage == 1):
            next_stage = 1
            stage = 1
        if (new_stage == 2):
            next_stage = 2
            stage = 2
        if (new_stage == 3):
            next_stage = 3
            stage = 3
        if (new_stage == 4):
            next_stage = 4
            stage = 4
        if (new_stage == 5):
            next_stage = 5
            stage = 5
    else:
            next_stage = 1
            stage = 1

    pygame.mixer.music.load("media/mp3/music/background_music_"+str(next_stage)+".mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.7)
    back_img = pygame.image.load("media/png/back/back_"+str(next_stage)+".png").convert_alpha()
    back_img = pygame.transform.scale(back_img, (width, height))
    const_img = pygame.image.load("media/png/const/const_"+str(next_stage)+".png").convert_alpha()
    const_img = pygame.transform.scale(const_img, (width, height))
    data = pygame.surfarray.pixels3d(const_img)
    darkened_data = (data * 0.4)
    darkened_img = make_surface(darkened_data)
    screen.blit(darkened_img, (0, 0))
    winner = 0
    ground_tiles.clear()
    tile_4 = "media/png/ground/def/solid_4_"+str(stage)+".png"
    tile_2 = "media/png/ground/def/solid_2_"+str(stage)+".png"
    tile_3 = "media/png/ground/def/solid_3_"+str(stage)+".png"
    tile_1 = "media/png/ground/def/solid_1_"+str(stage)+".png"
    
    # Загрузка изображений, формирующих полотно дороги
    count_col = 0
    for row in range(tiles_per_col):
        count_col += 1
        for col in range(tiles_per_row):
            row_var = random.randint(1, 2)
            if (count_col == 1):
                if (row_var == 1):
                    ground_tile = pygame.image.load(tile_4).convert_alpha()
                if (row_var == 2):
                    ground_tile = pygame.image.load(tile_2).convert_alpha()
                
            if (count_col == 2):
                if (row_var == 1):
                    ground_tile = pygame.image.load(tile_3).convert_alpha()
                if (row_var == 2):
                    ground_tile = pygame.image.load(tile_1).convert_alpha()

            if (row_var != 1):
                row_var = random.randint(1, 2)
        
            ground_tile = pygame.transform.scale(ground_tile, (tile_size, tile_size))
            ground_tiles.append((ground_tile, (col * tile_size, height - (row + 1) * tile_size)))

        if (count_col > 1):
            count_col = 1
    
    
# Функция проверки столкновения игрока с препятствием
def check_collision(player_pos, obstacle_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    p_size = player_size
    o_x = obstacle_pos[0]
    o_y = obstacle_pos[1]
    o_size = obstacle_max_size
    if (o_x <= p_x < o_x + o_size) or (o_x <= p_x + p_size < o_x + o_size):
        if o_y <= p_y < o_y + o_size:
            return True
        elif o_y <= p_y + p_size < o_y + o_size:
            return True
    return False

# Функция проверки столкновения игрока с танком
def check_collision_tank(player_pos, tank_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    p_size = player_size
    o_x = tank_pos[0]
    o_y = tank_pos[1]
    ox_size = 128
    oy_size = 64
    if (o_x <= p_x < o_x + ox_size) or (o_x <= p_x + p_size < o_x + ox_size):
        if o_y <= p_y < o_y + oy_size:
            return True
        elif o_y <= p_y + p_size < o_y + oy_size:
            return True
    return False



running = True
is_jumping = False
move_velocity = 2
is_moving_left = True
is_moving_right = False
clock = pygame.time.Clock()
game_over = False
game_over_text_y = height // 2 - 120
obstacle_frequency = 0
obstacle_counter = 0
obstacles = []
tank_frequency = 0
tank_counter = 0
tanks = []

# Параметры таймера
timer_minutes = 0
timer_seconds = 0
timer_font = pygame.font.Font(None, 36)
timer_text = timer_font.render("Время: 00:00", True, WHITE)
timer_text_x = width // 2 - timer_text.get_width() // 2
timer_text_y = 10
timer_frequency = 30  # Частота обновления таймера (в кадрах)
timer_counter = timer_frequency


# Функция для отображения таймера
def display_timer(minutes, seconds):
    timer_text = timer_font.render(f"Время: {timer_minutes:02}:{timer_seconds:02}", True, WHITE)
    screen.blit(timer_text, (timer_text_x, timer_text_y))

# Класс для частиц
class cParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.choice(cparticle_sizes)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(1, 3)
        self.distance = 0
    
    def move(self):
        self.distance += self.speed
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
    
    def draw(self, surface):
        if self.distance <= cmax_distance:
            pygame.draw.circle(surface, (7, 255, 212), (int(self.x), int(self.y)), self.size)

# Класс для частиц столкновения с левой границей экрана
class ocParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.choice(ocparticle_sizes)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(1, 3)
        self.distance = 0
    
    def move(self):
        self.distance += self.speed
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
    
    def draw(self, surface):
        if self.distance <= ocmax_distance:
            pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.size)

# Главный игровой цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()  # Пауза музыки
                else:
                    pygame.mixer.music.unpause()  # Возобновление музыки    
            
            # --------------------- БЛОК СТРЕЛЬБЫ -----------------------
            if event.key == pygame.K_SPACE:
                if not game_over:
                    if (lives > 1) and (gun_shell > 0):
                        shot_pos = [player_pos[0] + 30, player_pos[1] + 7]  # Расположение выстрела относительно игрока
                        shot_sound.play()
                        shots.append(shot_pos)
                        gun_shell -= 1
                        if gun_shell == 0:
                            lives = lives - 1
                            gun_shell = 3
                    else:
                        laser_empty.play()
            # --------------------- КОНЕЦ БЛОКА СТРЕЛЬБЫ -----------------
            
            if event.key == pygame.K_UP:
                if not game_over:
                    rocket_jump_sound.play()
                    player_state = 1
                    is_jumping = True
                    jump_velocity = 10                    
            if event.key == pygame.K_ESCAPE:
                screen = pygame.display.set_mode((width, height))
            if event.key == pygame.K_TAB:
                screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

            if event.key == pygame.K_LALT:
                if not game_over:
                    if lives > 10:
                        lives = lives - 10
                        #звук подрыва энергошаров
                        laser_sound.play()
                        obstacle_state = 1
                    else:
                        #звук что оружие не заряжено
                        laser_empty.play()

            if event.key == pygame.K_DOWN:
                if not game_over:
                    player_state = 2
                    is_jumping = False
            if event.key == pygame.K_LEFT:
                if not game_over:
                    is_moving_right = False
                    is_moving_left = True
                    move_velocity = 2
            if event.key == pygame.K_RIGHT:
                if not game_over:
                    is_moving_left = False
                    is_moving_right = True
                    move_velocity = 2
    if not paused:        
        
        if is_moving_left:
            player_pos[0] -= move_velocity
                
        if is_moving_right:
            player_pos[0] += move_velocity
        
        if is_jumping:
            player_pos[1] -= jump_velocity
            jump_velocity -= gravity
        else:
            if game_over == False:
                player_state = 0
            else:
                player_state = 0
        # Обновление таймера
        if not game_over:
            if timer_counter == 0:
                timer_seconds += 1
                if timer_seconds == 60:
                    timer_minutes += 1
                    timer_seconds = 0
                timer_counter = timer_frequency
            else:
                timer_counter -= 1
        
        resizing = not resizing
        
        # Ограничение игрока относительно земли
        if player_pos[1] > height - player_size - (ground_height):
            player_pos[1] = height - player_size - (ground_height + 2)
            player_state = 0

        if player_pos[0] < 0:
            player_pos[0] = 0
            player_state = 0
        if player_pos[0] > width - player_size:
            player_pos[0] = width - player_size
            player_state = 0

        if lives > 10:
            bomb_ready = 1
        else:
            bomb_ready = 0
        if lives > 1:
            gun_ready = 1
        else:
            gun_ready = 0

        # Проверка, чтобы игрок не мог прыгнуть выше верхней границы экрана
        if player_pos[1] < 1:
            player_state = 2
            is_jumping = False

        # Падение игрока, если не выполняется условие прыжка
        if not is_jumping:
            if player_pos[1] + player_size < height - (ground_height + 2):
                player_pos[1] += (gravity*10)
                player_state = 2

        # Создание танков с заданной частотой
        if tank_counter == 0:
            
            moref = 1000 - ((100* stage)+100)
            
            tank_frequency = random.randint(50, moref)
            tank_counter = tank_frequency
            tank_size = random.randint(tank_min_size, tank_max_size)
            tank_pos[0] = width
            tank_pos[1] = height - tank_size - (ground_height - 6)
            tanks.append(list(tank_pos))
        else:
            tank_counter -= 1
        # Обновление позиций танков и удаление вышедших за границу экрана
        for tank in tanks:
            tank[0] -= tank_speed
            if tank[0] + tank_max_size < 0:
                tanks.remove(tank)
            if check_collision_tank(player_pos, tank):
                lives -= 1
                if lives == 0:
                    cparticles = [cParticle(player_pos[0]+16, player_pos[1]-16) for _ in range(cparticle_count)]
                    collision_sound.play()
                    game_over = True
                    break
                else:
                    cparticles = [cParticle(player_pos[0]+16, player_pos[1]-16) for _ in range(cparticle_count)]
                    collision_sound.play()
                    is_jumping = True
                    jump_velocity = 10
                    tanks.remove(tank)
                    player_state = 3

        # Создание препятствий с заданной частотой
        if obstacle_counter < score:
            obstacle_frequency = random.randint(300, 400)
            obstacle_counter = obstacle_frequency
            obstacle_size = random.randint(obstacle_min_size, 600)
            obstacle_pos[0] = width
            obstacle_pos[1] = height - obstacle_size - (ground_height + 1)
            obstacles.append(list(obstacle_pos))
        else:
            obstacle_counter -= 1+(score-second_chance)

        # Обновление позиций препятствий и удаление вышедших за границу экрана
        for obstacle in obstacles:
            prev_ob = obstacle[1]
            obstacle[0] -= (obstacle_speed - 1)

            if obstacle[0] + obstacle_max_size < 0:
                ocparticles = [ocParticle(obstacle_pos[0] - width, prev_ob) for _ in range(ocparticle_count)]
                new_score_sound.play()
                obstacles.remove(obstacle)
                score += 1
                score_show = score
                # Каждые 10 очков даём жизнь
                if ((score-1) % 10) == 0:
                    new_life_sound.play()
                    new_life_sound.set_volume(0.4)
                    lives +=1
                # На 50 очках сброс интенсивности и замена спрайта
                if (score == 50):
                    darkened_data = (data * 0.6)
                    darkened_img = make_surface(darkened_data)
                    new_stage_sound.play()
                    obstacle_img = obstacle_img_g
                    obstacle_img_prev = obstacle_img_g
                    second_chance = 48
                    p_pr = 19
                    p_pg = 186
                    p_pb = 0
                # На 100 очках сброс интенсивности и замена спрайта
                if (score == 100):
                    darkened_data = (data * 0.7)
                    darkened_img = make_surface(darkened_data)
                    new_stage_sound.play()
                    obstacle_img = obstacle_img_y
                    obstacle_img_prev = obstacle_img_y
                    second_chance = 98
                    p_pr = 219
                    p_pg = 200
                    p_pb = 0
                # На 200 очках сброс интенсивности и замена спрайта
                if (score == 200):
                    darkened_data = (data * 0.8)
                    darkened_img = make_surface(darkened_data)
                    new_stage_sound.play()
                    obstacle_img = obstacle_img_r
                    obstacle_img_prev = obstacle_img_r
                    second_chance = 198
                    p_pr = 218
                    p_pg = 17
                    p_pb = 0
                # На 300 очках сброс интенсивности и замена спрайта
                if (score == 300):
                    darkened_data = (data * 1)
                    darkened_img = make_surface(darkened_data)
                    new_stage_sound.play()
                    obstacle_img = obstacle_img_f
                    obstacle_img_prev = obstacle_img_f
                    second_chance = 298
                    p_pr = 221
                    p_pg = 221
                    p_pb = 221
                # На 451 очках победа
                if (score == 451):
                    game_over = True
                    winner = 1
                    break
        
        # Проверка столкновения игрока с препятствием
            if check_collision(player_pos, obstacle):
                lives -= 1
                if lives == 0:
                    cparticles = [cParticle(player_pos[0]+16, player_pos[1]-16) for _ in range(cparticle_count)]
                    collision_sound.play()
                    game_over = True
                    break
                else:
                    cparticles = [cParticle(player_pos[0]+16, player_pos[1]-16) for _ in range(cparticle_count)]
                    collision_sound.play()
                    is_jumping = True
                    jump_velocity = 10
                    obstacles.remove(obstacle)
                    player_state = 3
            
        # Обновление позиций фоновых блоков для прокрутки
        for i, ground_tile in enumerate(ground_tiles):
            ground_x = ground_tile[1][0]
            ground_y = ground_tile[1][1]
            ground_x -= scrolling_speed
            if ground_x < -tile_size:
                ground_x = width - 2
            ground_tiles[i] = (ground_tile[0], (ground_x, ground_y))

        # Обновление позиции фона
        x_offset -= 1  # Смещение фона на 1 пиксель влево
        screen.blit(back_img, (back_img.get_width() + 1, 0))

        # Рендеринг фона
        screen.fill((0, 0, 0))  # Заполнение экрана черным цветом
        screen.blit(darkened_img, (0, 0))
        screen.blit(back_img, (x_offset, 0))  # Рендерим фон с учетом смещения

        # --------------------- БЛОК СТРЕЛЬБЫ -----------------------
        # Обработка движения выстрелов
        for shot in shots[:]:
            shot[0] += shot_speed
            if shot[0] > 800:  # Проверка, достиг ли выстрел края экрана
                shots.remove(shot)

        # Проверка столкновений выстрелов с препятствиями
        for shot in shots[:]:
            for obstacle in obstacles[:]:
                # Прямоугольники для проверок столкновений
                shot_rect = pygame.Rect(shot[0], shot[1], 16, 16)
                obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], 30, 30)
                if shot_rect.colliderect(obstacle_rect):  # Проверка на столкновение
                    score = score + 1
                    ocparticles = [ocParticle(obstacle[0], obstacle[1]) for _ in range(ocparticle_count)]
                    new_score_sound.play()
                    shots.remove(shot)
                    obstacles.remove(obstacle)
                    break
        
        for shot in shots[:]:
            for tank in tanks[:]:
                # Прямоугольники для проверок столкновений
                shot_rect = pygame.Rect(shot[0], shot[1], 16, 16)
                tank_rect = pygame.Rect(tank[0], tank[1], 128, 64)
                if shot_rect.colliderect(tank_rect):  # Проверка на столкновение
                    ocparticles = [ocParticle(tank[0], tank[1]) for _ in range(ocparticle_count)]
                    laser_sound.play()
                    shots.remove(shot)
                    tanks.remove(tank)
                    break
        # Отрисовка выстрелов
        for shot in shots:
            screen.blit(shot_img_sized, shot)
        # --------------------- КОНЕЦ БЛОКА СТРЕЛЬБЫ -----------------


        # Проверка, не вышел ли фон за пределы экрана
        if x_offset < -back_img.get_width():
            x_offset = back_img.get_width() - 1  # Возвращаем фон на начало
   
        # Отрисовка фоновых блоков
        for ground_tile in ground_tiles:
            screen.blit(ground_tile[0], ground_tile[1])

        # Логика изменения размера
        if resizing:
            current_size += resize_speed
            current_size_shot += resize_speed_shot

            if current_size > wanted_size:  # Например, максимальный размер 100 пикселей
                resize_speed = -resize_speed
            elif current_size < obstacle_min_size:  # Вернуться к минимальному размеру
                resize_speed = -resize_speed

            if current_size_shot > wanted_size_shot:  # Например, максимальный размер 100 пикселей
                resize_speed_shot = -resize_speed_shot
            elif current_size_shot < 16:  # Вернуться к минимальному размеру
                resize_speed_shot = -resize_speed_shot
        
        obstacle_img_sized = resize_image(obstacle_img, (current_size, current_size))

        shot_img_sized = resize_image(shot_img, (current_size_shot, current_size_shot))
    
    
        # Отрисовка танков
        for tank in tanks:
            screen.blit(tank_img, tank)

        # Отрисовка препятствий
        for obstacle in obstacles:
            screen.blit(obstacle_img_sized, obstacle)

        # Анимация изображения игрока
        tiktak += 1
        if tiktak > 30:
            tiktak = 0
        
        if bomb_ready == 1:
            screen.blit(obstacle_img_ex, (50, 40))
        if gun_ready == 1:
            screen.blit(interface_img_gun, (10, 40))

        if obstacle_state == 1:
            obstacle_img = obstacle_img_ex_2
            if tiktak == 20:
                obstacles.clear()
                obstacle_img = obstacle_img_prev
                obstacle_state = 0


        if tiktak == 10 or tiktak == 20 or tiktak == 30:
            # Анимация бега
            if player_state == 0:
                if current_img_index != 0:
                    current_img_index = 0
                else:
                    current_img_index = 1
            # Анимация полёта на ранце
            if player_state == 1:
                if current_img_index != 2:
                    current_img_index = 2
                else:
                    current_img_index = 3
            # Анимация падения
            if player_state == 2:
                if current_img_index != 4:
                    current_img_index = 4
                else:
                    current_img_index = 5
            # Анимация столкновения
            if player_state == 3:
                if current_img_index != 4:
                    current_img_index = 4
                else:
                    current_img_index = 5

        # Рендеринг изображения игрока
        screen.blit(player_imgs[current_img_index], player_pos)
        if player_state == 3:
            screen.blit(eximage, player_pos)
    
        # Отображение текстовых сообщений при окончании игры
        if game_over:
            is_moving_right = False
            is_moving_left = False
            score_show = score
            second_chance = 0
            obstacles.clear()
            tanks.clear()
            #pygame.mixer.music.stop()
            obstacle_img = obstacle_img_def
            if winner == 0:
                new_stage = 1                
                display_score(score_show)
                display_timer(timer_minutes, timer_seconds)
                display_lives(lives)
                display_text("Вы проиграли. You lost :(", game_over_text_y)
                display_text("Enter - начать заново. Enter for restart.", game_over_text_y + 30)
                font = pygame.font.Font(None, 26)
                display_text("Fractel " + version, game_over_text_y + 190)
                display_text("game by Stanislav Nixman", game_over_text_y + 220)
                font = pygame.font.Font(None, 36)
                is_winner = 0
            
            if winner == 1:
                # Смена уровней
                if (stage == 1):
                    new_stage = 2
                    display_score(score_show)
                    display_timer(timer_minutes, timer_seconds)
                    display_lives(lives)
                    display_text("Следующий уровень (next stage) - " + str(new_stage), game_over_text_y)
                    display_text("Enter - продолжить. Enter for continue.", game_over_text_y + 50)
                    font = pygame.font.Font(None, 26)
                    display_text("Fractel " + version, game_over_text_y + 190)
                    display_text("game by Stanislav Nixman", game_over_text_y + 220)
                    font = pygame.font.Font(None, 36)
                    is_winner = 1
                if (stage == 2):
                    new_stage = 3
                    display_score(score_show)
                    display_timer(timer_minutes, timer_seconds)
                    display_lives(lives)
                    display_text("Следующий уровень (next stage) - " + str(new_stage), game_over_text_y)
                    display_text("Enter - продолжить. Enter for continue.", game_over_text_y + 50)
                    font = pygame.font.Font(None, 26)
                    display_text("Fractel " + version, game_over_text_y + 190)
                    display_text("game by Stanislav Nixman", game_over_text_y + 220)
                    font = pygame.font.Font(None, 36)
                    is_winner = 1
                if (stage == 3):
                    new_stage = 4
                    display_score(score_show)
                    display_timer(timer_minutes, timer_seconds)
                    display_lives(lives)
                    display_text("Следующий уровень (next stage) - " + str(new_stage), game_over_text_y)
                    display_text("Enter - продолжить. Enter for continue.", game_over_text_y + 50)
                    font = pygame.font.Font(None, 26)
                    display_text("Fractel " + version, game_over_text_y + 190)
                    display_text("game by Stanislav Nixman", game_over_text_y + 220)
                    font = pygame.font.Font(None, 36)
                    is_winner = 1
                if (stage == 4):
                    new_stage = 5
                    display_score(score_show)
                    display_timer(timer_minutes, timer_seconds)
                    display_lives(lives)
                    display_text("Следующий уровень (next stage) - " + str(new_stage), game_over_text_y)
                    display_text("Enter - продолжить. Enter for continue.", game_over_text_y + 50)
                    font = pygame.font.Font(None, 26)
                    display_text("Fractel " + version, game_over_text_y + 190)
                    display_text("game by Stanislav Nixman", game_over_text_y + 220)
                    font = pygame.font.Font(None, 36)
                    is_winner = 1

                if (stage == 5):
                    new_stage = 1
                    display_score(score_show)
                    display_timer(timer_minutes, timer_seconds)
                    display_lives(lives)
                    display_text("Вы прошли игру! You win!", game_over_text_y)
                    display_text("Enter - перезапуск. Enter for restart. ", game_over_text_y + 50)
                    font = pygame.font.Font(None, 26)
                    display_text("Fractel " + version, game_over_text_y + 190)
                    display_text("game by Stanislav Nixman", game_over_text_y + 220)
                    font = pygame.font.Font(None, 36)
                    is_winner = 1

        else:
            display_score(score)
            display_lives(lives)

        if (timer_minutes == 00 and timer_seconds > 1 and timer_seconds < 10):
            font = pygame.font.Font(None, 36)
            display_text("Наберите 450 очков! Score 450 points!", game_over_text_y)
            font = pygame.font.Font(None, 26)
            display_text("Управление (Controls):", game_over_text_y + 40)
            display_text("Вверх (Up) - прыжок(jump). Вниз (Down) - падение (fall)", game_over_text_y + 70)
            display_text("Влево-Вправо (Left-Right), P - пауза (pause)", game_over_text_y + 90)
            display_text("LALT - подрыв (explose). SPACE - выстрел (shot)", game_over_text_y + 110)
            display_text("TAB - полноэкранный режим (fullscreen).", game_over_text_y + 130)
            display_text("ESC - оконный режим (windowed)", game_over_text_y + 150)
            font = pygame.font.Font(None, 36)
        
        # Обработка ввода клавиатуры для перезапуска игры
        keys = pygame.key.get_pressed()
        if game_over and keys[pygame.K_RETURN]:
            score = 1
            second_chance = 0
            timer_counter = 0
            timer_minutes = 0
            timer_seconds = 0
            p_pr = 7
            p_pg = 121
            p_pb = 212
            reset_game(new_stage, is_winner)

        # Отображение таймера
        display_timer(timer_minutes, timer_seconds)

        # Обновление координат частиц
        for i, particle in enumerate(particles):
            x, y = particle
            speed = speeds[i]
            x -= speed
            if x < 0:
                x = width
            particles[i] = (x, y)
    
        # Отрисовка частиц
        for particle in particles:
            x, y = particle
            pygame.draw.circle(screen, (p_pr, p_pg, p_pb), (x, y), random.randint(1, 2))

        for cparticle in cparticles:
            cparticle.move()
            cparticle.draw(screen)
        for ocparticle in ocparticles:
            ocparticle.move()
            ocparticle.draw(screen)       
        pass
    
    if paused:              
        draw_text_pause(screen, "Пауза (Pause)", 50, width // 2 - 100, height // 2 - 200)
    
    # Обновление дисплея
    pygame.display.flip()

    # Ограничение частоты обновления экрана
    clock.tick(30)

pygame.quit()
