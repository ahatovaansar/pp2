import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# 🎧 музыка
try:
    pygame.mixer.music.load("images/snake.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    print("⚠️ Ошибка загрузки музыки")

CELL = 20
COLS, ROWS = 30, 25
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 30, 30)
GRAY = (40, 40, 40)
BLUE = (50, 50, 200)
YELLOW = (240, 200, 0)

font = pygame.font.SysFont('Arial', 20, bold=True)

# ---------------- WALLS ----------------
def draw_walls():
    for x in range(COLS):
        pygame.draw.rect(screen, GRAY, (x * CELL, 0, CELL, CELL))
        pygame.draw.rect(screen, GRAY, (x * CELL, (ROWS - 1) * CELL, CELL, CELL))
    for y in range(ROWS):
        pygame.draw.rect(screen, GRAY, (0, y * CELL, CELL, CELL))
        pygame.draw.rect(screen, GRAY, ((COLS - 1) * CELL, y * CELL, CELL, CELL))

def is_wall(x, y):
    return x <= 0 or x >= COLS - 1 or y <= 0 or y >= ROWS - 1

# ---------------- FOOD ----------------
def random_food(snake_body):
    while True:
        x = random.randint(2, COLS - 3)
        y = random.randint(2, ROWS - 3)
        if (x, y) not in snake_body and not is_wall(x, y):

            # 🎯 разные типы еды
            food_type = random.choices(
                ["normal", "bonus", "rare"],
                weights=[60, 30, 10]
            )[0]

            return (x, y, food_type)

# ---------------- GAME ----------------
def run():
    clock = pygame.time.Clock()

    snake = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)

    food_x, food_y, food_type = random_food(snake)

    food_timer = pygame.time.get_ticks()
    food_lifetime = 5000

    score = 0
    level = 1

    speed = 5   # ✅ всегда INT (нет лагов)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        head = snake[0]
        new_head = (head[0] + direction[0], head[1] + direction[1])

        # 💀 столкновение
        if is_wall(new_head[0], new_head[1]) or new_head in snake:
            restart = game_over(score, level)
            if restart:
                return run()
            else:
                pygame.quit()
                sys.exit()

        snake.insert(0, new_head)

        # 🍎 еда
        if new_head == (food_x, food_y):

            if food_type == "normal":
                score += 10
            elif food_type == "bonus":
                score += 20
            elif food_type == "rare":
                score += 50

            # ⚡ стабильное ускорение (без лагов)
            if speed < 15:
                speed += 1

            # 📈 уровень
            if score % 50 == 0:
                level += 1

            food_x, food_y, food_type = random_food(snake)
            food_timer = pygame.time.get_ticks()

        else:
            snake.pop()

        # ⏱ исчезновение еды
        if pygame.time.get_ticks() - food_timer > food_lifetime:
            food_x, food_y, food_type = random_food(snake)
            food_timer = pygame.time.get_ticks()

        # 🎨 рисуем
        screen.fill(BLACK)
        draw_walls()

        if food_type == "normal":
            color = RED
        elif food_type == "bonus":
            color = BLUE
        else:
            color = YELLOW

        pygame.draw.rect(screen, color,
                         (food_x * CELL, food_y * CELL, CELL, CELL))

        for i, seg in enumerate(snake):
            color = GREEN if i > 0 else DARK_GREEN
            pygame.draw.rect(screen, color,
                             (seg[0] * CELL, seg[1] * CELL, CELL, CELL))

        info_y = ROWS * CELL + 8
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, info_y))
        screen.blit(font.render(f"Level: {level}", True, WHITE), (150, info_y))
        screen.blit(font.render(f"Speed: {speed}", True, WHITE), (290, info_y))

        pygame.display.flip()
        clock.tick(speed)

# ---------------- GAME OVER ----------------
def game_over(score, level):
    pygame.mixer.music.stop()

    screen.fill(BLACK)

    big_font = pygame.font.SysFont('Arial', 40, bold=True)
    screen.blit(big_font.render("GAME OVER", True, RED),
                (WIDTH // 2 - 120, HEIGHT // 2 - 60))
    screen.blit(font.render(f"Score: {score}  Level: {level}", True, WHITE),
                (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(font.render("R - Restart  Q - Quit", True, WHITE),
                (WIDTH // 2 - 110, HEIGHT // 2 + 40))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.music.play(-1)
                    return True
                if event.key == pygame.K_q:
                    return False

# ---------------- START ----------------
if __name__ == '__main__':
    run()