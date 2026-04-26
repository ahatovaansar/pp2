import pygame

def show_leaderboard(screen, font, data):
    screen.fill((0,0,0))
    screen.blit(font.render("LEADERBOARD", True, (255,255,255)), (80,50))

    y = 120
    for i, row in enumerate(data):
        text = f"{i+1}. {row['name']} - {row['score']} ({row['distance']})"
        screen.blit(font.render(text, True, (255,255,255)), (50, y))
        y += 30

    pygame.display.flip()