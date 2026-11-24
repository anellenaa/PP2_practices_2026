import pygame

from tools import draw_shape, draw_stroke, flood_fill, save_canvas

pygame.init()

WIDTH, HEIGHT = 1000, 700
TB = 85                                  # toolbar height
CANVAS_H = HEIGHT - TB
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, CANVAS_H))
canvas.fill((255, 255, 255))

UI_FONT = pygame.font.SysFont("arial", 15)

# ---- tools: (id, label, hotkey) ----
TOOLS = [
    ("pencil", "Pencil", pygame.K_p),
    ("line", "Line", pygame.K_l),
    ("rect", "Rect", pygame.K_r),
    ("square", "Square", pygame.K_q),
    ("circle", "Circle", pygame.K_c),
    ("rtri", "R-Tri", pygame.K_g),
    ("etri", "Eq-Tri", pygame.K_e),
    ("rhombus", "Rhombus", pygame.K_h),
    ("eraser", "Eraser", pygame.K_x),
    ("fill", "Fill", pygame.K_f),
    ("text", "Text", pygame.K_t),
    ("picker", "Picker", pygame.K_k),
]
KEY_TO_TOOL = {k: t for t, _, k in TOOLS}
SHAPES = {"line", "rect", "square", "circle", "rtri", "etri", "rhombus"}

PALETTE = [
    (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
    (255, 128, 0), (255, 255, 0), (0, 200, 0), (0, 200, 200),
    (0, 0, 255), (140, 0, 200), (255, 105, 180), (139, 69, 19),
]

SIZES = {1: 2, 2: 5, 3: 10}              # small / medium / large
TEXT_SIZES = {2: 20, 5: 32, 10: 48}      # font size per brush thickness
WHITE = (255, 255, 255)

# ---- toolbar buttons ----
btn_w = WIDTH // len(TOOLS)
tool_buttons = [(pygame.Rect(i * btn_w + 2, 4, btn_w - 4, 30), t, label)
                for i, (t, label, _) in enumerate(TOOLS)]
color_buttons = [(pygame.Rect(8 + i * 34, 46, 30, 30), c)
                 for i, c in enumerate(PALETTE)]
size_buttons = [(pygame.Rect(480 + i * 90, 46, 84, 30), lvl)
                for i, lvl in enumerate((1, 2, 3))]

# ---- state ----
tool = "pencil"
color = (0, 0, 0)
size_level = 2
drawing = False
start = last = (0, 0)

text_active = False
text_pos = (0, 0)
text_buf = ""

status = ""
status_until = 0


def brush():
    return SIZES[size_level]


def to_canvas(pos):
    return pos[0], pos[1] - TB


def commit_text():
    global text_active, text_buf
    if text_buf:
        font = pygame.font.SysFont("arial", TEXT_SIZES[brush()])
        canvas.blit(font.render(text_buf, True, color), text_pos)
    text_active, text_buf = False, ""


def cancel_text():
    global text_active, text_buf
    text_active, text_buf = False, ""


def set_tool(t):
    global tool, drawing
    if text_active:
        commit_text()
    tool, drawing = t, False


def draw_toolbar():
    pygame.draw.rect(screen, (225, 225, 225), (0, 0, WIDTH, TB))
    for rect, t, label in tool_buttons:
        bg = (160, 200, 255) if t == tool else (245, 245, 245)
        pygame.draw.rect(screen, bg, rect, border_radius=4)
        pygame.draw.rect(screen, (90, 90, 90), rect, 1, border_radius=4)
        txt = UI_FONT.render(label, True, (0, 0, 0))
        screen.blit(txt, txt.get_rect(center=rect.center))
    for rect, c in color_buttons:
        pygame.draw.rect(screen, c, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 3 if c == color else 1)
    for rect, lvl in size_buttons:
        bg = (160, 200, 255) if lvl == size_level else (245, 245, 245)
        pygame.draw.rect(screen, bg, rect, border_radius=4)
        pygame.draw.rect(screen, (90, 90, 90), rect, 1, border_radius=4)
        txt = UI_FONT.render(f"{lvl}: {SIZES[lvl]}px", True, (0, 0, 0))
        screen.blit(txt, txt.get_rect(center=rect.center))
    # current color swatch
    pygame.draw.rect(screen, color, (WIDTH - 60, 46, 50, 30))
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH - 60, 46, 50, 30), 1)
    if status and pygame.time.get_ticks() < status_until:
        s = UI_FONT.render(status, True, (0, 120, 0))
        screen.blit(s, (760, 54))


def handle_toolbar_click(pos):
    global color, size_level
    for rect, t, _ in tool_buttons:
        if rect.collidepoint(pos):
            set_tool(t)
            return
    for rect, c in color_buttons:
        if rect.collidepoint(pos):
            color = c
            return
    for rect, lvl in size_buttons:
        if rect.collidepoint(pos):
            size_level = lvl
            return


running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        elif e.type == pygame.KEYDOWN:
            ctrl = e.mod & pygame.KMOD_CTRL
            if ctrl and e.key == pygame.K_s:
                if text_active:
                    commit_text()
                name = save_canvas(canvas)
                status, status_until = f"Saved: {name}", pygame.time.get_ticks() + 3000
            elif text_active:
                if e.key == pygame.K_RETURN:
                    commit_text()
                elif e.key == pygame.K_ESCAPE:
                    cancel_text()
                elif e.key == pygame.K_BACKSPACE:
                    text_buf = text_buf[:-1]
                elif e.unicode and e.unicode.isprintable():
                    text_buf += e.unicode
            else:
                if e.key in (pygame.K_1, pygame.K_KP1):
                    size_level = 1
                elif e.key in (pygame.K_2, pygame.K_KP2):
                    size_level = 2
                elif e.key in (pygame.K_3, pygame.K_KP3):
                    size_level = 3
                elif e.key in KEY_TO_TOOL:
                    set_tool(KEY_TO_TOOL[e.key])

        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if e.pos[1] < TB:
                handle_toolbar_click(e.pos)
                continue
            cp = to_canvas(e.pos)
            if tool in ("pencil", "eraser"):
                drawing, last = True, cp
                c = WHITE if tool == "eraser" else color
                s = brush() * 3 if tool == "eraser" else brush()
                pygame.draw.circle(canvas, c, cp, max(1, s // 2))
            elif tool in SHAPES:
                drawing, start = True, cp
            elif tool == "fill":
                flood_fill(canvas, cp, color)
            elif tool == "picker":
                color = tuple(canvas.get_at(cp))[:3]
            elif tool == "text":
                text_pos, text_active = cp, True   # click places/moves the text cursor

        elif e.type == pygame.MOUSEMOTION and drawing:
            cp = to_canvas(e.pos)
            if tool == "pencil":
                draw_stroke(canvas, color, last, cp, brush())
                last = cp
            elif tool == "eraser":
                draw_stroke(canvas, WHITE, last, cp, brush() * 3)
                last = cp

        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and drawing:
            if tool in SHAPES:
                draw_shape(canvas, tool, color, start, to_canvas(e.pos), brush())
            drawing = False

    # ---- rendering ----
    view = canvas.copy()
    if drawing and tool in SHAPES:       # live preview
        mx, my = pygame.mouse.get_pos()
        draw_shape(view, tool, color, start, to_canvas((mx, my)), brush())
    if text_active:
        font = pygame.font.SysFont("arial", TEXT_SIZES[brush()])
        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
        view.blit(font.render(text_buf + cursor, True, color), text_pos)

    screen.fill((255, 255, 255))
    screen.blit(view, (0, TB))
    draw_toolbar()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()