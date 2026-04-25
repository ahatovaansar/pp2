import pygame
import random
import time
import os


pygame.init()
pygame.mixer.init()


WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20 

# Create display
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

# Fonts
score_font = pygame.font.SysFont("Verdana", 25)

# --- ЗВУКИ ---
eat_sound = None

try:
    print("Проверка файлов...")
    print("Музыка:", os.path.exists("images/snake.wav"))
    print("Еда:", os.path.exists("images/eat_sound.wav"))

    pygame.mixer.music.load("images/snake.wav")
    pygame.mixer.music.set_volume(0.5)

    eat_sound = pygame.mixer.Sound("images/eat_sound.wav")

    print("Звук успешно загружен ✅")

except Exception as e:
    print("Ошибка загрузки звука ❌:", e)



def display_ui(score, level):
    value = score_font.render(f"Score: {score}  Level: {level}", True, YELLOW)
    dis.blit(value, [10, 10])

def generate_food_pos(snake_list):
    while True:
        food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
        food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
        if [food_x, food_y] not in snake_list:
            return food_x, food_y

def gameLoop():
    game_over = False
    game_close = False

  
    try:
        pygame.mixer.music.play(-1)
        print("Музыка играет 🎵")
    except Exception as e:
        print("Ошибка воспроизведения:", e)

    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    score = 0
    level = 1
    current_speed = 7

    foodx, foody = generate_food_pos(snake_list)

    while not game_over:

        while game_close:
            pygame.mixer.music.stop()

            dis.fill(BLUE)
            msg = score_font.render("Game Over! Press C-Play or Q-Quit", True, RED)
            dis.blit(msg, [WIDTH / 6, HEIGHT / 3])
            display_ui(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)

        
        pygame.draw.rect(dis, GREEN, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for block in snake_list:
            pygame.draw.rect(dis, WHITE, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

        display_ui(score, level)
        pygame.display.update()

        
        if x1 == foodx and y1 == foody:
            if eat_sound:
                eat_sound.play()

            foodx, foody = generate_food_pos(snake_list)
            length_of_snake += 1
            score += 1

            if score % 3 == 0:
                level += 1
                current_speed += 1

        clock.tick(current_speed)

    pygame.quit()
    quit()

gameLoop()