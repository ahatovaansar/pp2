import sys
import random
import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
BASE_SPEED = 5

WHITE = (255,255,255)
BLACK = (0,0,0)
DARK_GRAY = (60,60,60)
RED = (220,20,60)
BLUE = (50,130,255)
GREEN = (0,200,120)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 42)

score = 0
coins_collected = 0

# 🔊 SOUND
crash_sound = pygame.mixer.Sound("images/crash.wav")

pygame.mixer.music.load("images/background.wav")
pygame.mixer.music.play(-1)

# ---------------- ROAD ----------------
class Road:
    def __init__(self):
        self.line_y = 0

    def update(self, speed):
        self.line_y += speed
        if self.line_y >= 40:
            self.line_y = 0

    def draw(self, surface):
        surface.fill(GREEN)
        pygame.draw.rect(surface, DARK_GRAY, (50,0,300,SCREEN_HEIGHT))

        pygame.draw.line(surface, WHITE, (50,0), (50,SCREEN_HEIGHT), 4)
        pygame.draw.line(surface, WHITE, (350,0), (350,SCREEN_HEIGHT), 4)

        for y in range(-40, SCREEN_HEIGHT, 40):
            pygame.draw.rect(surface, WHITE, (195, y+self.line_y, 10, 25))

# ---------------- PLAYER ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40,70), pygame.SRCALPHA)
        pygame.draw.rect(self.image, BLUE, (5,10,30,50), border_radius=8)
        self.rect = self.image.get_rect(center=(200,520))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self.rect.move_ip(-6,0)
        if keys[K_RIGHT]:
            self.rect.move_ip(6,0)

        if self.rect.left < 55:
            self.rect.left = 55
        if self.rect.right > 345:
            self.rect.right = 345

# ---------------- ENEMY ----------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40,70), pygame.SRCALPHA)
        pygame.draw.rect(self.image, RED, (5,10,30,50), border_radius=8)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(80,320), -80)

    def move(self, speed):
        global score
        self.rect.move_ip(0, speed)

        if self.rect.top > SCREEN_HEIGHT:
            score += 1
            self.reset()

# ---------------- COIN ----------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/coin.png")
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        # Coin with different values (weights)
        self.value = random.choices(
            [1,3,5],                  # possible values
            weights=[60,30,10]        # probability
        )[0]
        self.rect.center = (random.randint(80,320), -40)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

# ---------------- OBJECTS ----------------
road = Road()
player = Player()
enemy = Enemy()
coin = Coin()

enemies = pygame.sprite.Group(enemy)
coins = pygame.sprite.Group(coin)
all_sprites = pygame.sprite.Group(player, enemy, coin)

# ---------------- LOOP ----------------
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # Speed increases depending on collected coins
    SPEED = BASE_SPEED + coins_collected // 5

    # Move road animation
    road.update(SPEED)
    player.move()
    enemy.move(SPEED)
    coin.move(SPEED)

    # If player collects coin → add its value
    if pygame.sprite.spritecollideany(player, coins):
        coins_collected += coin.value
        coin.spawn()

    # Collision with enemy → Game Over
    if pygame.sprite.spritecollideany(player, enemies):

        pygame.mixer.music.stop()
        crash_sound.play()

        game_over = True

        while game_over:
            screen.fill(BLACK)

            text1 = font_big.render("GAME OVER", True, WHITE)
            text2 = font_small.render(f"Score: {score}", True, WHITE)
            text3 = font_small.render(f"Coins: {coins_collected}", True, WHITE)
            text4 = font_small.render("R - Restart    Q - Quit", True, WHITE)

            screen.blit(text1, (SCREEN_WIDTH//2 - text1.get_width()//2, 200))
            screen.blit(text2, (SCREEN_WIDTH//2 - text2.get_width()//2, 270))
            screen.blit(text3, (SCREEN_WIDTH//2 - text3.get_width()//2, 310))
            screen.blit(text4, (SCREEN_WIDTH//2 - text4.get_width()//2, 360))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_r:
                        score = 0
                        coins_collected = 0
                        player.rect.center = (200,520)
                        enemy.reset()
                        coin.spawn()

                        pygame.mixer.music.play(-1)

                        game_over = False

    road.draw(screen)

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    score_text = font_small.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10,10))

    coin_text = font_small.render(f"Coins: {coins_collected}", True, WHITE)
    screen.blit(coin_text, (250,10))

    pygame.display.update()
    clock.tick(FPS)