import pygame
import json
from racer import run_game
from persistence import load_leaderboard
from ui import show_leaderboard

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()


def input_username():
    username = ""
    while True:
        screen.fill((30, 30, 30))
        screen.blit(font.render("Enter name:", True, (255, 255, 255)), (100, 200))
        screen.blit(font.render(username, True, (0, 255, 0)), (100, 260))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return username or "player"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode


def leaderboard_screen():
    data = load_leaderboard()
    while True:
        show_leaderboard(screen, font, data)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return


def settings_screen():
    with open("settings.json") as f:
        settings = json.load(f)

    while True:
        screen.fill((0, 0, 0))

        screen.blit(font.render("SETTINGS", True, (255, 255, 255)), (100, 100))
        screen.blit(font.render(f"Sound: {settings['sound']}", True, (255, 255, 255)), (80, 200))
        screen.blit(font.render(f"Difficulty: {settings['difficulty']}", True, (255, 255, 255)), (80, 250))

        screen.blit(font.render("S - toggle sound", True, (200, 200, 200)), (60, 350))
        screen.blit(font.render("D - difficulty", True, (200, 200, 200)), (60, 390))
        screen.blit(font.render("C - car color", True, (200, 200, 200)), (60, 430))
        screen.blit(font.render("ESC - back", True, (200, 200, 200)), (100, 470))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]

                if event.key == pygame.K_d:
                    order = ["easy", "normal", "hard"]
                    idx = order.index(settings["difficulty"])
                    settings["difficulty"] = order[(idx + 1) % 3]

                if event.key == pygame.K_c:
                    import random
                    settings["car_color"] = [random.randint(0, 255) for _ in range(3)]

                if event.key == pygame.K_ESCAPE:
                    with open("settings.json", "w") as f:
                        json.dump(settings, f, indent=4)
                    return


def game_over_screen(score, distance):
    while True:
        screen.fill((0, 0, 0))
        screen.blit(font.render("GAME OVER", True, (255, 0, 0)), (90, 150))
        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (100, 220))
        screen.blit(font.render(f"Dist: {distance}", True, (255, 255, 255)), (100, 260))
        screen.blit(font.render("R - retry", True, (200, 200, 200)), (100, 320))
        screen.blit(font.render("ESC - menu", True, (200, 200, 200)), (100, 360))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "retry"
                if event.key == pygame.K_ESCAPE:
                    return "menu"


def main_menu():
    while True:
        screen.fill((0, 0, 0))

        screen.blit(font.render("Racer Game", True, (255, 255, 255)), (90, 100))
        screen.blit(font.render("1 - Play", True, (255, 255, 255)), (120, 200))
        screen.blit(font.render("2 - Leaderboard", True, (255, 255, 255)), (120, 250))
        screen.blit(font.render("3 - Settings", True, (255, 255, 255)), (120, 300))
        screen.blit(font.render("ESC - Quit", True, (255, 255, 255)), (120, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    username = input_username()
                    while True:
                        score, dist = run_game(username)
                        action = game_over_screen(score, dist)
                        if action == "menu":
                            break

                elif event.key == pygame.K_2:
                    leaderboard_screen()

                elif event.key == pygame.K_3:
                    settings_screen()

                elif event.key == pygame.K_ESCAPE:
                    exit()

        clock.tick(30)


main_menu()