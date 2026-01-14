import pyxel
import random

# ===== 定数 =====
BLOCK = 8
COLS = 10
ROWS = 18
WIDTH = COLS * BLOCK
HEIGHT = ROWS * BLOCK

pyxel.init(WIDTH, HEIGHT, title="テトリス風")

# ===== テトリミノ定義 =====
SHAPES = [
    [[1, 1, 1, 1]],            # I
    [[1, 1],
     [1, 1]],                  # O
    [[1, 0],
     [1, 0],
     [1, 1]],                  # L
    [[1, 1, 0],
     [0, 1, 1]]                # Z
]

COLORS = [8, 9, 10, 11, 12]

# ===== 盤面 =====
field = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# ===== 落下ブロック =====
shape = None
color = 0
bx = 0
by = 0
drop_timer = 0

def new_block():
    global shape, color, bx, by
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    bx = COLS // 2 - len(shape[0]) // 2
    by = 0

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
    global field
    new_field = []
    for row in field:
        if 0 not in row:
            continue
        new_field.append(row)
    while len(new_field) < ROWS:
        new_field.insert(0, [0] * COLS)
    field = new_field

def update():
    global bx, by, drop_timer, shape

    # 左右移動
    if pyxel.btnp(pyxel.KEY_LEFT):
        if can_move(bx - 1, by, shape):
            bx -= 1
    if pyxel.btnp(pyxel.KEY_RIGHT):
        if can_move(bx + 1, by, shape):
            bx += 1

    # 回転
    if pyxel.btnp(pyxel.KEY_UP):
        r = rotate(shape)
        if can_move(bx, by, r):
            shape = r

    # 落下
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

    # 盤面
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

    # 落下中ブロック
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

new_block()
pyxel.run(update, draw)
