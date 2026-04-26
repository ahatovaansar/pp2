import pygame

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


def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    width, height = surface.get_size()
    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if surface.get_at((px, py)) == target_color:
            surface.set_at((px, py), new_color)

            if px > 0:
                stack.append((px-1, py))
            if px < width-1:
                stack.append((px+1, py))
            if py > 0:
                stack.append((px, py-1))
            if py < height-1:
                stack.append((px, py+1))