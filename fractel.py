import pygame
from pygame.locals import *
from pygame.surfarray import make_surface
import random
import time
import math

pygame.init()
pygame.mixer.init()

# Загрузка звуковых файлов
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.8) 

collision_sound = pygame.mixer.Sound("collision.mp3")
rocket_jump_sound = pygame.mixer.Sound("rocket_jump.mp3")
new_stage_sound = pygame.mixer.Sound("new_stage.mp3")
new_life_sound = pygame.mixer.Sound("new_life.mp3")

#Проверка выиграл или проиграл
winner = 0

# Инициализация окна
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("FRACTEL")

WHITE = (255, 255, 255)

# Создаем списки для хранения координат и скоростей частиц
particles = []
speeds = []
# Цвета частиц в RGB
p_pr = 7
p_pg = 121
p_pb = 212

# Генерируем случайные частицы и их скорости
for _ in range(100):
    x = random.randint(0, width)
    y = random.randint(0, height)
    particles.append((x, y))
    speed = random.randint(1, 5)
    speeds.append(speed)


# Загрузка заднего фона
back_img = pygame.image.load("back.png").convert_alpha()
back_img = pygame.transform.scale(back_img, (width, height))

const_img = pygame.image.load("const.png").convert_alpha()
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

# Параметры скроллинга и игрового процесса
scrolling_speed = 2
obstacle_speed = random.randint(4, 6)
score = 1
lives = 3
second_chance=0

# Параметры фоновых блоков
tile_size = 32
tiles_per_row = width // tile_size + 1
tiles_per_col = ground_height // tile_size + 1
ground_tiles = []

# Загрузка изображений
for row in range(tiles_per_col):
    for col in range(tiles_per_row):
        ground_tile = pygame.image.load("solid.png")
        ground_tile = pygame.transform.scale(ground_tile, (tile_size, tile_size))
        ground_tiles.append((ground_tile, (col * tile_size, height - (row + 1) * tile_size)))

obstacle_img_def = pygame.image.load("obst.png")
obstacle_img_def = pygame.transform.scale(obstacle_img_def, (obstacle_max_size, obstacle_max_size))
obstacle_img_g = pygame.image.load("obst_green.png")
obstacle_img_g = pygame.transform.scale(obstacle_img_g, (obstacle_max_size, obstacle_max_size))
obstacle_img_y = pygame.image.load("obst_yellow.png")
obstacle_img_y = pygame.transform.scale(obstacle_img_y, (obstacle_max_size, obstacle_max_size))
obstacle_img_r = pygame.image.load("obst_red.png")
obstacle_img_r = pygame.transform.scale(obstacle_img_r, (obstacle_max_size, obstacle_max_size))
obstacle_img_f = pygame.image.load("obst_final.png")
obstacle_img_f = pygame.transform.scale(obstacle_img_f, (obstacle_max_size, obstacle_max_size))
obstacle_img = obstacle_img_def


# Загрузка изображений игрока
player_images = ['Player_stand_1.png', 'Player_stand_2.png', 'Player_jump_1.png', 'Player_jump_2.png', 'Player_1.png', 'Player_2.png']

# Загрузка изображений игрока
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

# Загрузка изображения столкновения
eximage_path = "expl.png"
eximage = pygame.image.load(eximage_path)


# Шрифт для отображения счета и жизней
font = pygame.font.Font(None, 36)


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
def reset_game():
    global player_pos, is_jumping, jump_velocity, obstacle_pos, score, lives, game_over
    player_pos = [width / 2, height - player_size - ground_height]
    is_jumping = False
    jump_velocity = 10
    obstacle_pos[0] = width
    score = 1
    lives = 3
    game_over = False
    obstacle_frequency = 0
    obstacle_counter = 0
    
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

running = True
is_jumping = False
clock = pygame.time.Clock()
game_over = False
game_over_text_y = height // 2 - 40
obstacle_frequency = 0
obstacle_counter = 0
obstacles = []

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

# Главный игровой цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over:
                    rocket_jump_sound.play()
                    player_state = 1
                    is_jumping = True
                    jump_velocity = 10                    
            if event.key == pygame.K_ESCAPE:
                screen = pygame.display.set_mode((width, height))
            if event.key == pygame.K_TAB:
                screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
            if event.key == pygame.K_LCTRL:
                player_state = 2
                is_jumping = False
         
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

    # Ограничение игрока относительно земли
    if player_pos[1] > height - player_size - ground_height:
        player_pos[1] = height - player_size - (ground_height + 2)
        player_state = 0

    # Проверка, чтобы игрок не мог прыгнуть выше верхней границы экрана
    if player_pos[1] < 1:
        player_state = 2
        is_jumping = False

    # Падение игрока, если не выполняется условие прыжка
    if not is_jumping:
        if player_pos[1] + player_size < height - (ground_height + 2):
            player_pos[1] += (gravity*10)
            player_state = 2

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
        obstacle[0] -= (obstacle_speed - 1)

        if obstacle[0] + obstacle_max_size < 0:
            obstacles.remove(obstacle)
            score += 1
            # Каждые 10 очков даём жизнь
            if ((score-1) % 10) == 0:
                new_life_sound.play()
                lives +=1
            # На 50 очках сброс интенсивности и замена спрайта
            if (score == 50):
                darkened_data = (data * 0.6)
                darkened_img = make_surface(darkened_data)
                new_stage_sound.play()
                obstacle_img = obstacle_img_g
                second_chance = 48
                p_pr = 19
                p_pg = 186
                p_pb = 0
            # На 100 очках сброс интенсивности и замена спрайта
            if (score == 100):
                darkened_data = (data * 0.8)
                darkened_img = make_surface(darkened_data)
                new_stage_sound.play()
                obstacle_img = obstacle_img_y
                second_chance = 98
                p_pr = 219
                p_pg = 200
                p_pb = 0
            # На 200 очках сброс интенсивности и замена спрайта
            if (score == 200):
                darkened_data = (data * 0.9)
                darkened_img = make_surface(darkened_data)
                new_stage_sound.play()
                obstacle_img = obstacle_img_r
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
                game_over = True
                break
            else:
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

    # Проверка, не вышел ли фон за пределы экрана
    if x_offset < -back_img.get_width():
        x_offset = back_img.get_width() - 1  # Возвращаем фон на начало
   
    # Отрисовка фоновых блоков
    for ground_tile in ground_tiles:
        screen.blit(ground_tile[0], ground_tile[1])
    
    # Отрисовка препятствий
    for obstacle in obstacles:
        screen.blit(obstacle_img, obstacle)

        # Анимация изображения игрока
    tiktak += 1
    if tiktak > 30:
        tiktak = 0

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
        if winner == 0:
            display_score(score)
            display_timer(timer_minutes, timer_seconds)
            display_lives(lives)
            obstacles.clear()
            # проиграть проигрыш?
            pygame.mixer.music.stop()
            obstacle_img = obstacle_img_def
            display_text("Вы проиграли :(", game_over_text_y)
            display_text("Нажмите Enter, чтобы начать заново", game_over_text_y + 40)
            display_text("Space - прыжок. LCTRL - отключение ранца", game_over_text_y + 80)
            display_text("TAB - полноэкранный режим. ESC - оконный режим", game_over_text_y + 120)
            display_text("Game by Stanislav Nixman Developed 18-20 august 2024", game_over_text_y + 160)

        if winner == 1:
            display_score(score)
            display_timer(timer_minutes, timer_seconds)
            display_lives(lives)
            obstacles.clear()
            # проиграть победную?
            pygame.mixer.music.stop()
            obstacle_img = obstacle_img_def
            display_text("ПОЗДРАВЛЯЮ С ПОБЕДОЙ!", game_over_text_y)
            display_text("Нажмите Enter, чтобы начать заново", game_over_text_y + 40)
            display_text("Space - прыжок. LCTRL - отключение ранца", game_over_text_y + 80)
            display_text("TAB - полноэкранный режим. ESC - оконный режим", game_over_text_y + 120)
            display_text("Game by Stanislav Nixman Developed 18-20 august 2024", game_over_text_y + 160)
            
    else:
        display_score(score)
        display_lives(lives)
    
    # Обработка ввода клавиатуры для перезапуска игры
    keys = pygame.key.get_pressed()
    if game_over and keys[pygame.K_RETURN]:
        timer_counter = 0
        timer_minutes = 0
        timer_seconds = 0
        pygame.mixer.music.play(-1)
        reset_game()

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
        pygame.draw.circle(screen, (p_pr, p_pg, p_pb), (x, y), random.randint(1, 2))  # Здесь вы можете задать цвет и размер частиц


    # Обновление дисплея
    pygame.display.flip()

    # Ограничение частоты обновления экрана
    clock.tick(30)

pygame.quit()
