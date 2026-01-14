import pyxel
import random

BLOCK = 8
COLS = 10
ROWS = 18
WIDTH = COLS * BLOCK
HEIGHT = ROWS * BLOCK

pyxel.init(WIDTH, HEIGHT, title="テトリス風")

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1],
     [1, 1]],
    [[1, 0],
     [1, 0],
     [1, 1]],
    [[1, 1, 0],
     [0, 1, 1]]
]

COLORS = [8, 9, 10, 11, 12]

field = [[0 for _ in range(COLS)] for _ in range(ROWS)]

shape = None
color = 0
bx = 0
by = 0
drop_timer = 0
score = 0
game_over = False

def new_block():
    global shape, color, bx, by, game_over
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    bx = COLS // 2 - len(shape[0]) // 2
    by = 0

    if not can_move(bx, by, shape):
        game_over = True

def can_move(nx, ny, s):
    for y in range(len(s)):
        for x in range(len(s[0])):
            if s[y][x]:
                fx = nx + x
                fy = ny + y
                if fx < 0 or fx >= COLS or fy >= ROWS:
                    return False
                if fy >= 0 and field[fy][fx]:
                    return False
    return True

def rotate(s):
    return list(zip(*s[::-1]))

def fix_block():
    for y in range(len(shape)):
        for x in range(len(shape[0])):
            if shape[y][x]:
                field[by + y][bx + x] = color
    clear_lines()
    new_block()

def clear_lines():
    global field, score
    new_field = []
    cleared = 0
    for row in field:
        if 0 not in row:
            cleared += 1
        else:
            new_field.append(row)
    while len(new_field) < ROWS:
        new_field.insert(0, [0] * COLS)
    field = new_field
    score += cleared

def update():
    global bx, by, drop_timer, shape
    if game_over:
        return

    if pyxel.btnp(pyxel.KEY_LEFT) and can_move(bx - 1, by, shape):
        bx -= 1
    if pyxel.btnp(pyxel.KEY_RIGHT) and can_move(bx + 1, by, shape):
        bx += 1

    if pyxel.btnp(pyxel.KEY_UP):
        r = rotate(shape)
        if can_move(bx, by, r):
            shape = r

    drop_timer += 1
    speed = 15
    if pyxel.btn(pyxel.KEY_DOWN):
        speed = 3

    if drop_timer >= speed:
        if can_move(bx, by + 1, shape):
            by += 1
        else:
            fix_block()
        drop_timer = 0

def draw():
    pyxel.cls(0)

    for y in range(ROWS):
        for x in range(COLS):
            if field[y][x]:
                pyxel.rect(
                    x * BLOCK,
                    y * BLOCK,
                    BLOCK,
                    BLOCK,
                    field[y][x]
                )


    if not game_over:
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x]:
                    pyxel.rect(
                        (bx + x) * BLOCK,
                        (by + y) * BLOCK,
                        BLOCK,
                        BLOCK,
                        color
                    )

    pyxel.text(2, 2, f"SCORE: {score}", 7)

    if game_over:
        pyxel.text(WIDTH // 2 - 28, HEIGHT // 2 - 4, "GAME OVER", 8)

new_block()
pyxel.run(update, draw)
