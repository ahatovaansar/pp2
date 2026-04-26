import pygame
import sys
import datetime
from tools import draw_line, normalize_rect, flood_fill

pygame.init()
pygame.mouse.set_visible(False)

WIDTH, HEIGHT = 900, 600
TOOLBAR_HEIGHT = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

# COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (220,220,220)
RED = (255,0,0)
GREEN = (0,180,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PURPLE = (160,32,240)
ORANGE = (255,140,0)

colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

current_color = BLACK
brush_size = 5
tool = "brush"

drawing = False
start_pos = None
last_pos = None
preview_pos = None

typing = False
text = ""
text_pos = (0,0)

CLEAR_BTN = pygame.Rect(WIDTH - 120, 20, 100, 40)

def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0,0,WIDTH,TOOLBAR_HEIGHT))

    text_surface = font.render(
        "B Brush | L Line | R Rect | O Circle | S Square | T Triangle | Q EqTri | H Rhombus | F Fill | X Text | 1/2/3 Size | Ctrl+S Save",
        True, BLACK)
    screen.blit(text_surface, (10,50))

    for i, color in enumerate(colors):
        rect = pygame.Rect(20+i*50, 10, 35, 35)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    pygame.draw.rect(screen, RED, CLEAR_BTN)
    pygame.draw.rect(screen, BLACK, CLEAR_BTN, 2)
    txt = font.render("Clear", True, WHITE)
    screen.blit(txt, (CLEAR_BTN.x+15, CLEAR_BTN.y+10))


while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # ===== TEXT MODE =====
            if typing:
                if event.key == pygame.K_RETURN:
                    canvas.blit(font.render(text, True, current_color), text_pos)
                    typing = False
                    tool = "brush"
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    tool = "brush"
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                continue

            # ===== SAVE (FIXED) =====
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = "assets/" + datetime.datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, filename)
                print("Saved:", filename)

            # ===== TOOLS =====
            elif event.key == pygame.K_b: tool="brush"
            elif event.key == pygame.K_l: tool="line"
            elif event.key == pygame.K_r: tool="rectangle"
            elif event.key == pygame.K_o: tool="circle"
            elif event.key == pygame.K_s: tool="square"
            elif event.key == pygame.K_t: tool="triangle"
            elif event.key == pygame.K_q: tool="eq_triangle"
            elif event.key == pygame.K_h: tool="rhombus"
            elif event.key == pygame.K_f: tool="fill"
            elif event.key == pygame.K_x: tool="text"

            # ===== SIZE =====
            elif event.key == pygame.K_1: brush_size = 2
            elif event.key == pygame.K_2: brush_size = 5
            elif event.key == pygame.K_3: brush_size = 10

        if event.type == pygame.MOUSEBUTTONDOWN:
            if typing:
                continue

            mx, my = event.pos

            if CLEAR_BTN.collidepoint(mx, my):
                canvas.fill(WHITE)
                continue

            if my < TOOLBAR_HEIGHT:
                index = (mx - 20)//50
                if 0 <= index < len(colors):
                    current_color = colors[index]
                continue

            if tool == "fill":
                flood_fill(canvas, mx, my - TOOLBAR_HEIGHT, current_color)
                continue

            if tool == "text":
                typing = True
                text = ""
                text_pos = (mx, my - TOOLBAR_HEIGHT)
                continue

            drawing = True
            start_pos = (mx, my - TOOLBAR_HEIGHT)
            last_pos = start_pos
            preview_pos = start_pos

        if event.type == pygame.MOUSEBUTTONUP and drawing:
            if typing:
                continue

            mx, my = event.pos
            end = (mx, my - TOOLBAR_HEIGHT)
            rect = normalize_rect(start_pos, end)

            if tool == "line":
                pygame.draw.line(canvas, current_color, start_pos, end, brush_size)

            elif tool == "rectangle":
                pygame.draw.rect(canvas, current_color, rect, brush_size)

            elif tool == "circle":
                center = ((start_pos[0]+end[0])//2,
                          (start_pos[1]+end[1])//2)
                radius = max(rect.width, rect.height)//2
                pygame.draw.circle(canvas, current_color, center, radius, brush_size)

            elif tool == "square":
                size = min(rect.width, rect.height)
                pygame.draw.rect(canvas, current_color,
                                 (rect.left, rect.top, size, size), brush_size)

            elif tool == "triangle":
                pygame.draw.polygon(canvas, current_color,
                    [start_pos, end, (start_pos[0], end[1])], brush_size)

            elif tool == "eq_triangle":
                mid = (start_pos[0] + end[0]) // 2
                pygame.draw.polygon(canvas, current_color,
                    [(mid, start_pos[1]),
                     (start_pos[0], end[1]),
                     (end[0], end[1])], brush_size)

            elif tool == "rhombus":
                midx = (start_pos[0] + end[0]) // 2
                midy = (start_pos[1] + end[1]) // 2
                pygame.draw.polygon(canvas, current_color,
                    [(midx, start_pos[1]),
                     (end[0], midy),
                     (midx, end[1]),
                     (start_pos[0], midy)], brush_size)

            drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if typing:
                continue

            mx, my = event.pos
            pos = (mx, my - TOOLBAR_HEIGHT)

            if tool == "brush":
                draw_line(canvas, current_color, last_pos, pos, brush_size)
                last_pos = pos

            else:
                preview_pos = pos

    screen.fill(WHITE)
    draw_toolbar()
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    if drawing and preview_pos:
        temp = canvas.copy()
        rect = normalize_rect(start_pos, preview_pos)

        if tool == "line":
            pygame.draw.line(temp, current_color, start_pos, preview_pos, brush_size)

        elif tool == "rectangle":
            pygame.draw.rect(temp, current_color, rect, brush_size)

        elif tool == "circle":
            center = ((start_pos[0]+preview_pos[0])//2,
                      (start_pos[1]+preview_pos[1])//2)
            radius = max(rect.width, rect.height)//2
            pygame.draw.circle(temp, current_color, center, radius, brush_size)

        screen.blit(temp, (0, TOOLBAR_HEIGHT))

    if typing:
        screen.blit(font.render(text, True, current_color),
                    (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    mx, my = pygame.mouse.get_pos()
    pygame.draw.circle(screen, BLACK, (mx,my), brush_size, 1)

    pygame.display.flip()
    clock.tick(60)