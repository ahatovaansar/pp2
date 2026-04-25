import pygame
import sys

pygame.init()
pygame.mouse.set_visible(False)

WIDTH, HEIGHT = 900, 600
TOOLBAR_HEIGHT = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

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

history = []  # 🔥 undo

current_color = BLACK
brush_size = 8
tool = "brush"

drawing = False
start_pos = None
last_pos = None
preview_pos = None

def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0,0,WIDTH,TOOLBAR_HEIGHT))

    text = font.render(
        "B-Brush R-Rect O-Circle E-Eraser S-Square T-Triangle Q-EqTri H-Rhombus  | Ctrl+Z Undo | C Clear",
        True, BLACK)
    screen.blit(text, (10,50))

    for i, color in enumerate(colors):
        rect = pygame.Rect(20+i*50, 10, 35, 35)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

def draw_line(surface, color, start, end, radius):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    steps = max(abs(dx), abs(dy))

    for i in range(steps+1):
        x = int(start[0] + dx*i/steps)
        y = int(start[1] + dy*i/steps)
        pygame.draw.circle(surface, color, (x,y), radius)

def normalize_rect(a, b):
    return pygame.Rect(min(a[0], b[0]), min(a[1], b[1]),
                       abs(a[0]-b[0]), abs(a[1]-b[1]))

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 🎮 keyboard
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_b: tool="brush"
            elif event.key == pygame.K_r: tool="rectangle"
            elif event.key == pygame.K_o: tool="circle"
            elif event.key == pygame.K_e: tool="eraser"
            elif event.key == pygame.K_s: tool="square"
            elif event.key == pygame.K_t: tool="triangle"
            elif event.key == pygame.K_q: tool="eq_triangle"
            elif event.key == pygame.K_h: tool="rhombus"

            # 🔥 undo
            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if history:
                    canvas = history.pop()

            # 🧹 clear
            elif event.key == pygame.K_c:
                history.append(canvas.copy())
                canvas.fill(WHITE)

        # 🖱 DOWN
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if my < TOOLBAR_HEIGHT:
                index = (mx - 20)//50
                if 0 <= index < len(colors):
                    current_color = colors[index]
                continue

            history.append(canvas.copy())  # save state

            drawing = True
            start_pos = (mx, my - TOOLBAR_HEIGHT)
            last_pos = start_pos
            preview_pos = start_pos

        # 🖱 UP
        if event.type == pygame.MOUSEBUTTONUP and drawing:
            mx, my = event.pos
            end = (mx, my - TOOLBAR_HEIGHT)
            rect = normalize_rect(start_pos, end)

            if tool == "square":
                size = min(rect.width, rect.height)
                pygame.draw.rect(canvas, current_color,
                                 (rect.left, rect.top, size, size), 2)

            elif tool == "triangle":
                pygame.draw.polygon(canvas, current_color,
                    [start_pos, end, (start_pos[0], end[1])], 2)

            elif tool == "eq_triangle":
                mid = (start_pos[0] + end[0]) // 2
                pygame.draw.polygon(canvas, current_color,
                    [(mid, start_pos[1]),
                     (start_pos[0], end[1]),
                     (end[0], end[1])], 2)

            elif tool == "rhombus":
                midx = (start_pos[0] + end[0]) // 2
                midy = (start_pos[1] + end[1]) // 2
                pygame.draw.polygon(canvas, current_color,
                    [(midx, start_pos[1]),
                     (end[0], midy),
                     (midx, end[1]),
                     (start_pos[0], midy)], 2)

            elif tool == "rectangle":
                pygame.draw.rect(canvas, current_color, rect, 2)

            elif tool == "circle":
                center = ((start_pos[0]+end[0])//2,
                          (start_pos[1]+end[1])//2)
                radius = max(rect.width, rect.height)//2
                pygame.draw.circle(canvas, current_color, center, radius, 2)

            drawing = False

        # 🖱 MOVE
        if event.type == pygame.MOUSEMOTION and drawing:
            mx, my = event.pos
            pos = (mx, my - TOOLBAR_HEIGHT)

            if tool == "brush":
                draw_line(canvas, current_color, last_pos, pos, brush_size)
                last_pos = pos
            elif tool == "eraser":
                draw_line(canvas, WHITE, last_pos, pos, brush_size)
                last_pos = pos
            else:
                preview_pos = pos

    # 🎨 draw
    screen.fill(WHITE)
    draw_toolbar()
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    # 👁 preview
    if drawing and preview_pos:
        temp = canvas.copy()
        rect = normalize_rect(start_pos, preview_pos)

        if tool == "square":
            size = min(rect.width, rect.height)
            pygame.draw.rect(temp, current_color,
                             (rect.left, rect.top, size, size), 2)

        elif tool == "triangle":
            pygame.draw.polygon(temp, current_color,
                [start_pos, preview_pos, (start_pos[0], preview_pos[1])], 2)

        elif tool == "eq_triangle":
            mid = (start_pos[0] + preview_pos[0]) // 2
            pygame.draw.polygon(temp, current_color,
                [(mid, start_pos[1]),
                 (start_pos[0], preview_pos[1]),
                 (preview_pos[0], preview_pos[1])], 2)

        elif tool == "rhombus":
            midx = (start_pos[0] + preview_pos[0]) // 2
            midy = (start_pos[1] + preview_pos[1]) // 2
            pygame.draw.polygon(temp, current_color,
                [(midx, start_pos[1]),
                 (preview_pos[0], midy),
                 (midx, preview_pos[1]),
                 (start_pos[0], midy)], 2)

        elif tool == "rectangle":
            pygame.draw.rect(temp, current_color, rect, 2)

        elif tool == "circle":
            center = ((start_pos[0]+preview_pos[0])//2,
                      (start_pos[1]+preview_pos[1])//2)
            radius = max(rect.width, rect.height)//2
            pygame.draw.circle(temp, current_color, center, radius, 2)

        screen.blit(temp, (0, TOOLBAR_HEIGHT))

    # 🎯 cursor
    mx, my = pygame.mouse.get_pos()
    pygame.draw.circle(screen, BLACK, (mx,my), brush_size, 1)

    pygame.display.flip()
    clock.tick(60)