import turtle
import math
import random
import time

# Screen setup
wn = turtle.Screen()
wn.title("Space Shooter | kanak Dovloper")
wn.bgcolor("black")
wn.setup(width=1024, height=768)
wn.tracer(0)

# Register shapes
turtle.register_shape("triangle", ((-10, 0), (0, 20), (10, 0)))

# Border
border = turtle.Turtle()
border.speed(0)
border.color("cyan")
border.pensize(3)
border.penup()
border.hideturtle()
border.goto(-500, 370)
border.pendown()
for side in range(4):
    border.forward(1000)
    border.right(90)
border.penup()

# Player
player = turtle.Turtle()
player.color("cyan")
player.shape("triangle")
player.penup()
player.speed(0)
player.setheading(90)
player.goto(0, -330)

# Player speed
playerspeed = 15

# Score
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("yellow")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(-490, 340)
score_pen.write(f"Score: {score} | kanak Dovloper", align="left", font=("Arial", 16, "bold"))

# Lives
lives = 3
lives_pen = turtle.Turtle()
lives_pen.speed(0)
lives_pen.color("white")
lives_pen.penup()
lives_pen.hideturtle()
lives_pen.goto(490, 340)
lives_pen.write(f"Lives: {lives}", align="right", font=("Arial", 16, "bold"))

# Bullets
bullets = []

# Enemies
enemies = []
for i in range(6):
    enemy = turtle.Turtle()
    enemy.color("red")
    enemy.shape("triangle")
    enemy.penup()
    enemy.speed(0)
    enemy.setheading(-90)
    x = random.randint(-450, 450)
    y = random.randint(100, 320)
    enemy.goto(x, y)
    enemies.append(enemy)

enemyspeed = 2

# Move functions
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -480:
        x = -480
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 480:
        x = 480
    player.setx(x)

def move_up():
    y = player.ycor()
    y += playerspeed
    if y > 320:
        y = 320
    player.sety(y)

def move_down():
    y = player.ycor()
    y -= playerspeed
    if y < -330:
        y = -330
    player.sety(y)

def fire_bullet():
    global bulletstate
    if len(bullets) < 3:
        bullet = turtle.Turtle()
        bullet.color("yellow")
        bullet.shape("triangle")
        bullet.penup()
        bullet.speed(0)
        bullet.setheading(90)
        bullet.shapesize(stretch_wid=0.2, stretch_len=0.8)
        x = player.xcor()
        y = player.ycor() + 10
        bullet.goto(x, y)
        bullets.append(bullet)

# Keyboard bindings
wn.listen()
wn.onkey(move_left, "Left")
wn.onkey(move_right, "Right")
wn.onkey(move_up, "Up")
wn.onkey(move_down, "Down")
wn.onkey(fire_bullet, "space")

# Game loop
while True:
    wn.update()
    
    for enemy in enemies:
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)
        
        if enemy.xcor() > 480:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1
        
        if enemy.xcor() < -480:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1
        
        # Collision between enemy and player
        if enemy.distance(player) < 30:
            player.goto(0, -330)
            score_pen.clear()
            lives -= 1
            lives_pen.clear()
            score_pen.write(f"Score: {score} | kanak Dovloper", align="left", font=("Arial", 16, "bold"))
            lives_pen.write(f"Lives: {lives}", align="right", font=("Arial", 16, "bold"))
            if lives <= 0:
                score_pen.goto(0, 0)
                score_pen.write("GAME OVER", align="center", font=("Arial", 48, "bold"))
                lives_pen.clear()
                time.sleep(3)
                break
    
    # Move bullets
    for bullet in bullets:
        y = bullet.ycor()
        y += 20
        bullet.sety(y)
        
        if bullet.ycor() > 370:
            bullet.hideturtle()
            bullets.remove(bullet)
            continue
        
        for enemy in enemies:
            if bullet.distance(enemy) < 25:
                bullet.hideturtle()
                bullets.remove(bullet)
                enemy.goto(random.randint(-450, 450), random.randint(100, 320))
                score += 10
                score_pen.clear()
                score_pen.write(f"Score: {score} | kanak Dovloper", align="left", font=("Arial", 16, "bold"))
                break
    
    if lives <= 0:
        break

wn.mainloop()
