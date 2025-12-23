import turtle
import time
import random

delay = 0.1

score = 1
high_score = 0

def draw_gradient_bg(screen, width, height):
    colors = ["#000000", "#000000", "#000000"]
    turtle.colormode(255)
    turtle.speed(0)
    turtle.hideturtle()
    turtle.penup()
    step = height // len(colors)
    for i, color in enumerate(colors):
        turtle.goto(-width//2, height//2 - i * step)
        turtle.color(color)
        turtle.begin_fill()
        for _ in range(2):
            turtle.forward(width)
            turtle.right(90)
            turtle.forward(step)
            turtle.right(90)
        turtle.end_fill()
    turtle.update()

screen = turtle.Screen()
screen.title("Snake Game by @Dhruv Deshmukh")
screen.setup(width=600, height=600)
screen.tracer(0)

# Load apple image (Option 1: recommended)
try:
    screen.register_shape("apple.gif")
    use_apple_img = True
except:
    use_apple_img = False

draw_gradient_bg(screen, 600, 600)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#38ef7d")  # Vibrant green head
head.pensize(3)
head.pencolor("#26734d")  # Darker border for head
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Eyes for the snake head
left_eye = turtle.Turtle()
right_eye = turtle.Turtle()
for eye in (left_eye, right_eye):
    eye.speed(0)
    eye.shape("circle")
    eye.color("black")
    eye.shapesize(stretch_wid=0.2, stretch_len=0.2)
    eye.penup()

def update_eyes():
    x = head.xcor()
    y = head.ycor()
    if head.direction in ["up", "stop"]:
        left_eye.goto(x - 6, y + 8)
        right_eye.goto(x + 6, y + 8)
    elif head.direction == "down":
        left_eye.goto(x - 6, y - 8)
        right_eye.goto(x + 6, y - 8)
    elif head.direction == "left":
        left_eye.goto(x - 8, y + 6)
        right_eye.goto(x - 8, y - 6)
    elif head.direction == "right":
        left_eye.goto(x + 8, y + 6)
        right_eye.goto(x + 8, y - 6)

# Tongue for the snake head
tongue = turtle.Turtle()
tongue.speed(0)
tongue.shape("triangle")  # Tongue shape
tongue.color("red")
tongue.shapesize(stretch_wid=0.1, stretch_len=0.5)
tongue.penup()
tongue.hideturtle()

tongue_out = True  # toggle for tongue flick

def update_tongue():
    global tongue_out
    x = head.xcor()
    y = head.ycor()
    offset = 12 if tongue_out else 8  # flick effect by changing offset
    if head.direction == "up":
        tongue.goto(x, y + offset)
        tongue.setheading(90)
    elif head.direction == "down":
        tongue.goto(x, y - offset)
        tongue.setheading(270)
    elif head.direction == "left":
        tongue.goto(x - offset, y)
        tongue.setheading(180)
    elif head.direction == "right":
        tongue.goto(x + offset, y)
        tongue.setheading(0)
    else:
        tongue.hideturtle()
        return
    tongue.showturtle()
    tongue_out = not tongue_out

# Food (three apples)
food = turtle.Turtle()
food.speed(0)
if use_apple_img:
    food.shape("apple.gif")
else:
    food.shape("circle")
    food.color("red")
food.penup()
food.goto(0, 100)

food2 = turtle.Turtle()
food2.speed(0)
if use_apple_img:
    food2.shape("apple.gif")
else:
    food2.shape("circle")
    food2.color("red")
food2.penup()
food2.goto(0, 150)

food3 = turtle.Turtle()
food3.speed(0)
if use_apple_img:
    food3.shape("apple.gif")
else:
    food3.shape("circle")
    food3.color("red")
food3.penup()
food3.goto(0, 200)

segments = []

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

zigzag_toggle = True

def move():
    global zigzag_toggle
    offset = 5 if zigzag_toggle else -5
    zigzag_toggle = not zigzag_toggle

    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
        head.setx(head.xcor() + offset)
    elif head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
        head.setx(head.xcor() + offset)
    elif head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
        head.sety(head.ycor() + offset)
    elif head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)
        head.sety(head.ycor() + offset)

    update_eyes()
    update_tongue()

screen.listen()
screen.onkeypress(go_up, "w")
screen.onkeypress(go_down, "s")
screen.onkeypress(go_left, "a")
screen.onkeypress(go_right, "d")

while True:
    screen.update()

    # Border collision
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"
        left_eye.goto(1000, 1000)
        right_eye.goto(1000, 1000)
        tongue.hideturtle()
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        score = 0
        delay = 0.1
        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    # Food collision for food1
    if head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#43cea2" if len(segments) % 2 == 0 else "#185a9d")
        new_segment.pensize(2)
        new_segment.pencolor("#123456")
        new_segment.penup()
        segments.append(new_segment)

        delay = max(0.05, delay - 0.001)
        score += 10
        if score > high_score:
            high_score = score
        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    # Food collision for food2
    if head.distance(food2) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food2.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#43cea2" if len(segments) % 2 == 0 else "#185a9d")
        new_segment.pensize(2)
        new_segment.pencolor("#123456")
        new_segment.penup()
        segments.append(new_segment)

        delay = max(0.05, delay - 0.001)
        score += 10
        if score > high_score:
            high_score = score
        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    # Food collision for food3
    if head.distance(food3) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food3.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#43cea2" if len(segments) % 2 == 0 else "#185a9d")
        new_segment.pensize(2)
        new_segment.pencolor("#123456")
        new_segment.penup()
        segments.append(new_segment)

        delay = max(0.05, delay - 0.001)
        score += 10
        if score > high_score:
            high_score = score
        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    # Move end segments
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Self collision
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"
            left_eye.goto(1000, 1000)
            right_eye.goto(1000, 1000)
            tongue.hideturtle()
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0
            delay = 0.1
            pen.clear()
            pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)
