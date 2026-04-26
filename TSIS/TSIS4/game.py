# TSIS 4: Snake Game 

import pygame
import random
from db import save_game
import json

# Load settings
with open("settings.json") as f:
    settings = json.load(f)

snake_color = settings["snake_color"]
sound_enabled = settings["sound"]

def run_game(player_id, best_score):
    pygame.init()
    pygame.mixer.init()

    try:
        eat_sound = pygame.mixer.Sound("assets/snake.wav")
    except:
        eat_sound = None

    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    snake = [(100, 100)]
    direction = (20, 0)

    food = (200, 200)
    poison = (300, 200)

    power_up = None
    power_spawn_time = 0
    effect = None
    effect_time = 0

    obstacles = []

    score = 0
    level = 1
    running = True

    while running:
        screen.fill((0, 0, 0))

        # управление (без разворота назад)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != (0, 20):
            direction = (0, -20)
        elif keys[pygame.K_DOWN] and direction != (0, -20):
            direction = (0, 20)
        elif keys[pygame.K_LEFT] and direction != (20, 0):
            direction = (-20, 0)
        elif keys[pygame.K_RIGHT] and direction != (-20, 0):
            direction = (20, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(player_id, score, level)
                return score, level

        # GRID
        if settings["grid"]:
            for x in range(0, WIDTH, 20):
                pygame.draw.line(screen, (40,40,40), (x,0), (x,HEIGHT))
            for y in range(0, HEIGHT, 20):
                pygame.draw.line(screen, (40,40,40), (0,y), (WIDTH,y))

        # движение
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, head)

        # FOOD
        if head == food:
            score += 10
            if sound_enabled and eat_sound:
                eat_sound.play()

            while True:
                food = (random.randrange(0, WIDTH, 20), random.randrange(0, HEIGHT, 20))
                if food not in snake and food not in obstacles:
                    break

            # уровень каждые 3 еды
            if score % 30 == 0:
                level += 1

                if level >= 3:
                    obstacles = []
                    while len(obstacles) < 5:
                        block = (
                            random.randrange(0, WIDTH, 20),
                            random.randrange(0, HEIGHT, 20)
                        )

                        # безопасный спавн
                        if (
                            block not in snake and
                            block != food and
                            block != poison and
                            abs(block[0] - head[0]) > 40
                        ):
                            obstacles.append(block)
        else:
            snake.pop()

        # POISON
        if head == poison:
            if sound_enabled and eat_sound:
                eat_sound.play()

            if len(snake) > 2:
                snake = snake[:-2]
            else:
                running = False

            poison = (random.randrange(0, WIDTH, 20), random.randrange(0, HEIGHT, 20))

        # POWER-UP SPAWN
        if power_up is None and random.randint(1, 60) == 1:
            while True:
                new_power = (
                    random.randrange(0, WIDTH, 20),
                    random.randrange(0, HEIGHT, 20)
                )
                if new_power not in snake and new_power not in obstacles:
                    power_up = new_power
                    power_spawn_time = pygame.time.get_ticks()
                    break

        # исчезает через 8 сек
        if power_up and pygame.time.get_ticks() - power_spawn_time > 8000:
            power_up = None

        # подбор
        if power_up and head == power_up:
            if sound_enabled and eat_sound:
                eat_sound.play()

            effect = random.choice(["speed", "slow", "shield"])
            effect_time = pygame.time.get_ticks()
            power_up = None

        # длительность эффекта
        if effect and pygame.time.get_ticks() - effect_time > 5000:
            effect = None

        # скорость
        speed = 5 + level
        if effect == "speed":
            speed = 9
        elif effect == "slow":
            speed = 3

        # COLLISION
        collision = (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake[1:] or
            head in obstacles
        )

        if collision:
            if effect == "shield":
                effect = None
                snake.pop(0)
            else:
                running = False

        # DRAW
        color = (0,255,255) if effect == "shield" else snake_color

        for s in snake:
            pygame.draw.rect(screen, color, (*s, 20, 20))

        pygame.draw.rect(screen, (255, 0, 0), (*food, 20, 20))
        pygame.draw.rect(screen, (150, 0, 0), (*poison, 20, 20))

        if power_up:
            pygame.draw.rect(screen, (0, 0, 255), (*power_up, 20, 20))

        for o in obstacles:
            pygame.draw.rect(screen, (100, 100, 100), (*o, 20, 20))

        # UI
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10, 10))
        screen.blit(font.render(f"Best: {best_score}", True, (255,255,255)), (10, 40))
        screen.blit(font.render(f"Level: {level}", True, (255,255,255)), (10, 70))

        if effect:
            screen.blit(font.render(f"Effect: {effect}", True, (255,255,0)), (10, 100))

        pygame.display.flip()
        clock.tick(speed)

    save_game(player_id, score, level)
    return score, level