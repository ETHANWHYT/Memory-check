import turtle
import random
import time

# basic screen setup
sc = turtle.Screen()
sc.title("Memory Game")
sc.setup(width=700, height=800)
sc.bgcolor("white")

# taking input from user

player = sc.textinput("Name", "Enter your name:")
grsize = sc.textinput(
    "Grid Size",
    "Enter grid size:\n3 for 3x3\n4 for 4x4\n5 for 5x5"
)

if grsize not in ["3", "4", "5"]:
    grsize = "5"

grid = int(grsize)
totlbox = grid * grid
box_size = 400 // grid
memory_time = totlbox * 2

# game variables

nums = list(range(1, totlbox + 1))
random.shuffle(nums)

traps = random.sample(nums[3:], 2)
bonus = random.sample([n for n in nums if n not in traps], 2)

current = 1
points = 100
mistakes = 0
clicks = 0
end = False
start_time = None

positions = {}

# turtle objects

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

info = turtle.Turtle()
info.hideturtle()
info.penup()
info.goto(0, -350)


# start screen

def start():
    sc.clear()
    sc.bgcolor("lightyellow")

    t = turtle.Turtle()
    t.hideturtle()
    t.penup()

    t.goto(0, 260)
    t.write("MEMORY NUMBER GAME",
            align="center", font=("Arial", 22, "bold"))

    rules_text = [
        f"Player: {player}",
        f"Grid: {grid}x{grid}",
        "",
        "Rules:",
        "1. Numbers kuch seconds ke liye dikhai denge.",
        f"   Time = Grid² × 2 = {memory_time} seconds.",
        "2. Numbers gayab hone ke baad 1 se last tak click karo.",
        "3. Sahi click = green",
        "4. Galat click = -5 points",
        "5. Trap = -15 points",
        "6. Bonus = +10 points",
        "7. Jab tak sabhi sahi ni lelete, tab tak game chalta rahega.",
        "",
        "Press SPACE to start",
        "Press Q to quit"
    ]

    y = 220
    for line in rules_text:
        t.goto(0, y)
        t.write(line, align="center",
                font=("Arial", 14, "normal"))
        y -= 28

    sc.listen()
    sc.onkey(start_game, "space")
    sc.onkey(quit_game, "q")

# drawing grid

def draw(show_numbers=True):
    t.clear()
    t.penup()

    st_x = -(grid * box_size) / 2
    st_y = (grid * box_size) / 2
    i = 0

    for r in range(grid):
        for c in range(grid):
            x = st_x + c * box_size
            y = st_y - r * box_size

            t.goto(x, y)
            t.pendown()
            for _ in range(4):
                t.forward(box_size)
                t.right(90)
            t.penup()

            if show_numbers:
                t.goto(x + box_size/3, y - box_size/1.5)
                t.write(nums[i],
                          font=("Arial", int(150/grid), "bold"))

            positions[nums[i]] = (x, y)
            i += 1


# memory countdown

time_left = memory_time

def countdown():
    global time_left

    if time_left > 0:
        info.clear()
        info.write(f"Memorize! Time Left: {time_left}s",
                   align="center",
                   font=("Arial", 14, "bold"))
        time_left -= 1
        sc.ontimer(countdown, 1000)
    else:
        hide_numbers()


# hide numbers and start game

def hide_numbers():
    global start_time
    draw(False)
    start_time = time.time()
    update_info()
    sc.onclick(click_game)

# update bottom info

def update_info():
    if start_time:
        elapsed = int(time.time() - start_time)
    else:
        elapsed = 0

    info.clear()
    info.write(
        f"Player: {player} | Next: {current} | "
        f"Score: {points} | Wrong: {mistakes} | Time: {elapsed}s",
        align="center",
        font=("Arial", 11, "bold")
    )

# detect clicked number

def get_num(x, y):
    for n, (cx, cy) in positions.items():
        if cx <= x <= cx + box_size and cy - box_size <= y <= cy:
            return n
    return None


# mark clicked box

def mark(n, color):
    x, y = positions[n]
    m = turtle.Turtle()
    m.hideturtle()
    m.penup()
    m.goto(x + box_size/2, y - box_size/2)
    m.dot(box_size/3, color)

# result screen
 
def show_end(text="GAME OVER"):
    global end
    end = True

    total_time = 0
    if start_time:
        total_time = int(time.time() - start_time)

    sc.clear()
    sc.bgcolor("black")

    r = turtle.Turtle()
    r.hideturtle()
    r.color("white")
    r.penup()

    result = [
        f"{text}, {player}",
        f"Grid: {grid}x{grid}",
        f"Score: {points}",
        f"Time: {total_time}s",
        f"Wrong: {mistakes}",
        f"Total Clicks: {clicks}"
    ]

    y = 200
    for line in result:
        r.goto(0, y)
        r.write(line, align="center",
                font=("Arial", 16, "bold"))
        y -= 60
        time.sleep(0.8)

 
# quit function
 
def quit_game():
    show_end("GAME QUIT")

 
# main click logic
 
def click_game(x, y):
    global current, points, mistakes, clicks

    if end:
        return

    num = get_num(x, y)
    if num is None:
        return

    clicks += 1

    if num == current:
        mark(num, "green")
        current += 1

        if random.randint(1, 5) == 3:
            points += 10

        if current > totlbox:
            show_end("GAME FINISHED")

    elif num in traps:
        points -= 15
        mistakes += 1
        mark(num, "purple")

    elif num in bonus:
        points += 10
        mark(num, "blue")

    else:
        points -= 5
        mistakes += 1
        mark(num, "red")

    update_info()

# start game

def start_game():
    sc.clear()
    sc.bgcolor("white")
    draw(True)
    countdown()

start()
turtle.done()