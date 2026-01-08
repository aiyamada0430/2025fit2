import pyxel

pyxel.init(200, 200)
pyxel.sound(0).set(notes='A2C3', tones='TT', volumes='33', effects='NN', speed=10)
pyxel.sound(1).set(notes='C2', tones='N', volumes='3', effects='S', speed=30)

balls = []
for i in range(3):
    angle = pyxel.rndi(30, 150)
    balls.append({
        "x": pyxel.rndi(0, 199),
        "y": 0,
        "vx": pyxel.cos(angle),
        "vy": pyxel.sin(angle),
        "speed": 1
    })

padx = 100
score = 0

def reset_ball(ball):
    angle = pyxel.rndi(30, 150)
    ball["x"] = pyxel.rndi(0, 199)
    ball["y"] = 0
    ball["vx"] = pyxel.cos(angle)
    ball["vy"] = pyxel.sin(angle)
    ball["speed"] += 1

def update():
    global padx, score
    padx = pyxel.mouse_x

    for ball in balls:
        ball["x"] += ball["vx"] * ball["speed"]
        ball["y"] += ball["vy"] * ball["speed"]

 
        if (ball["x"] < 0) or (ball["x"] >= 200):
            ball["vx"] = -ball["vx"]

     
        if ball["y"] >= 200:
            pyxel.play(0, 1)
            reset_ball(ball)

        if ball["y"] >= 195 and (padx - 20 <= ball["x"] <= padx + 20):
            pyxel.play(0, 0)
            score += 1
            reset_ball(ball)

def draw():
    pyxel.cls(7)
    for ball in balls:
        pyxel.circ(ball["x"], ball["y"], 10, 6)
    pyxel.rect(padx - 20, 195, 40, 5, 14)
    pyxel.text(5, 5, "score: " + str(score), 0)

pyxel.run(update, draw)
