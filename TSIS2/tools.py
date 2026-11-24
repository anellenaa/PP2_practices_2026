import math
from datetime import datetime

import pygame


def _sign(v):
    return -1 if v < 0 else 1


def draw_shape(surf, tool, color, a, b, size):
    """Draw a shape from two points (a = start, b = current/end)."""
    x1, y1 = a
    x2, y2 = b
    dx, dy = x2 - x1, y2 - y1

    if tool == "line":
        pygame.draw.line(surf, color, a, b, size)
        # round the ends so thick lines look clean
        if size > 2:
            pygame.draw.circle(surf, color, a, size // 2)
            pygame.draw.circle(surf, color, b, size // 2)

    elif tool == "rect":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(dx), abs(dy))
        pygame.draw.rect(surf, color, rect, size)

    elif tool == "square":
        side = min(abs(dx), abs(dy))
        sx = x1 if dx >= 0 else x1 - side
        sy = y1 if dy >= 0 else y1 - side
        pygame.draw.rect(surf, color, (sx, sy, side, side), size)

    elif tool == "circle":
        r = int(math.hypot(dx, dy))
        if r > 0:
            pygame.draw.circle(surf, color, a, r, min(size, r))

    elif tool == "rtri":  # right triangle
        pts = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surf, color, pts, size)

    elif tool == "etri":  # equilateral triangle
        base = abs(dx)
        h = base * math.sqrt(3) / 2
        apex_y = y1 + _sign(dy) * h
        pts = [(x1, y1), (x2, y1), ((x1 + x2) / 2, apex_y)]
        pygame.draw.polygon(surf, color, pts, size)

    elif tool == "rhombus":
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        pts = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
        pygame.draw.polygon(surf, color, pts, size)


def draw_stroke(surf, color, p_from, p_to, size):
    """Continuous pencil/eraser stroke between two mouse positions."""
    pygame.draw.line(surf, color, p_from, p_to, size)
    if size > 2:
        pygame.draw.circle(surf, color, p_to, size // 2)


def flood_fill(surf, pos, new_color):
    """Flood fill (scanline algorithm) using get_at / set_at.
    Stops at any boundary of a different color (exact color match)."""
    w, h = surf.get_size()
    x, y = pos
    if not (0 <= x < w and 0 <= y < h):
        return
    target = surf.get_at((x, y))[:3]
    new = tuple(new_color[:3])
    if target == new:
        return

    stack = [(x, y)]
    while stack:
        x, y = stack.pop()
        if surf.get_at((x, y))[:3] != target:
            continue
        lx = x
        while lx > 0 and surf.get_at((lx - 1, y))[:3] == target:
            lx -= 1
        rx = x
        while rx < w - 1 and surf.get_at((rx + 1, y))[:3] == target:
            rx += 1
        for i in range(lx, rx + 1):
            surf.set_at((i, y), new)
        for ny in (y - 1, y + 1):
            if 0 <= ny < h:
                in_span = False
                for i in range(lx, rx + 1):
                    if surf.get_at((i, ny))[:3] == target:
                        if not in_span:
                            stack.append((i, ny))
                            in_span = True
                    else:
                        in_span = False


def save_canvas(surf):
    """Save the canvas as a timestamped PNG. Returns the file name."""
    name = datetime.now().strftime("canvas_%Y%m%d_%H%M%S.png")
    pygame.image.save(surf, name)
    return name