import pygame
from pygame.locals import *
from pygame.surfarray import make_surface
import random
import time
import math

version = "1.0.6"

pygame.init()
pygame.mixer.init()

# --------------------- Блок основных игровых переменных ------------------

# Текущий язык
current_language = 'russian'  # По умолчанию русский
# Указатель уровня игры (всего пять уровней на данный момент)
stage = 1

# Размеры окна игры
width = 800
height = 600

# Указатель, что это первый запуск игры
first_play = 1

# Указатель статуса победы
winner = 0

# Определение коротких имён для цветов
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Списки для хранения координат и скоростей нейтральных частиц летящих по экрану
particles = []
speeds = []

# Цвета нейтральных частиц в RGB
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

# Начальные условия выстрела
shots = []  # Список выстрелов
shot_speed = 10  # Скорость выстрела
gun_shell = 3 # Обойма

rockets_state = 0
rockets_shell = 3

# бафф на размер выстрела и урон по боссам
big_shot = 0
# постоянный щит
g_shield = 0
g_shield_switch = 0
# бонус на подрыв шаров
g_obst_ex = 0
# бонус к ракетам
g_rockets = 0
g_rockets_shell = 5


# Переменная для отслеживания позиции фона
x_offset = 0

# Параметры земли и игрока
ground_height = 63
player_size = 30
player_pos = [width / 2, height - player_size - (ground_height + 4)]
jump_height = 150
jump_velocity = 10
gravity = 1

# Параметры препятствий (они же - энергошары)
obstacle_min_size = 30
obstacle_max_size = 30
obstacle_pos = [width / 2, height - obstacle_max_size - (ground_height + 1)]

# Параметры объекта допэнергия (он же - дружественный дрон тип 1)
exen_min_size = 30
exen_max_size = 30
exen_pos = [width / 2, height - exen_max_size - (ground_height + 1)]

# Параметры объекта бафф (он же - дружественный дрон тип 2)
exen_b_min_size = 30
exen_b_max_size = 30
exen_b_pos = [width / 2, height - exen_b_max_size - (ground_height + 1)]



# Параметры объекта nyan (она же - ракета)
nyan_min_size = 30
nyan_max_size = 30
nyan_pos = [width / 2, height - nyan_max_size - (ground_height + 1)]

# Параметры объекта Танк (он же грузовик-корован)
tank_min_size = 64
tank_max_size = 64
tank_pos = [width / 2, height - tank_max_size - (ground_height + 1)]

# Параметры объекта Босс (он же Кибер-Панк)
boss_1_min_size = 256
boss_1_max_size = 256
boss_1_pos = [width / 2, height - boss_1_max_size - (ground_height + 1)]

# Параметры объекта Босс (он же Болотный Мех)
boss_2_min_size = 256
boss_2_max_size = 256
boss_2_pos = [width / 2, height - boss_2_max_size - (ground_height + 1)]

# Параметры объекта Босс (он же Белый Птиц)
boss_3_min_size = 256
boss_3_max_size = 256
boss_3_pos = [width / 2, height - boss_3_max_size - (ground_height + 1)]

# Параметры объекта Босс (он же Снежный Мех)
boss_4_min_size = 256
boss_4_max_size = 256
boss_4_pos = [width / 2, height - boss_4_max_size - (ground_height + 1)]

# Параметры объекта Босс (он же Чужой Мех)
boss_5_min_size = 256
boss_5_max_size = 256
#boss_5_pos = [width / 2, height - boss_5_max_size - (ground_height + 1)]
boss_5_pos = [width / 2, height]


# Параметры скроллинга и игрового процесса
scrolling_speed = 2
obstacle_speed = random.randint(4, 6)
exen_speed = 6
exen_b_speed = 7
nyan_speed = 6
tank_speed = 5
score = 1
lives = 3
second_chance = 0
bomb_ready = 0
gun_ready = 1
shield_ready = 1
rockets_ready = 0
running = True
is_jumping = False
move_velocity = 2
is_moving_left = True
is_moving_right = False
game_over = False
game_over_text_y = height // 2 - 120
obstacle_frequency = 0
obstacle_counter = 0
obstacles = []
tank_frequency = 0
tank_counter = 0
exen_counter = 0
exen_b_counter = -1
nyan_counter = 0
tanks = []
exens = []
exens_b = []
nyans = []
nyan_particles = []

boss_1_counter = 0
boss_1_defeated = 0
boss_1_speed = 6
bosses_1 = []
boss_1_appear = 0
boss_1_life = 30

boss_2_counter = 0
boss_2_defeated = 0
boss_2_speed = 6
bosses_2 = []
boss_2_appear = 0
boss_2_life = 34

boss_3_counter = 0
boss_3_defeated = 0
boss_3_speed = 6
bosses_3 = []
boss_3_appear = 0
boss_3_life = 38

boss_4_counter = 0
boss_4_defeated = 0
boss_4_speed = 6
bosses_4 = []
boss_4_appear = 0
boss_4_life = 44

boss_5_counter = 0
boss_5_defeated = 0
boss_5_speed = 6
bosses_5 = []
boss_5_appear = 0
boss_5_life = 48

# Объект для отслеживания времени
clock = pygame.time.Clock()

# Параметры таймера
timer_minutes = 0
timer_seconds = 0
timer_font = pygame.font.Font(None, 36)
timer_text = timer_font.render("00:00", True, WHITE)
timer_text_x = width // 2 - timer_text.get_width() // 2
timer_text_y = 10
timer_frequency = 30  # Частота обновления таймера (в кадрах)
timer_counter = timer_frequency

# Параметры фоновых блоков дороги
tile_size = 32
tiles_per_row = width // tile_size + 1
tiles_per_col = ground_height // tile_size + 1
ground_tiles = []

# Параметры пульсации для спрайтов
resize_speed = 1  # Скорость изменения размера
resize_speed_shot = 3  # Скорость изменения размера
resizing = False  # Флаг, отвечающий за изменение размера
current_size = obstacle_max_size
wanted_size = 31
current_size_shot = 16
wanted_size_shot = 20

# Таймер для смены изображений
tiktak = 0

# Создание списка со всеми спрайтами игрока
pi_dir = "media/png/player/" # Player_Images_DIRectory, а не то, что вы подумали
player_images = [pi_dir+'Player_stand_1.png', pi_dir+'Player_stand_2.png', pi_dir+'Player_jump_1.png', pi_dir+'Player_jump_2.png', pi_dir+'Player_1.png', pi_dir+'Player_2.png']
player_imgs = []
# Переменная для отслеживания текущего изображения
current_img_index = 0
# Статусы игрока 0 - норма, 1 - прыжок, 2 - отключение ранца
player_state = 0

# Статусы босса для смены спрайтов
boss_1_state = 0
boss_2_state = 0
boss_3_state = 0
boss_4_state = 0
boss_5_state = 0

# Статусы энергошаров 0 - норма, 1 - уничтожено игроком
obstacle_state = 0

# Шрифт для отображения счета и жизней
font = pygame.font.Font(None, 36)

# --------------------- Конец блока основных игровых переменных ------------------


# Инициализация окна
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fractel " + version)


# --------------------- Блок особых стартовых условий ------------------
# Стартовый экран, показывается при запуске игры во время паузы
start_img = pygame.image.load("media/png/start_screen.png").convert_alpha()
start_img = pygame.transform.scale(start_img, (width, height))
screen.blit(start_img, (0, 0))

# Стартовая мелодия, сразу ставится на паузу, так как игра начинается с паузы
pygame.mixer.music.load("media/mp3/music/background_music_1.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.pause()
music_active = 0

# Игра стартует и сразу ставится на паузу
paused = True
# --------------------- Конец блока особых стартовых условий ------------------


# ------------------ Блок загрузки звуковых файлов -------------
collision_sound = pygame.mixer.Sound("media/mp3/sfx/collision.mp3")
rocket_jump_sound = pygame.mixer.Sound("media/mp3/sfx/rocket_jump.mp3")
new_stage_sound = pygame.mixer.Sound("media/mp3/sfx/new_stage.mp3")
new_life_sound = pygame.mixer.Sound("media/mp3/sfx/new_life.mp3")
new_score_sound = pygame.mixer.Sound("media/mp3/sfx/new_score.mp3")
laser_sound = pygame.mixer.Sound("media/mp3/sfx/laser.mp3")
laser_empty = pygame.mixer.Sound("media/mp3/sfx/laser_empty.mp3")
shot_sound = pygame.mixer.Sound("media/mp3/sfx/shot.mp3")
rocket_launch_sound = pygame.mixer.Sound("media/mp3/sfx/rocket_launch.mp3")
boss_death_sound = pygame.mixer.Sound("media/mp3/sfx/boss_death.mp3")
shield_on_sound = pygame.mixer.Sound("media/mp3/sfx/shield_on.mp3")
# ------------------ Конец блока загрузки звуковых файлов -------------


# ------------------ Блок загрузки изображений -------------
# Определение загрузки изображений блоков полотна дороги в соответствии с уровнем игры
tile_4 = "media/png/ground/def/solid_4_"+str(stage)+".png"
tile_2 = "media/png/ground/def/solid_2_"+str(stage)+".png"
tile_3 = "media/png/ground/def/solid_3_"+str(stage)+".png"
tile_1 = "media/png/ground/def/solid_1_"+str(stage)+".png"

# Загружаем картинку выстрела
shot_img_1 = pygame.image.load("media/png/particles/shot.png").convert_alpha()
shot_img_1 = pygame.transform.scale(shot_img_1, (16, 16))
shot_img_2 = pygame.image.load('media/png/particles/nyan_particle.png')
shot_img_2 = pygame.transform.scale(shot_img_2, (16, 16))
shot_img = shot_img_1

# Загружаем фоны главного экрана в соответствии с уровнем игры
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
# Создание массива значений цвета для эффекта затемнения
data = pygame.surfarray.pixels3d(const_img)
darkened_data = (data * 0.4)
# Создание затемненной поверхности из массива
darkened_img = make_surface(darkened_data)

# Загрузка изображений допэнергии
exen_img = pygame.image.load("media/png/objects/extra_energy.png")
exen_img = pygame.transform.scale(exen_img, (exen_max_size, exen_max_size))

# Загрузка изображений баффа
exen_b_img = pygame.image.load("media/png/objects/extra_buff.png")
exen_b_img = pygame.transform.scale(exen_b_img, (exen_b_max_size, exen_b_max_size))

# Загрузка изображений nyan (ракеты)
nyan_img = pygame.image.load("media/png/objects/nyan.png")
nyan_img = pygame.transform.scale(nyan_img, (nyan_max_size, nyan_max_size))
nyan_particle_image = pygame.image.load('media/png/particles/nyan_particle.png')
nyan_particle_image = pygame.transform.scale(nyan_particle_image, (8, 8))
nyan_particle_image_2 = pygame.image.load('media/png/particles/shot.png')
nyan_particle_image_2 = pygame.transform.scale(nyan_particle_image_2, (8, 8))

# Загрузка изображений танка
tank_img = pygame.image.load("media/png/objects/tank.png")
tank_img = pygame.transform.scale(tank_img, (128, tank_max_size))
# Создание копии изображения с прозрачностью

# Загрузка изображений босса Кибер-Панк
boss_1_1_img = pygame.image.load("media/png/boss/boss_1_1.png")
boss_1_1_img = pygame.transform.scale(boss_1_1_img, (256, 256))
boss_1_1_alpha_img = boss_1_1_img.copy()
boss_1_1_alpha_img.set_alpha(255)
boss_1_2_img = pygame.image.load("media/png/boss/boss_1_2.png")
boss_1_2_img = pygame.transform.scale(boss_1_2_img, (256, 256))
boss_1_2_alpha_img = boss_1_2_img.copy()
boss_1_2_alpha_img.set_alpha(255)
boss_1_3_img = pygame.image.load("media/png/boss/boss_1_3.png")
boss_1_3_img = pygame.transform.scale(boss_1_3_img, (256, 256))
boss_1_3_alpha_img = boss_1_3_img.copy()
boss_1_3_alpha_img.set_alpha(255)
boss_1_4_img = pygame.image.load("media/png/boss/boss_1_4.png")
boss_1_4_img = pygame.transform.scale(boss_1_4_img, (256, 256))
boss_1_4_alpha_img = boss_1_4_img.copy()
boss_1_4_alpha_img.set_alpha(255)


# Загрузка изображений босса Болотный Мех
boss_2_1_img = pygame.image.load("media/png/boss/boss_2_1.png")
boss_2_1_img = pygame.transform.scale(boss_2_1_img, (256, 256))
boss_2_1_alpha_img = boss_2_1_img.copy()
boss_2_1_alpha_img.set_alpha(255)
boss_2_2_img = pygame.image.load("media/png/boss/boss_2_2.png")
boss_2_2_img = pygame.transform.scale(boss_2_2_img, (256, 256))
boss_2_2_alpha_img = boss_2_2_img.copy()
boss_2_2_alpha_img.set_alpha(255)
boss_2_3_img = pygame.image.load("media/png/boss/boss_2_3.png")
boss_2_3_img = pygame.transform.scale(boss_2_3_img, (256, 256))
boss_2_3_alpha_img = boss_2_3_img.copy()
boss_2_3_alpha_img.set_alpha(255)
boss_2_4_img = pygame.image.load("media/png/boss/boss_2_4.png")
boss_2_4_img = pygame.transform.scale(boss_2_4_img, (256, 256))
boss_2_4_alpha_img = boss_2_4_img.copy()
boss_2_4_alpha_img.set_alpha(255)


# Загрузка изображений босса Бклый Птиц
boss_3_1_img = pygame.image.load("media/png/boss/boss_3_1.png")
boss_3_1_img = pygame.transform.scale(boss_3_1_img, (256, 256))
boss_3_1_alpha_img = boss_3_1_img.copy()
boss_3_1_alpha_img.set_alpha(255)
boss_3_2_img = pygame.image.load("media/png/boss/boss_3_2.png")
boss_3_2_img = pygame.transform.scale(boss_3_2_img, (256, 256))
boss_3_2_alpha_img = boss_3_2_img.copy()
boss_3_2_alpha_img.set_alpha(255)
boss_3_3_img = pygame.image.load("media/png/boss/boss_3_3.png")
boss_3_3_img = pygame.transform.scale(boss_3_3_img, (256, 256))
boss_3_3_alpha_img = boss_3_3_img.copy()
boss_3_3_alpha_img.set_alpha(255)
boss_3_4_img = pygame.image.load("media/png/boss/boss_3_4.png")
boss_3_4_img = pygame.transform.scale(boss_3_4_img, (256, 256))
boss_3_4_alpha_img = boss_3_4_img.copy()
boss_3_4_alpha_img.set_alpha(255)

# Загрузка изображений босса Снежный Мех
boss_4_1_img = pygame.image.load("media/png/boss/boss_4_1.png")
boss_4_1_img = pygame.transform.scale(boss_4_1_img, (256, 256))
boss_4_1_alpha_img = boss_4_1_img.copy()
boss_4_1_alpha_img.set_alpha(255)
boss_4_2_img = pygame.image.load("media/png/boss/boss_4_2.png")
boss_4_2_img = pygame.transform.scale(boss_4_2_img, (256, 256))
boss_4_2_alpha_img = boss_4_2_img.copy()
boss_4_2_alpha_img.set_alpha(255)
boss_4_3_img = pygame.image.load("media/png/boss/boss_4_3.png")
boss_4_3_img = pygame.transform.scale(boss_4_3_img, (256, 256))
boss_4_3_alpha_img = boss_4_3_img.copy()
boss_4_3_alpha_img.set_alpha(255)
boss_4_4_img = pygame.image.load("media/png/boss/boss_4_4.png")
boss_4_4_img = pygame.transform.scale(boss_4_4_img, (256, 256))
boss_4_4_alpha_img = boss_4_4_img.copy()
boss_4_4_alpha_img.set_alpha(255)

# Загрузка изображений босса Чужой Мех
boss_5_1_img = pygame.image.load("media/png/boss/boss_5_1.png")
boss_5_1_img = pygame.transform.scale(boss_5_1_img, (256, 256))
boss_5_1_alpha_img = boss_5_1_img.copy()
boss_5_1_alpha_img.set_alpha(255)
boss_5_2_img = pygame.image.load("media/png/boss/boss_5_2.png")
boss_5_2_img = pygame.transform.scale(boss_5_2_img, (256, 256))
boss_5_2_alpha_img = boss_5_2_img.copy()
boss_5_2_alpha_img.set_alpha(255)
boss_5_3_img = pygame.image.load("media/png/boss/boss_5_3.png")
boss_5_3_img = pygame.transform.scale(boss_5_3_img, (256, 256))
boss_5_3_alpha_img = boss_5_3_img.copy()
boss_5_3_alpha_img.set_alpha(255)
boss_5_4_img = pygame.image.load("media/png/boss/boss_5_4.png")
boss_5_4_img = pygame.transform.scale(boss_5_4_img, (256, 256))
boss_5_4_alpha_img = boss_5_4_img.copy()
boss_5_4_alpha_img.set_alpha(255)


# Иконки для интерфейса
obstacle_img_ex = pygame.image.load("media/png/interface/obst_explosed.png").convert_alpha()
obstacle_img_ex = pygame.transform.scale(obstacle_img_ex, (obstacle_max_size, obstacle_max_size))
g_obstacle_img_ex = pygame.image.load("media/png/interface/g_obst_explosed.png").convert_alpha()
g_obstacle_img_ex = pygame.transform.scale(g_obstacle_img_ex, (obstacle_max_size, obstacle_max_size))
interface_img_gun = pygame.image.load("media/png/interface/gun_shell.png").convert_alpha()
interface_img_gun = pygame.transform.scale(interface_img_gun, (obstacle_max_size, obstacle_max_size))
interface_img_rocket = pygame.image.load("media/png/interface/rocket_shell.png").convert_alpha()
interface_img_rocket = pygame.transform.scale(interface_img_rocket, (obstacle_max_size, obstacle_max_size))
interface_img_g_rocket = pygame.image.load("media/png/interface/g_rocket_shell.png").convert_alpha()
interface_img_g_rocket = pygame.transform.scale(interface_img_g_rocket, (obstacle_max_size, obstacle_max_size))

interface_img_shield = pygame.image.load("media/png/interface/shield_energy.png").convert_alpha()
interface_img_shield = pygame.transform.scale(interface_img_shield, (obstacle_max_size, obstacle_max_size))
interface_img_g_shield = pygame.image.load("media/png/interface/g_shield.png").convert_alpha()
interface_img_g_shield = pygame.transform.scale(interface_img_g_shield, (obstacle_max_size, obstacle_max_size))
interface_img_big_shot = pygame.image.load("media/png/interface/big_shot.png").convert_alpha()
interface_img_big_shot = pygame.transform.scale(interface_img_big_shot, (obstacle_max_size, obstacle_max_size))


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

# Первоначальные установки скинов на дефолтные
obstacle_img = obstacle_img_def
obstacle_img_prev  = obstacle_img_def

# Загрузка изображения столкновения
eximage_path = "media/png/mask/expl.png"
eximage = pygame.image.load(eximage_path)

# Загрузка изображений игрока
for img_name in player_images:
    player_img = pygame.image.load(img_name).convert_alpha()
    player_imgs.append(pygame.transform.scale(player_img, (player_size, player_size)))

# ------------------ Конец блока загрузки изображений -------------

# ------------------ Блок с циклами -------------
# Генерируем случайные нейтральные частицы и их скорости
for _ in range(60):
    x = random.randint(0, width)
    y = random.randint(0, (height - 80))
    particles.append((x, y))
    speed = random.randint(1, 5)
    speeds.append(speed)

# Формирование полотна дороги из блоков
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
# ------------------ Конец блока с циклами -------------

# ----------------------------- Блок с функциями ----------------------
def switch_language():
    global current_language
    if current_language == 'english':
        current_language = 'russian'
    else:
        current_language = 'english'

def new_stage_text(new_stage):
    if current_language == 'russian':
        display_text("Следующий уровень " + str(new_stage) + "!", game_over_text_y)
        display_text("Нажмите [Enter] чтобы продолжить.", game_over_text_y + 30)
    if current_language == 'english':
        display_text("Next stage " + str(new_stage) + "!", game_over_text_y)
        display_text("Press [Enter] for continue.", game_over_text_y + 30)


# Функция для уменьшения прозрачности изображения
def decrease_alpha(surface, amount=50, alpha=255):
    current_alpha = surface.get_alpha()
    new_alpha = max(0, current_alpha - amount)
    surface.set_alpha(new_alpha)
    return surface, new_alpha


# Функция для изменения размера изображения
def resize_image(image, new_size):
    return pygame.transform.scale(image, new_size)

# Отображение текста
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    surface.blit(text_surface, (x, y))

# Отображение текста во время паузы
def draw_text_pause(surface, text, size, x, y):
    screen.fill((0, 0, 0)) 
    screen.blit(start_img, (0, 0))
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, RED)
    surface.blit(text_surface, (x, y))

# Функции для отображения счета, жизней и текстовых сообщений
def display_score(score):
    if current_language == 'russian':
        score_text = font.render("Очки: " + str(score-1), True, WHITE)
    if current_language == 'english':
        score_text = font.render("Score: " + str(score-1), True, WHITE)
    screen.blit(score_text, (10, 10))
def display_lives(lives):
    if current_language == 'russian':
        lives_text = font.render("Энергия: " + str(lives), True, WHITE)
    if current_language == 'english':
        lives_text = font.render("Energy: " + str(lives), True, WHITE)
    screen.blit(lives_text, (width - lives_text.get_width() - 10, 10))
def display_text(text, y):
    text_render = font.render(text, True, WHITE)
    screen.blit(text_render, (width // 2 - text_render.get_width() // 2, y))

# ================================================= Функция сброса игры
def reset_game(new_stage, is_winner):
    global player_pos, is_jumping, is_moving_left, is_moving_right, move_velocity, jump_velocity, obstacle_pos, score, lives,\
        game_over, const_img, back_img, darkened_data, darkened_img, data, stage, winner, bomb_ready, wanted_size, gun_ready, shield_ready,\
        rockets_ready, tile_1, tile_2, tile_3, tile_4, ground_tile, boss_1_life, boss_2_life, boss_3_life, boss_4_life, boss_5_life,\
        obstacle_img, obstacle_img_prev, exen_b_counter, big_shot, shot_img, current_size_shot,\
        boss_1_1_alpha_img, boss_1_2_alpha_img, boss_1_3_alpha_img, boss_1_4_alpha_img,\
        boss_2_1_alpha_img, boss_2_2_alpha_img, boss_2_3_alpha_img, boss_2_4_alpha_img,\
        boss_3_1_alpha_img, boss_3_2_alpha_img, boss_3_3_alpha_img, boss_3_4_alpha_img,\
        boss_4_1_alpha_img, boss_4_2_alpha_img, boss_4_3_alpha_img, boss_4_4_alpha_img,\
        boss_5_1_alpha_img, boss_5_2_alpha_img, boss_5_3_alpha_img, boss_5_4_alpha_img,\
        g_shield, g_shield_switch, g_rockets, g_rockets_shell, g_obst_ex
    
    boss_1_1_alpha_img.set_alpha(255), boss_1_2_alpha_img.set_alpha(255), boss_1_3_alpha_img.set_alpha(255), boss_1_4_alpha_img.set_alpha(255)
    boss_2_1_alpha_img.set_alpha(255), boss_2_2_alpha_img.set_alpha(255), boss_2_3_alpha_img.set_alpha(255), boss_2_4_alpha_img.set_alpha(255)
    boss_3_1_alpha_img.set_alpha(255), boss_3_2_alpha_img.set_alpha(255), boss_3_3_alpha_img.set_alpha(255), boss_3_4_alpha_img.set_alpha(255)
    boss_4_1_alpha_img.set_alpha(255), boss_4_2_alpha_img.set_alpha(255), boss_4_3_alpha_img.set_alpha(255), boss_4_4_alpha_img.set_alpha(255)
    boss_5_1_alpha_img.set_alpha(255), boss_5_2_alpha_img.set_alpha(255), boss_5_3_alpha_img.set_alpha(255), boss_5_4_alpha_img.set_alpha(255)

    big_shot = 0
    g_obst_ex = 0
    g_rockets = 0
    g_rockets_shell = 5
    g_shield = 0
    g_shield_switch = 0

    shot_img = shot_img_1
    current_size_shot = 16
    exen_b_counter = -1
    obstacle_img = obstacle_img_def
    obstacle_img_prev  = obstacle_img_def
    boss_1_life = 30
    boss_2_life = 34
    boss_3_life = 38
    boss_4_life = 44
    boss_5_life = 48
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
    shield_ready = 1
    rockets_ready = 0
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
    if music_active == 0:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    # Загрузка заднего фона
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
    # ================================================= Конец функции сброса игры
    
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

# Функция проверки столкновения nyan(ракеты) с препятствием
def check_collision_nyan(nyan_pos, obstacle_pos):
    p_x = nyan_pos[0]
    p_y = nyan_pos[1]
    p_size = nyan_size
    o_x = obstacle_pos[0]
    o_y = obstacle_pos[1]
    o_size = obstacle_max_size
    if (o_x <= p_x < o_x + o_size) or (o_x <= p_x + p_size < o_x + o_size):
        if o_y <= p_y < o_y + o_size:
            return True
        elif o_y <= p_y + p_size < o_y + o_size:
            return True
    return False

# Функция проверки столкновения nyan(ракеты) с боссом Кибер-Панк
def check_collision_boss_1(nyan_pos, boss_1_pos):
    p_x = nyan_pos[0]
    p_y = nyan_pos[1]
    p_size = nyan_size
    o_x = boss_1_pos[0]
    o_y = boss_1_pos[1]
    o_size = boss_1_max_size
    if (o_x <= p_x < o_x + o_size) or (o_x <= p_x + p_size < o_x + o_size):
        if o_y <= p_y < o_y + o_size:
            return True
        elif o_y <= p_y + p_size < o_y + o_size:
            return True
    return False

# Функция проверки столкновения nyan(ракеты) с боссом Болотный Мех
def check_collision_boss_2(nyan_pos, boss_2_pos):
    p_x = nyan_pos[0]
    p_y = nyan_pos[1]
    p_size = nyan_size
    o_x = boss_2_pos[0]
    o_y = boss_2_pos[1]
    o_size = boss_2_max_size
    if (o_x <= p_x < o_x + o_size) or (o_x <= p_x + p_size < o_x + o_size):
        if o_y <= p_y < o_y + o_size:
            return True
        elif o_y <= p_y + p_size < o_y + o_size:
            return True
    return False

# Функция проверки столкновения nyan(ракеты) с боссом Белый Птиц
def check_collision_boss_3(nyan_pos, boss_3_pos):
    p_x = nyan_pos[0]
    p_y = nyan_pos[1]
    p_size = nyan_size
    o_x = boss_3_pos[0]
    o_y = boss_3_pos[1]
    o_size = boss_3_max_size
    if (o_x <= p_x < o_x + o_size) or (o_x <= p_x + p_size < o_x + o_size):
        if o_y <= p_y < o_y + o_size:
            return True
        elif o_y <= p_y + p_size < o_y + o_size:
            return True
    return False

# Функция проверки столкновения nyan(ракеты) с боссом Снежный Мех
def check_collision_boss_4(nyan_pos, boss_4_pos):
    p_x = nyan_pos[0]
    p_y = nyan_pos[1]
    p_size = nyan_size
    o_x = boss_4_pos[0]
    o_y = boss_4_pos[1]
    o_size = boss_4_max_size
    if (o_x <= p_x < o_x + o_size) or (o_x <= p_x + p_size < o_x + o_size):
        if o_y <= p_y < o_y + o_size:
            return True
        elif o_y <= p_y + p_size < o_y + o_size:
            return True
    return False

# Функция проверки столкновения nyan(ракеты) с боссом Чужой Мех
def check_collision_boss_5(nyan_pos, boss_5_pos):
    p_x = nyan_pos[0]
    p_y = nyan_pos[1]
    p_size = nyan_size
    o_x = boss_5_pos[0]
    o_y = boss_5_pos[1]
    o_size = boss_5_max_size
    if (o_x <= p_x < o_x + o_size) or (o_x <= p_x + p_size < o_x + o_size):
        if o_y <= p_y < o_y + o_size:
            return True
        elif o_y <= p_y + p_size < o_y + o_size:
            return True
    return False

# Функция проверки столкновения игрока с допэнергией
def check_collision_exen(player_pos, exen_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    p_size = player_size
    o_x = exen_pos[0]
    o_y = exen_pos[1]
    o_size = exen_max_size
    if (o_x <= p_x < o_x + o_size) or (o_x <= p_x + p_size < o_x + o_size):
        if o_y <= p_y < o_y + o_size:
            return True
        elif o_y <= p_y + p_size < o_y + o_size:
            return True
    return False

# Функция проверки столкновения игрока с баффом
def check_collision_exen_b(player_pos, exen_b_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    p_size = player_size
    o_x = exen_b_pos[0]
    o_y = exen_b_pos[1]
    o_size = exen_b_max_size
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

# Функция для отображения таймера
def display_timer(minutes, seconds):
    timer_text = timer_font.render(f"{timer_minutes:02}:{timer_seconds:02}", True, WHITE)
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

# ================================== Главный игровой цикл ===================================
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                paused = not paused
                
                if (paused == False) and (first_play == 1) and (music_active==0):
                    music_active = 1
                    pygame.mixer.music.unpause()
                    first_play = 0
                if (paused == False) and (first_play != 1) and (music_active==0):
                    music_active = 0
                    pygame.mixer.music.pause()
                if (paused == False) and (first_play != 1) and (music_active==1):
                    music_active = 1
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                    
            if event.key == pygame.K_l:
                switch_language()
                #print (current_language)

            if event.key == pygame.K_MINUS:
                if not paused:
                    if not game_over:
                        if music_active == 1:
                            pygame.mixer.music.pause()
                            music_active = 0
                        
                        else:
                            pygame.mixer.music.unpause()
                            music_active = 1
                        
            # --------------------- БЛОК СТРЕЛЬБЫ -----------------------
            if event.key == pygame.K_SPACE:
                if not game_over and not paused:
                    if (lives > 1) and (gun_shell > 0):
                        shot_pos = [player_pos[0] + 30, player_pos[1] + 7]  # Расположение выстрела относительно игрока
                        shot_sound.play()
                        shots.append(shot_pos)
                        gun_shell -= 1
                        if gun_shell == 0:
                            lives = lives - 1
                            gun_shell = 3
                    if (lives < 2) and not paused:
                        laser_empty.play()
            # --------------------- КОНЕЦ БЛОКА СТРЕЛЬБЫ -----------------
            # --------------------- БЛОК ракет -----------------------
            if event.key == pygame.K_x:
                if not game_over and (rockets_state != 1) and not paused:
                    if (lives > 5):
                        lives -= 5
                        rocket_launch_sound.play()
                        rockets_state = 1
                        if g_rockets == 1: rockets_shell = g_rockets_shell
                        if g_rockets == 0: rockets_shell = 3
                    else:
                        laser_empty.play()
                else:
                    if not paused:
                        laser_empty.play()
            # --------------------- КОНЕЦ БЛОКА ракет -----------------
            
            if event.key == pygame.K_UP:
                if not game_over and not paused:
                    rocket_jump_sound.play()
                    player_state = 1
                    is_jumping = True
                    jump_velocity = 10                    
            if event.key == pygame.K_ESCAPE:
                screen = pygame.display.set_mode((width, height))
            if event.key == pygame.K_TAB:
                screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

            if event.key == pygame.K_LALT:
                if not game_over and not paused:
                    if lives > 10:
                        lives = lives - 10
                        #звук подрыва энергошаров
                        laser_sound.play()
                        obstacle_state = 1

                        if (boss_1_counter == 1) and (boss_1_defeated != 1):
                            if g_obst_ex == 1: boss_1_life -=11
                            if g_obst_ex == 0: boss_1_life -=10
                            cparticles = [cParticle(boss_1_pos[0]-128, boss_1_pos[1]+128) for _ in range(cparticle_count)]
                            
                        if (boss_2_counter == 1) and (boss_2_defeated != 1):
                            if g_obst_ex == 1: boss_2_life -=12
                            if g_obst_ex == 0: boss_2_life -=11
                            cparticles = [cParticle(boss_2_pos[0]-128, boss_2_pos[1]+128) for _ in range(cparticle_count)]
                                                    
                        if (boss_3_counter == 1) and (boss_3_defeated != 1):
                            if g_obst_ex == 1: boss_3_life -=13
                            if g_obst_ex == 0: boss_3_life -=12
                            cparticles = [cParticle(boss_3_pos[0]-128, boss_3_pos[1]+128) for _ in range(cparticle_count)]
                        
                        if (boss_4_counter == 1) and (boss_4_defeated != 1):
                            if g_obst_ex == 1: boss_4_life -=14
                            if g_obst_ex == 0: boss_4_life -=13
                            cparticles = [cParticle(boss_4_pos[0]-128, boss_4_pos[1]+128) for _ in range(cparticle_count)]
                        
                        if (boss_5_counter == 1) and (boss_5_defeated != 1):
                            if g_obst_ex == 1: boss_5_life -=15
                            if g_obst_ex == 0: boss_5_life -=14
                            cparticles = [cParticle(boss_5_pos[0]-128, boss_5_pos[1]+128) for _ in range(cparticle_count)]
                            
                    else:
                        #звук что оружие не заряжено
                        laser_empty.play()

            if event.key == pygame.K_DOWN:
                if not game_over and not paused:
                    player_state = 2
                    is_jumping = False
            if event.key == pygame.K_LEFT:
                if not game_over and not paused:
                    is_moving_right = False
                    is_moving_left = True
                    move_velocity = 2
            if event.key == pygame.K_RIGHT:
                if not game_over and not paused:
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
        if lives > 5:
            rockets_ready = 1
        else:
            rockets_ready = 0
        if lives > 1:
            gun_ready = 1
        else:
            gun_ready = 0
        if lives > 0:
            shield_ready = 1
        else:
            shield_ready = 0

        # Проверка, чтобы игрок не мог прыгнуть выше верхней границы экрана
        if player_pos[1] < 1:
            player_state = 2
            is_jumping = False

        # Падение игрока, если не выполняется условие прыжка
        if not is_jumping:
            if player_pos[1] + player_size < height - (ground_height + 2):
                player_pos[1] += (gravity*10)
                player_state = 2

        # Создание nyan с заданной частотой
        if nyan_counter == 0:
            nyan_frequency = random.randint(50, 100)
            nyan_counter = nyan_frequency
            nyan_size = random.randint(nyan_min_size, nyan_max_size)
            nyan_pos[0] = 0
            #nyan_pos[1] = height - nyan_size - (ground_height + random.randint(200, 500))
            nyan_pos[1] = player_pos[1]-50
            if (rockets_state == 1) and (rockets_shell > 0):                
                nyans.append(list(nyan_pos))
                rockets_shell -= 1
                if (rockets_shell==0):
                    rockets_state = 0
        else:
            nyan_counter -= 1
        # Обновление позиций nyan и удаление вышедших за границу экрана
        for nyan in nyans:
            nyan[0] += nyan_speed
            if nyan[0] + nyan_max_size > 800:
                nyans.remove(nyan)
            
            # Проверяем столкновение с боссом Кибер-Панк    
            for boss_1 in bosses_1:
                prev_ob_0 = nyan[0]
                prev_ob_1 = nyan[1]
                if check_collision_boss_1(nyan, boss_1):
                    cparticles = [cParticle(prev_ob_0+6, prev_ob_1) for _ in range(cparticle_count)]
                    laser_sound.play()
                    nyans.remove(nyan)
                    boss_1_life -=2
                                
            # Проверяем столкновение с боссом Болотный Мех    
            for boss_2 in bosses_2:
                prev_ob_0 = nyan[0]
                prev_ob_1 = nyan[1]
                if check_collision_boss_1(nyan, boss_2):
                    cparticles = [cParticle(prev_ob_0+6, prev_ob_1) for _ in range(cparticle_count)]
                    laser_sound.play()
                    nyans.remove(nyan)
                    boss_2_life -=2
                    
            # Проверяем столкновение с боссом Белый Птиц
            for boss_3 in bosses_3:
                prev_ob_0 = nyan[0]
                prev_ob_1 = nyan[1]
                if check_collision_boss_1(nyan, boss_3):
                    cparticles = [cParticle(prev_ob_0+6, prev_ob_1) for _ in range(cparticle_count)]
                    laser_sound.play()
                    nyans.remove(nyan)
                    boss_3_life -=2
                    
            # Проверяем столкновение с боссом Снежный Мех 
            for boss_4 in bosses_4:
                prev_ob_0 = nyan[0]
                prev_ob_1 = nyan[1]
                if check_collision_boss_1(nyan, boss_4):
                    cparticles = [cParticle(prev_ob_0+6, prev_ob_1) for _ in range(cparticle_count)]
                    laser_sound.play()
                    nyans.remove(nyan)
                    boss_4_life -=2
            
            # Проверяем столкновение с боссом Чужой Мех    
            for boss_5 in bosses_5:
                prev_ob_0 = nyan[0]
                prev_ob_1 = nyan[1]
                if check_collision_boss_1(nyan, boss_5):
                    cparticles = [cParticle(prev_ob_0+6, prev_ob_1) for _ in range(cparticle_count)]
                    laser_sound.play()
                    nyans.remove(nyan)
                    boss_5_life -=2
                    
            # Проверяем столкновение с каждым энергошаром   
            for obstacle in obstacles:
                prev_ob_0 = obstacle[0]
                prev_ob_1 = obstacle[1]
                if check_collision_nyan(obstacle, nyan):
                    cparticles = [cParticle(prev_ob_0+16, prev_ob_1+20) for _ in range(cparticle_count)]
                    laser_sound.play()
                    #nyans.remove(nyan)
                    obstacles.remove(obstacle)
            else:
            # Добавление частицы следа
                nyan_particle_size = random.randint(3, 6)
                nyan_particle_pos = [nyan[0], nyan[1] + 30 // 2]
                nyan_particle_img = pygame.transform.scale(nyan_particle_image_2, (nyan_particle_size, nyan_particle_size))
                nyan_particles.append({'pos': nyan_particle_pos, 'image': nyan_particle_img, 'alpha': 255})

        # ---------------------- начало блока босса -----------------
        if (timer_minutes == 1 and timer_seconds == 12):
            if (stage == 1):
                boss_1_appear, boss_5_appear, boss_4_appear, boss_3_appear, boss_2_appear = 1, 0, 0, 0, 0
                boss_death_sound.play()
            if (stage == 2):
                boss_2_appear, boss_1_appear, boss_5_appear, boss_4_appear, boss_3_appear = 1, 0, 0, 0, 0
                boss_death_sound.play()
            if (stage == 3):
                boss_3_appear, boss_2_appear, boss_1_appear, boss_5_appear, boss_4_appear = 1, 0, 0, 0, 0
                boss_death_sound.play()
            if (stage == 4):
                boss_4_appear, boss_3_appear, boss_2_appear, boss_1_appear, boss_5_appear = 1, 0, 0, 0, 0
                boss_death_sound.play()
            if (stage == 5):
                boss_5_appear, boss_4_appear, boss_3_appear, boss_2_appear, boss_1_appear = 1, 0, 0, 0, 0
                boss_death_sound.play()

        # Создание босса Кибер Панк если пришло его время и он не побеждён
        if boss_1_appear == 1 and boss_1_defeated == 0:
            if (boss_1_counter == 0):
                boss_1_frequency = 1
                boss_1_counter = boss_1_frequency
                boss_1_size = random.randint(boss_1_min_size, boss_1_max_size)
                boss_1_pos[0] = width
                boss_1_pos[1] = height - boss_1_size - (ground_height - 1)
                bosses_1.append(list(boss_1_pos))
            else:
                boss_1_counter = 1
            # Обновление позиций босса
            boss_1_appear = 1
            for boss_1 in bosses_1:
                if boss_1_appear == 1:
                    boss_1[0] -= boss_1_speed
                if (boss_1_appear == 1) and (boss_1[0] < 580):
                    boss_1_appear = 0
        
        # Создание босса Болотный Мех если пришло его время и он не побеждён
        if boss_2_appear == 1 and boss_2_defeated == 0:
            if (boss_2_counter == 0):
                boss_2_frequency = 1
                boss_2_counter = boss_2_frequency
                boss_2_size = random.randint(boss_2_min_size, boss_2_max_size)
                boss_2_pos[0] = width
                boss_2_pos[1] = height - boss_2_size - (ground_height - 1)
                bosses_2.append(list(boss_2_pos))
            else:
                boss_2_counter = 1
            # Обновление позиций босса
            boss_2_appear = 1
            for boss_2 in bosses_2:
                if boss_2_appear == 1:
                    boss_2[0] -= boss_2_speed
                if (boss_2_appear == 1) and (boss_2[0] < 580):
                    boss_2_appear = 0
        
        # Создание босса Белый Птиц если пришло его время и он не побеждён
        if boss_3_appear == 1 and boss_3_defeated == 0:
            if (boss_3_counter == 0):
                boss_3_frequency = 1
                boss_3_counter = boss_3_frequency
                boss_3_size = random.randint(boss_3_min_size, boss_3_max_size)
                boss_3_pos[0] = width
                boss_3_pos[1] = height - boss_3_size - (ground_height - 1)
                bosses_3.append(list(boss_3_pos))
            else:
                boss_3_counter = 1
            # Обновление позиций босса
            boss_3_appear = 1
            for boss_3 in bosses_3:
                if boss_3_appear == 1:
                    boss_3[0] -= boss_3_speed
                if (boss_3_appear == 1) and (boss_3[0] < 580):
                    boss_3_appear = 0
        
        # Создание босса Снежный Мех если пришло его время и он не побеждён
        if boss_4_appear == 1 and boss_4_defeated == 0:
            if (boss_4_counter == 0):
                boss_4_frequency = 1
                boss_4_counter = boss_4_frequency
                boss_4_size = random.randint(boss_4_min_size, boss_4_max_size)
                boss_4_pos[0] = width
                boss_4_pos[1] = height - boss_4_size - (ground_height - 1)
                bosses_4.append(list(boss_4_pos))
            else:
                boss_4_counter = 1
            # Обновление позиций босса
            boss_4_appear = 1
            for boss_4 in bosses_4:
                if boss_4_appear == 1:
                    boss_4[0] -= boss_4_speed
                if (boss_4_appear == 1) and (boss_4[0] < 580):
                    boss_4_appear = 0
        
        # Создание босса Чужой Мех если пришло его время и он не побеждён
        if boss_5_appear == 1 and boss_5_defeated == 0:
            if (boss_5_counter == 0):
                boss_5_frequency = 1
                boss_5_counter = boss_5_frequency
                boss_5_size = random.randint(boss_5_min_size, boss_5_max_size)
                boss_5_pos[0] = width
                boss_5_pos[1] = height - boss_5_size - (ground_height - 64)
                bosses_5.append(list(boss_5_pos))
            else:
                boss_5_counter = 1
            # Обновление позиций босса
            boss_5_appear = 1
            for boss_5 in bosses_5:
                if boss_5_appear == 1:
                    boss_5[0] -= boss_5_speed
                if (boss_5_appear == 1) and (boss_5[0] < 580):
                    boss_5_appear = 0
        # ---------------------- конец блока босса -----------------

        # Создание допэнергии с заданной частотой
        if exen_counter == 0:
            exen_frequency = random.randint(50, 350)
            exen_counter = exen_frequency
            exen_size = random.randint(exen_min_size, exen_max_size)
            exen_pos[0] = width
            exen_pos[1] = height - exen_size - (ground_height + random.randint(200, 600))
            exens.append(list(exen_pos))
        else:
            exen_counter -= 1
        # Обновление позиций допэнергии и удаление вышедших за границу экрана
        for exen in exens:
            exen[0] -= exen_speed
            if exen[0] + exen_max_size < 0:
                exens.remove(exen)
            else:
            # Добавление частицы следа
                nyan_particle_size = random.randint(8, 10)
                nyan_particle_pos = [exen[0], exen[1] + 10]
                nyan_particle_img = pygame.transform.scale(nyan_particle_image, (nyan_particle_size, nyan_particle_size))
                nyan_particles.append({'pos': nyan_particle_pos, 'image': nyan_particle_img, 'alpha': 255})
            if check_collision_exen(player_pos, exen):
                    lives += 1
                    cparticles = [cParticle(player_pos[0]+16, player_pos[1]-16) for _ in range(cparticle_count)]
                    new_life_sound.play()
                    exens.remove(exen)

        # С какого момента начинают вылетать дроны типа 2
        if timer_minutes==00 and timer_seconds == 30 and exen_b_counter < 0:
            exen_b_counter = 0

        # Обновление щита
        if (timer_seconds == 20 or timer_seconds == 40 or timer_seconds == 0) and (g_shield == 1 and g_shield_switch == 0):
            g_shield_switch = 1
            shield_on_sound.play()

        # Создание допэнергии с заданной частотой
        if exen_b_counter == 0:
            exen_b_frequency = random.randint(500, 1000)
            exen_b_counter = exen_b_frequency
            exen_b_size = random.randint(exen_b_min_size, exen_b_max_size)
            exen_b_pos[0] = width
            exen_b_pos[1] = height - exen_b_size - (ground_height + random.randint(200, 500))
            exens_b.append(list(exen_b_pos))
        else:
            exen_b_counter -= 1
        # Обновление позиций допэнергии и удаление вышедших за границу экрана
        for exen_b in exens_b:
            exen_b[0] -= exen_b_speed
            if exen_b[0] + exen_b_max_size < 0:
                exens_b.remove(exen_b)
            else:
            # Добавление частицы следа
                nyan_particle_size = random.randint(8, 10)
                nyan_particle_pos = [exen_b[0], exen_b[1] + 10]
                nyan_particle_img = pygame.transform.scale(nyan_particle_image_2, (nyan_particle_size, nyan_particle_size))
                nyan_particles.append({'pos': nyan_particle_pos, 'image': nyan_particle_img, 'alpha': 255})
            if check_collision_exen_b(player_pos, exen_b):
                    #Логика выбора бонусного баффа
                    sel_bonus = random.randint(1,4)

                    if sel_bonus == 1 and g_shield == 0:
                        g_shield = 1
                        g_shield_switch = 1
                    
                    if sel_bonus == 2 and big_shot == 0:
                        big_shot = 1
                        current_size_shot = 32
                        shot_img = shot_img_2

                    if sel_bonus == 3 and g_rockets == 0: g_rockets = 1

                    if sel_bonus == 4 and g_obst_ex == 0: g_obst_ex = 1

                    if big_shot == 1 or g_shield == 1:
                        lives += 2

                                       
                    
                    
                        
                    cparticles = [cParticle(player_pos[0]+16, player_pos[1]-16) for _ in range(cparticle_count)]
                    new_life_sound.play()
                    exens_b.remove(exen_b)
            

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
                if score > 1:
                    score -= 1
                    
            if check_collision_tank(player_pos, tank):
                if g_shield == 1 and g_shield_switch == 0: lives -= 1
                if g_shield == 0: lives -= 1
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
                    lives += 1
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
                if (score > 450):
                    game_over = True
                    winner = 1
                    if (stage == 1):
                        if (boss_1_defeated == 1):
                            winner = 1
                        else:
                            winner = 0
                            
                    if (stage == 2):
                        if (boss_2_defeated == 1):
                            winner = 1
                        else:
                            winner = 0
                            
                    if (stage == 3):
                        if (boss_3_defeated == 1):
                            winner = 1
                        else:
                            winner = 0
                            
                    if (stage == 4):
                        if (boss_4_defeated == 1):
                            winner = 1
                        else:
                            winner = 0
                            
                    if (stage == 5):
                        if (boss_5_defeated == 1):
                            winner = 1
                        else:
                            winner = 0
                            
                    boss_1_appear, boss_1_counter, boss_1_defeated = 0, 0, 0
                    boss_2_appear, boss_2_counter, boss_2_defeated = 0, 0, 0
                    boss_3_appear, boss_3_counter, boss_3_defeated = 0, 0, 0
                    boss_4_appear, boss_4_counter, boss_4_defeated = 0, 0, 0
                    boss_5_appear, boss_5_counter, boss_5_defeated = 0, 0, 0
                    break
        
        # Проверка столкновения игрока с препятствием
            if check_collision(player_pos, obstacle):
                if g_shield == 1 and g_shield_switch == 0: lives -= 1
                if g_shield == 0: lives -= 1
                if lives < 1:
                    cparticles = [cParticle(player_pos[0]+16, player_pos[1]-16) for _ in range(cparticle_count)]
                    collision_sound.play()
                    game_over = True
                   
                    boss_1_appear, boss_1_counter, boss_1_defeated = 0, 0, 0
                    boss_2_appear, boss_2_counter, boss_2_defeated = 0, 0, 0
                    boss_3_appear, boss_3_counter, boss_3_defeated = 0, 0, 0
                    boss_4_appear, boss_4_counter, boss_4_defeated = 0, 0, 0
                    boss_5_appear, boss_5_counter, boss_5_defeated = 0, 0, 0
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
            else:
                # Добавление частицы следа
                if big_shot == 0:
                    nyan_particle_size = random.randint(3, 5)
                    nyan_particle_pos = [shot[0], shot[1] + (current_size_shot / 2)]
                    nyan_particle_img = pygame.transform.scale(nyan_particle_image_2, (nyan_particle_size, nyan_particle_size))
                    nyan_particles.append({'pos': nyan_particle_pos, 'image': nyan_particle_img, 'alpha': 255})
                if big_shot == 1:
                    nyan_particle_size = random.randint(3, 5)
                    nyan_particle_pos = [shot[0], shot[1] + (current_size_shot / 2)]
                    nyan_particle_img = pygame.transform.scale(nyan_particle_image, (nyan_particle_size, nyan_particle_size))
                    nyan_particles.append({'pos': nyan_particle_pos, 'image': nyan_particle_img, 'alpha': 255})

        # Проверка столкновений выстрелов с препятствиями
        for shot in shots[:]:
            for obstacle in obstacles[:]:
                # Прямоугольники для проверок столкновений
                shot_rect = pygame.Rect(shot[0], shot[1], 16, 16)
                obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], 30, 30)
                if shot_rect.colliderect(obstacle_rect):  # Проверка на столкновение
                    score = score + 1
                    ocparticles = [ocParticle(shot[0], shot[1]) for _ in range(ocparticle_count)]
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
                    ocparticles = [ocParticle(shot[0], shot[1]) for _ in range(ocparticle_count)]
                    laser_sound.play()
                    shots.remove(shot)
                    tanks.remove(tank)
                    break
        
        for shot in shots[:]:
            for boss_1 in bosses_1[:]:
                # Прямоугольники для проверок столкновений
                shot_rect = pygame.Rect(shot[0], shot[1], 16, 16)
                boss_1_rect = pygame.Rect(boss_1[0], boss_1[1], 256, 256)
                if shot_rect.colliderect(boss_1_rect):  # Проверка на столкновение
                    ocparticles = [ocParticle(shot[0], shot[1]) for _ in range(ocparticle_count)]
                    laser_sound.play()
                    shots.remove(shot)
                    if big_shot == 0:
                        boss_1_life -=1
                    if big_shot == 1:
                        boss_1_life -=2
                    break
        
        for shot in shots[:]:
            for boss_2 in bosses_2[:]:
                # Прямоугольники для проверок столкновений
                shot_rect = pygame.Rect(shot[0], shot[1], 16, 16)
                boss_2_rect = pygame.Rect(boss_2[0], boss_2[1], 256, 256)
                if shot_rect.colliderect(boss_2_rect):  # Проверка на столкновение
                    ocparticles = [ocParticle(shot[0], shot[1]) for _ in range(ocparticle_count)]
                    laser_sound.play()
                    shots.remove(shot)
                    if big_shot == 0:
                        boss_2_life -=1
                    if big_shot == 1:
                        boss_2_life -=2
                    break
        
        for shot in shots[:]:
            for boss_3 in bosses_3[:]:
                # Прямоугольники для проверок столкновений
                shot_rect = pygame.Rect(shot[0], shot[1], 16, 16)
                boss_3_rect = pygame.Rect(boss_3[0], boss_3[1], 256, 256)
                if shot_rect.colliderect(boss_3_rect):  # Проверка на столкновение
                    ocparticles = [ocParticle(shot[0], shot[1]) for _ in range(ocparticle_count)]
                    laser_sound.play()
                    shots.remove(shot)
                    if big_shot == 0:
                        boss_3_life -=1
                    if big_shot == 1:
                        boss_3_life -=2
                    break
        
        for shot in shots[:]:
            for boss_4 in bosses_4[:]:
                # Прямоугольники для проверок столкновений
                shot_rect = pygame.Rect(shot[0], shot[1], 16, 16)
                boss_4_rect = pygame.Rect(boss_4[0], boss_4[1], 256, 256)
                if shot_rect.colliderect(boss_4_rect):  # Проверка на столкновение
                    ocparticles = [ocParticle(shot[0], shot[1]) for _ in range(ocparticle_count)]
                    laser_sound.play()
                    shots.remove(shot)
                    if big_shot == 0:
                        boss_4_life -=1
                    if big_shot == 1:
                        boss_4_life -=2
                    break
        
        for shot in shots[:]:
            for boss_5 in bosses_5[:]:
                # Прямоугольники для проверок столкновений
                shot_rect = pygame.Rect(shot[0], shot[1], 16, 16)
                boss_5_rect = pygame.Rect(boss_5[0], boss_5[1], 256, 256)
                if shot_rect.colliderect(boss_5_rect):  # Проверка на столкновение
                    ocparticles = [ocParticle(shot[0], shot[1]) for _ in range(ocparticle_count)]
                    laser_sound.play()
                    shots.remove(shot)
                    if big_shot == 0:
                        boss_5_life -=1
                    if big_shot == 1:
                        boss_5_life -=2
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

         # Обновление координат нейтральных частиц
        for i, particle in enumerate(particles):
            x, y = particle
            speed = speeds[i]
            x -= speed
            if x < 0:
                x = width
            particles[i] = (x, y)
    
        # Отрисовка нейтральных частиц
        for particle in particles:
            x, y = particle
            pygame.draw.circle(screen, (p_pr, p_pg, p_pb), (x, y), random.randint(1, 2))

               
        pass

        # Логика изменения размера
        if resizing:
            current_size += resize_speed
            current_size_shot += resize_speed_shot

            if current_size > wanted_size:  # Например, максимальный размер 100 пикселей
                resize_speed = -resize_speed
            elif current_size < obstacle_min_size:  # Вернуться к минимальному размеру
                resize_speed = -resize_speed

            if current_size_shot == wanted_size_shot:  # Например, максимальный размер 100 пикселей
                resize_speed_shot = -resize_speed_shot
            elif current_size_shot != 16:  # Вернуться к минимальному размеру
                resize_speed_shot = -resize_speed_shot
        
        obstacle_img_sized = resize_image(obstacle_img, (current_size, current_size))
        shot_img_sized = resize_image(shot_img, (current_size_shot, current_size_shot))


        # Обновление и рисование частиц
        for nyan_particle in nyan_particles[:]:
            nyan_particle['alpha'] -= 5  # Замедление затухания
            nyan_particle_surf = nyan_particle['image'].copy()
            nyan_particle_surf.set_alpha(nyan_particle['alpha'])
            screen.blit(nyan_particle_surf, nyan_particle['pos'])

        # Удаление затухших частиц
            if nyan_particle['alpha'] <= 0:
                nyan_particles.remove(nyan_particle)

        # Отрисовка nyan
        for nyan in nyans:
            screen.blit(nyan_img, nyan)    
        
        # Отрисовка допэнергии
        for exen in exens:
            screen.blit(exen_img, exen)
        
        # Отрисовка баффов
        for exen_b in exens_b:
            screen.blit(exen_b_img, exen_b)


        # Отрисовка босса Кибер Панк
        for boss_1 in bosses_1:
                if boss_1_state == 0:
                    if boss_1_life < 5:
                        screen.blit(boss_1_3_alpha_img, boss_1)
                    else:
                        screen.blit(boss_1_1_alpha_img, boss_1)
                if boss_1_state == 1:
                    if boss_1_life < 5:
                        screen.blit(boss_1_4_alpha_img, boss_1)
                    else:
                        screen.blit(boss_1_2_alpha_img, boss_1)

        # Отрисовка босса Болотный Мех
        for boss_2 in bosses_2:
            if boss_2_state == 0:
                if boss_2_life < 5:
                    screen.blit(boss_2_3_alpha_img, boss_2)
                else:
                    screen.blit(boss_2_1_alpha_img, boss_2)
            if boss_2_state == 1:
                if boss_2_life < 5:
                    screen.blit(boss_2_4_alpha_img, boss_2)
                else:
                    screen.blit(boss_2_2_alpha_img, boss_2)
        
        # Отрисовка босса Белый Птиц
        for boss_3 in bosses_3:
            if boss_3_state == 0:
                if boss_3_life < 5:
                    screen.blit(boss_3_3_alpha_img, boss_3)
                else:
                    screen.blit(boss_3_1_alpha_img, boss_3)
            if boss_3_state == 1:
                if boss_3_life < 5:
                    screen.blit(boss_3_4_alpha_img, boss_3)
                else:
                    screen.blit(boss_3_2_alpha_img, boss_3)
        
        # Отрисовка босса Снежный Мех
        for boss_4 in bosses_4:
            if boss_4_state == 0:
                if boss_4_life < 5:
                    screen.blit(boss_4_3_alpha_img, boss_4)
                else:
                    screen.blit(boss_4_1_alpha_img, boss_4)
            if boss_4_state == 1:
                if boss_4_life < 5:
                    screen.blit(boss_4_4_alpha_img, boss_4)
                else:
                    screen.blit(boss_4_2_alpha_img, boss_4)
        
        

        # Отрисовка препятствий
        for obstacle in obstacles:
            screen.blit(obstacle_img_sized, obstacle)

        # Отрисовка танков
        for tank in tanks:
            screen.blit(tank_img, tank)

        # Отрисовка босса Чужой Мех
        for boss_5 in bosses_5:
            if boss_5_state == 0:
                if boss_5_life < 5:
                    screen.blit(boss_5_3_alpha_img, boss_5)
                else:
                        screen.blit(boss_5_1_alpha_img, boss_5)
            if boss_5_state == 1:
                if boss_5_life < 5:
                    screen.blit(boss_5_4_alpha_img, boss_5)
                else:
                    screen.blit(boss_5_2_alpha_img, boss_5)
        #=========================== Частицы на первом плане =========================
        for cparticle in cparticles:
            cparticle.move()
            cparticle.draw(screen)

        for ocparticle in ocparticles:
            ocparticle.move()
            ocparticle.draw(screen)
        #=============================================================================

        if shield_ready == 1:
            screen.blit(interface_img_shield, (790-30, 40))
        if gun_ready == 1:
            screen.blit(interface_img_gun, (755-30, 40))
        if rockets_ready == 1:
            screen.blit(interface_img_rocket, (720-30, 40))
        if bomb_ready == 1:
            screen.blit(obstacle_img_ex, (685-30, 40))
        
        if g_shield == 1:
            screen.blit(interface_img_g_shield, (10, 40))
        if big_shot == 1:
            screen.blit(interface_img_big_shot, (45, 40))
        if g_rockets == 1:
            screen.blit(interface_img_g_rocket, (80, 40))
        if g_obst_ex == 1:
            screen.blit(g_obstacle_img_ex, (115, 40))

        # Тик так для анимации
        tiktak += 1
        if tiktak > 30:
            tiktak = 0


        if obstacle_state == 1:
            obstacle_img = obstacle_img_ex_2
            if tiktak == 15:
                if g_obst_ex == 1:
                    if len(obstacles) > 0:
                        ex_lives = round(len(obstacles) / 10)
                        lives = lives + ex_lives
                        print(ex_lives)
                    score = score + len(obstacles)
                obstacles.clear()
                obstacle_img = obstacle_img_prev
                obstacle_state = 0


        if tiktak == 1:
            if boss_1_state == 0: boss_1_state = 1
            if boss_2_state == 0: boss_2_state = 1
            if boss_3_state == 0: boss_3_state = 1
            if boss_4_state == 0: boss_4_state = 1
            if boss_5_state == 0: boss_5_state = 1
                
        if tiktak == 15:
            if boss_1_state == 1: boss_1_state = 0
            if boss_2_state == 1: boss_2_state = 0
            if boss_3_state == 1: boss_3_state = 0
            if boss_4_state == 1: boss_4_state = 0
            if boss_5_state == 1: boss_5_state = 0
        
        if tiktak == 16 and winner !=1:
            if boss_1_defeated == 0 and stage == 1 and not game_over:
                if boss_1_life < 1:
                    boss_1_1_alpha_img, new_alpha = decrease_alpha(boss_1_1_alpha_img)
                    boss_1_2_alpha_img, new_alpha = decrease_alpha(boss_1_2_alpha_img)
                    boss_1_3_alpha_img, new_alpha = decrease_alpha(boss_1_3_alpha_img)
                    boss_1_4_alpha_img, new_alpha = decrease_alpha(boss_1_4_alpha_img)
                    if (new_alpha < 60):
                        boss_1_defeated = 1
                    if boss_1_defeated == 1:
                        cparticles = [cParticle(boss_1_pos[0]-128, boss_1_pos[1]+128) for _ in range(cparticle_count)]
                        boss_death_sound.play()
                        bosses_1.remove(boss_1)

            if boss_2_defeated == 0 and stage == 2 and not game_over:
                if boss_2_life < 1:
                    boss_2_1_alpha_img, new_alpha = decrease_alpha(boss_2_1_alpha_img)
                    boss_2_2_alpha_img, new_alpha = decrease_alpha(boss_2_2_alpha_img)
                    boss_2_3_alpha_img, new_alpha = decrease_alpha(boss_2_3_alpha_img)
                    boss_2_4_alpha_img, new_alpha = decrease_alpha(boss_2_4_alpha_img)
                    if (new_alpha < 60):
                        boss_2_defeated = 1
                    if boss_2_defeated == 1:
                        cparticles = [cParticle(boss_2_pos[0]-128, boss_2_pos[1]+128) for _ in range(cparticle_count)]
                        boss_death_sound.play()
                        bosses_2.remove(boss_2)
            if boss_3_defeated == 0 and stage == 3 and not game_over:
                if boss_3_life < 1:
                    boss_3_1_alpha_img, new_alpha = decrease_alpha(boss_3_1_alpha_img)
                    boss_3_2_alpha_img, new_alpha = decrease_alpha(boss_3_2_alpha_img)
                    boss_3_3_alpha_img, new_alpha = decrease_alpha(boss_3_3_alpha_img)
                    boss_3_4_alpha_img, new_alpha = decrease_alpha(boss_3_4_alpha_img)
                    if (new_alpha < 60):
                        boss_3_defeated = 1
                    if boss_3_defeated == 1:
                        cparticles = [cParticle(boss_3_pos[0]-128, boss_3_pos[1]+128) for _ in range(cparticle_count)]
                        boss_death_sound.play()
                        bosses_3.remove(boss_3)
            if boss_4_defeated == 0 and stage == 4 and not game_over:
                if boss_4_life < 1:
                    boss_4_1_alpha_img, new_alpha = decrease_alpha(boss_4_1_alpha_img)
                    boss_4_2_alpha_img, new_alpha = decrease_alpha(boss_4_2_alpha_img)
                    boss_4_3_alpha_img, new_alpha = decrease_alpha(boss_4_3_alpha_img)
                    boss_4_4_alpha_img, new_alpha = decrease_alpha(boss_4_4_alpha_img)
                    if (new_alpha < 60):
                        boss_4_defeated = 1
                    if boss_4_defeated == 1:
                        cparticles = [cParticle(boss_4_pos[0]-128, boss_4_pos[1]+128) for _ in range(cparticle_count)]
                        boss_death_sound.play()
                        bosses_4.remove(boss_4)
            if boss_5_defeated == 0 and stage == 5 and not game_over:
                if boss_5_life < 1:
                    boss_5_1_alpha_img, new_alpha = decrease_alpha(boss_5_1_alpha_img)
                    boss_5_2_alpha_img, new_alpha = decrease_alpha(boss_5_2_alpha_img)
                    boss_5_3_alpha_img, new_alpha = decrease_alpha(boss_5_3_alpha_img)
                    boss_5_4_alpha_img, new_alpha = decrease_alpha(boss_5_4_alpha_img)
                    if (new_alpha < 60):
                        boss_5_defeated = 1
                    if boss_5_defeated == 1:
                        cparticles = [cParticle(boss_5_pos[0]-128, boss_5_pos[1]+128) for _ in range(cparticle_count)]
                        boss_death_sound.play()
                        bosses_5.remove(boss_5)

        # Смена спрайтов по таймеру каждые 10, 20 и 30 кадров
        if tiktak == 10 or tiktak == 20 or tiktak == 30:

            # Анимация бега
            if player_state == 0:
                if current_img_index != 0: current_img_index = 0
                else:
                    current_img_index = 1
            # Анимация полёта на ранце
            if player_state == 1:
                if current_img_index != 2: current_img_index = 2
                else:
                    current_img_index = 3
            # Анимация падения
            if player_state == 2:
                if current_img_index != 4: current_img_index = 4
                else:
                    current_img_index = 5
            # Анимация столкновения
            if player_state == 3:
                if g_shield == 1 and g_shield_switch == 1:
                    g_shield_switch = 0 
                if current_img_index != 4: current_img_index = 4
                else:
                    current_img_index = 5

        # Рендеринг изображения игрока
        screen.blit(player_imgs[current_img_index], player_pos)

        if player_state == 3 or (g_shield == 1 and g_shield_switch == 1):
            screen.blit(eximage, player_pos)
            if player_state !=0:
                nyan_particle_size = random.randint(4, 7)
                nyan_particle_pos = [player_pos[0]+5, player_pos[1] + 30 // 2]
                nyan_particle_img = pygame.transform.scale(nyan_particle_image_2, (nyan_particle_size, nyan_particle_size))
                nyan_particles.append({'pos': nyan_particle_pos, 'image': nyan_particle_img, 'alpha': 255})
        else:
            # Добавление частицы следа
            if player_state == 1:
                nyan_particle_size = random.randint(4, 7)
                nyan_particle_pos = [player_pos[0]+5, player_pos[1] + 30 // 2]
                nyan_particle_img = pygame.transform.scale(nyan_particle_image_2, (nyan_particle_size, nyan_particle_size))
                nyan_particles.append({'pos': nyan_particle_pos, 'image': nyan_particle_img, 'alpha': 255})
    
        # Отображение текстовых сообщений при окончании игры
        if game_over:
            bosses_1.clear(), bosses_2.clear(), bosses_3.clear(), bosses_4.clear(), bosses_5.clear()
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
                
                if current_language == 'russian':
                    display_text("Вы проиграли... :(", game_over_text_y)
                    display_text("Нажмите [Enter] и начните заново.", game_over_text_y + 30)
                if current_language == 'english':
                    display_text("You lost... :(", game_over_text_y)
                    display_text("Press [Enter] for restart.", game_over_text_y + 30)
                
                font = pygame.font.Font(None, 26)
                display_text("Fractel " + version, game_over_text_y + 260)
                display_text("game by Stanislav Nixman", game_over_text_y + 280)
                font = pygame.font.Font(None, 36)
                is_winner = 0
            
            if winner == 1:
                # Смена уровней
                if (stage == 1):
                    new_stage = 2
                    display_score(score_show)
                    display_timer(timer_minutes, timer_seconds)
                    display_lives(lives)
                    new_stage_text(new_stage)
                    is_winner = 1
                if (stage == 2):
                    new_stage = 3
                    display_score(score_show)
                    display_timer(timer_minutes, timer_seconds)
                    display_lives(lives)
                    new_stage_text(new_stage)
                    is_winner = 1
                if (stage == 3):
                    new_stage = 4
                    display_score(score_show)
                    display_timer(timer_minutes, timer_seconds)
                    display_lives(lives)
                    new_stage_text(new_stage)
                    is_winner = 1
                if (stage == 4):
                    new_stage = 5
                    display_score(score_show)
                    display_timer(timer_minutes, timer_seconds)
                    display_lives(lives)
                    new_stage_text(new_stage)
                    is_winner = 1

                if (stage == 5):
                    new_stage = 1
                    display_score(score_show)
                    display_timer(timer_minutes, timer_seconds)
                    display_lives(lives)
                    if current_language == 'russian':
                        display_text("Вы прошли игру! :)", game_over_text_y)
                        display_text("Нажмите [Enter] для перезапуска.", game_over_text_y + 50)
                    if current_language == 'english':
                        display_text("You win this game! :)", game_over_text_y)
                        display_text("Press [Enter] for restart. ", game_over_text_y + 50)
                    is_winner = 1

        else:
            display_score(score)
            display_lives(lives)

        if (timer_minutes == 00 and timer_seconds > 0 and timer_seconds < 8):
            font = pygame.font.Font(None, 36)
            if current_language == 'russian':
                display_text("Наберите 450 очков!", game_over_text_y - 40)
            if current_language == 'english':
                display_text("Score 450 points!", game_over_text_y - 40)
          
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

       
    
    if paused:
        if current_language == 'english':
            draw_text_pause(screen, "Press [P] to play!", 50, width // 2 - 140, height // 2 - 200)
        if current_language == 'russian':
            draw_text_pause(screen, "Нажмите [P] чтобы играть!", 50, width // 2 - 230, height // 2 - 200)
        font = pygame.font.Font(None, 28)
        
        if current_language == 'english':
            display_text("Controls:", game_over_text_y + 60)
            display_text("[Up] jump. [Down] fall.", game_over_text_y + 90)
            display_text("[Left-Right] moves horisontally. [P] pause.", game_over_text_y + 110)
            display_text("[SPACE, X, Left ALT] weapons.", game_over_text_y + 130)
            display_text("[TAB / ESC] fullscreen / windowed mode.", game_over_text_y + 160)
            display_text("[Minus] music on/off, [L] RU/ENG language.", game_over_text_y + 180)
            display_text("Fractel v" + version, game_over_text_y + 220)
            display_text("game by Stanislav Nixman", game_over_text_y + 240)
            font = pygame.font.Font(None, 36)
        if current_language == 'russian':
            display_text("Управление:", game_over_text_y + 60)
            display_text("[Вверх] прыжок. [Вниз] падение", game_over_text_y + 90)
            display_text("[Влево-Вправо] туда-сюда. [P] пауза.", game_over_text_y + 110)
            display_text("[SPACE, X, Left ALT] оружие.", game_over_text_y + 130)
            display_text("[TAB / ESC] полный экран / в окне.", game_over_text_y + 160)
            display_text("[Минус] вкл/выкл музыку. [L] RU/ENG язык.", game_over_text_y + 180)
            display_text("Fractel v" + version, game_over_text_y + 220)
            display_text("игра Станислава Никсмана", game_over_text_y + 240)
            font = pygame.font.Font(None, 36)
    
    # Обновление дисплея
    pygame.display.flip()

    # Ограничение частоты обновления экрана
    clock.tick(30)

# ================================== Конец главного игрового цикла ===================================

pygame.quit()
