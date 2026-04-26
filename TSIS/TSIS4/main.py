import pygame
import json
from db import get_or_create_player, get_personal_best, get_top_scores
from game import run_game

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()


def input_username():
    username = ""
    while True:
        screen.fill((30,30,30))
        screen.blit(font.render("Enter username:", True, (255,255,255)), (150,120))
        screen.blit(font.render(username, True, (0,255,0)), (150,180))

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


def game_over_screen(score, level):
    while True:
        screen.fill((0,0,0))
        screen.blit(font.render("GAME OVER", True, (255,0,0)), (180,100))
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (200,160))
        screen.blit(font.render("R - Retry", True, (255,255,255)), (200,220))
        screen.blit(font.render("ESC - Menu", True, (255,255,255)), (200,260))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "retry"
                if event.key == pygame.K_ESCAPE:
                    return "menu"


# 🔥 ПОЛНОСТЬЮ ИСПРАВЛЕННЫЙ SETTINGS
def settings_screen():
    with open("settings.json") as f:
        settings = json.load(f)

    while True:
        screen.fill((0,0,0))

        screen.blit(font.render("SETTINGS", True, (255,255,255)), (200,60))

        screen.blit(font.render(f"Sound: {settings['sound']}", True, (255,255,255)), (180,120))
        screen.blit(font.render(f"Grid: {settings['grid']}", True, (255,255,255)), (180,160))
        screen.blit(font.render(f"Color: {settings['snake_color']}", True, (255,255,255)), (180,200))

        screen.blit(font.render("S - toggle sound", True, (200,200,200)), (150,250))
        screen.blit(font.render("G - toggle grid", True, (200,200,200)), (150,280))
        screen.blit(font.render("C - change color", True, (200,200,200)), (150,310))
        screen.blit(font.render("ESC - save & back", True, (200,200,200)), (150,340))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]

                elif event.key == pygame.K_g:
                    settings["grid"] = not settings["grid"]

                elif event.key == pygame.K_c:
                    if settings["snake_color"] == [0,255,0]:
                        settings["snake_color"] = [255,0,0]
                    elif settings["snake_color"] == [255,0,0]:
                        settings["snake_color"] = [0,0,255]
                    else:
                        settings["snake_color"] = [0,255,0]

                elif event.key == pygame.K_ESCAPE:
                    with open("settings.json", "w") as f:
                        json.dump(settings, f)
                    return


def leaderboard_screen():
    scores = get_top_scores()

    while True:
        screen.fill((0,0,0))
        screen.blit(font.render("Leaderboard", True, (255,255,255)), (180,40))

        y = 100
        for i, row in enumerate(scores):
            screen.blit(font.render(f"{i+1}. {row[0]} - {row[1]}", True, (255,255,255)), (120,y))
            y += 30

        screen.blit(font.render("ESC - Back", True, (200,200,200)), (180,350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


def main_menu():
    while True:
        screen.fill((0,0,0))

        screen.blit(font.render("Snake Game", True, (255,255,255)), (180,60))
        screen.blit(font.render("1 - Play", True, (255,255,255)), (200,140))
        screen.blit(font.render("2 - Leaderboard", True, (255,255,255)), (200,180))
        screen.blit(font.render("3 - Settings", True, (255,255,255)), (200,220))
        screen.blit(font.render("ESC - Quit", True, (255,255,255)), (200,260))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    username = input_username()
                    player_id = get_or_create_player(username)
                    best = get_personal_best(player_id)

                    while True:
                        result = run_game(player_id, best)
                        action = game_over_screen(*result)

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