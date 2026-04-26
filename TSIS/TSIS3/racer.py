import pygame
import random
import json
from persistence import save_leaderboard

pygame.init()
pygame.mixer.init()

def run_game(username):
    WIDTH, HEIGHT = 400, 600

    ROAD_X = 50
    ROAD_WIDTH = 300
    ROAD_RIGHT = ROAD_X + ROAD_WIDTH

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    with open("settings.json") as f:
        settings = json.load(f)

    car_color = tuple(settings["car_color"])

    try:
        crash_sound = pygame.mixer.Sound("assets/crash.wav")
    except:
        crash_sound = None

    LANES = [120, 200, 280]

    BASE_SPEED = {
        "easy": 4,
        "normal": 6,
        "hard": 9
    }[settings["difficulty"]]

    player = pygame.Rect(200, 500, 40, 70)

    enemies = []
    obstacles = []
    items = []

    score = 0
    coins = 0
    distance = 0

    power_active = None
    power_timer = 0
    is_repaired = False

    popup_text = ""
    popup_timer = 0

    line_offset = 0

    def clamp(rect):
        if rect.left < ROAD_X:
            rect.left = ROAD_X
        if rect.right > ROAD_RIGHT:
            rect.right = ROAD_RIGHT

    def spawn_enemy():
        lane = random.choice(LANES)
        enemies.append(pygame.Rect(lane-20, -80, 40, 70))

    def spawn_obstacle():
        lanes_used = [o["rect"].centerx for o in obstacles if o["rect"].y < 150]
        free_lanes = [l for l in LANES if l not in lanes_used]

        if not free_lanes:
            return

        lane = random.choice(free_lanes)

        obstacles.append({
            "rect": pygame.Rect(lane-15, -50, 30, 30),
            "type": random.choice(["barrier","oil","slow"])
        })

    def spawn_item():
        items.append({
            "rect": pygame.Rect(random.choice(LANES)-15, -50, 30, 30),
            "type": random.choice(["coin","power"])
        })

    def save_score():
        try:
            with open("leaderboard.json") as f:
                data = json.load(f)
        except:
            data = []

        data.append({"name": username, "score": score, "distance": distance})
        data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
        save_leaderboard(data)

    def draw_road():
        screen.fill((0,180,90))
        pygame.draw.rect(screen, (60,60,60), (ROAD_X,0,ROAD_WIDTH,HEIGHT))

        pygame.draw.line(screen, (255,255,0), (ROAD_X,0), (ROAD_X,HEIGHT), 4)
        pygame.draw.line(screen, (255,255,0), (ROAD_RIGHT,0), (ROAD_RIGHT,HEIGHT), 4)

        for y in range(-40, HEIGHT, 60):
            pygame.draw.rect(screen, (255,255,255),
                (195, y + line_offset, 10, 30), border_radius=4)

    def draw_car(rect, color):
        pygame.draw.rect(screen, color, rect, border_radius=18)

        # окно
        pygame.draw.rect(screen, (30,30,30),
            (rect.x+8, rect.y+10, 24, 20), border_radius=5)

        # колёса
        pygame.draw.circle(screen, (20,20,20), (rect.x+6, rect.y+15), 4)
        pygame.draw.circle(screen, (20,20,20), (rect.x+34, rect.y+15), 4)
        pygame.draw.circle(screen, (20,20,20), (rect.x+6, rect.y+55), 4)
        pygame.draw.circle(screen, (20,20,20), (rect.x+34, rect.y+55), 4)

    spawn_enemy()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                save_score()
                return score, distance

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 7
        if keys[pygame.K_RIGHT]:
            player.x += 7

        clamp(player)

        speed = BASE_SPEED + distance // 6000
        now = pygame.time.get_ticks()

        if power_active == "nitro":
            speed += 3

        distance += speed
        line_offset = (line_offset + speed) % 60

        if random.randint(1, 90) == 1:
            spawn_enemy()

        if random.randint(1, 140) == 1:
            spawn_obstacle()

        if random.randint(1, 25) == 1:
            spawn_item()

        for en in enemies:
            en.y += speed
        enemies = [e for e in enemies if e.y < HEIGHT]

        for obj in obstacles:
            obj["rect"].y += speed
        obstacles = [o for o in obstacles if o["rect"].y < HEIGHT]

        for obj in items:
            obj["rect"].y += speed
        items = [o for o in items if o["rect"].y < HEIGHT]

        collision = False

        for en in enemies:
            if player.colliderect(en):
                collision = True

        for obj in obstacles:
            if player.colliderect(obj["rect"]):
                if obj["type"] == "barrier":
                    collision = True
                elif obj["type"] == "oil":
                    player.x += random.choice([-50,50])
                    clamp(player)
                elif obj["type"] == "slow":
                    speed = max(2, speed-2)

        for obj in items:
            if player.colliderect(obj["rect"]):
                if obj["type"] == "coin":
                    coins += 1

                elif obj["type"] == "power":
                    if power_active is None:
                        new = random.choice(["nitro","shield","repair"])

                        if new == "repair":
                            is_repaired = True
                            power_active = "repair"
                            popup_text = "REPAIR"

                        elif new == "shield":
                            power_active = "shield"
                            popup_text = "SHIELD"

                        else:
                            power_active = "nitro"
                            power_timer = now
                            popup_text = "NITRO"

                        popup_timer = now

                items.remove(obj)

        if power_active and power_active != "repair":
            if now - power_timer > 5000:
                power_active = None

        if collision:
            if power_active == "shield":
                power_active = None
                collision = False

            elif is_repaired:
                is_repaired = False
                power_active = None
                collision = False

            else:
                if settings["sound"] and crash_sound:
                    crash_sound.play()
                save_score()
                return score, distance

        score = coins * 10 + distance // 100

        draw_road()
        draw_car(player, car_color)

        for en in enemies:
            draw_car(en, (200,50,50))

        for obj in obstacles:
            color = (120,120,120)
            if obj["type"] == "oil": color = (20,20,20)
            if obj["type"] == "slow": color = (255,140,0)
            pygame.draw.rect(screen, color, obj["rect"], border_radius=8)

        # ✔ КРУГЛЫЕ предметы
        for obj in items:
            if obj["type"] == "coin":
                pygame.draw.circle(screen, (255,215,0), obj["rect"].center, 12)
            else:
                pygame.draw.circle(screen, (0,255,255), obj["rect"].center, 12)

        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
        screen.blit(font.render(f"Dist: {distance}", True, (255,255,255)), (10,40))

        # ✔ ТЕКСТ POWER-UP
        if popup_text:
            if pygame.time.get_ticks() - popup_timer < 2000:
                text = font.render(popup_text, True, (0,255,255))
                screen.blit(text, (150,100))
            else:
                popup_text = ""

        pygame.display.flip()
        clock.tick(60)