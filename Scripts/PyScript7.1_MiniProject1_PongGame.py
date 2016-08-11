# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = 0.0
paddle2_pos = 0.0
paddle1_vel , paddle2_vel = 0, 0
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0,0]
player1_score, player2_score = 0, 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction1, direction2):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel[0] = random.randrange(2,3)
    ball_vel[1] = random.randrange(2,3)
    if(direction1 == "LEFT"):
        ball_vel[0] = -ball_vel[0]
    if(direction2 == "TOP"):
        ball_vel[1] = -ball_vel[1]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global player1_score, player2_score  # these are ints
    player1_score, player2_score = 0, 0
    spawn_ball(random.choice(["LEFT","RIGHT"]), random.choice(["BOTTOM","TOP"]))

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, player1_score, player2_score

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    if((ball_pos[0] <= BALL_RADIUS) or (ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH)):
        ball_vel[0] = - ball_vel[0]

    if((ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] +  BALL_RADIUS >= HEIGHT)):
        ball_vel[1] = - ball_vel[1]


    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")


    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel) >= -(HEIGHT/2.0 - HALF_PAD_HEIGHT) and (paddle1_pos + paddle1_vel) <= (HEIGHT/2.0 - HALF_PAD_HEIGHT):
        paddle1_pos += paddle1_vel
    if (paddle2_pos + paddle2_vel) >= -(HEIGHT/2.0 - HALF_PAD_HEIGHT) and (paddle2_pos + paddle2_vel) <= (HEIGHT/2.0 - HALF_PAD_HEIGHT):
        paddle2_pos += paddle2_vel


    canvas.draw_polygon([(0, HEIGHT/2.0 - HALF_PAD_HEIGHT + paddle1_pos),
                    (PAD_WIDTH, HEIGHT/2.0 - HALF_PAD_HEIGHT + paddle1_pos),
                    (PAD_WIDTH, HEIGHT/2.0 + HALF_PAD_HEIGHT + paddle1_pos),
                    (0, HEIGHT/2.0 + HALF_PAD_HEIGHT + paddle1_pos)], 3, 'Red',
                    'White')

    canvas.draw_polygon([(WIDTH - PAD_WIDTH, HEIGHT/2.0 - HALF_PAD_HEIGHT + paddle2_pos),
                    (WIDTH, HEIGHT/2.0 - HALF_PAD_HEIGHT + paddle2_pos),
                    (WIDTH, HEIGHT/2.0 + HALF_PAD_HEIGHT + paddle2_pos),
                    (WIDTH - PAD_WIDTH, HEIGHT/2.0 + HALF_PAD_HEIGHT + paddle2_pos)],
                    3, 'Blue', 'White')


    # determine whether paddle and ball collide
    # right side collision
    if(ball_pos[0] + BALL_RADIUS >= (WIDTH - PAD_WIDTH - 1)):
        if((ball_pos[1] >= (paddle2_pos - HALF_PAD_HEIGHT + (HEIGHT/2))) and (ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT + (HEIGHT/2)))):
            ball_vel[0] *= 1.05
        else:
            player1_score += 1
            spawn_ball("LEFT", random.choice(["BOTTOM","TOP"]))

    # left side collision
    if(ball_pos[0] - BALL_RADIUS <= PAD_WIDTH + 1):
        if((ball_pos[1] >= (paddle1_pos - HALF_PAD_HEIGHT + (HEIGHT/2))) and (ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT + (HEIGHT/2)))):
            ball_vel[0] *= 1.05
        else:
            player2_score += 1
            spawn_ball("RIGHT", random.choice(["BOTTOM","TOP"]))

    # draw scores
    canvas.draw_text(str(player1_score), (85, 50), 48, 'RED')
    canvas.draw_text(str(player2_score), (485, 50), 48, 'BLUE')

def keydown(key):
    global paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos
    if(key == simplegui.KEY_MAP["W"]):
        paddle1_vel -= 5
    elif(key == simplegui.KEY_MAP["S"]):
        paddle1_vel += 5
    elif(key == simplegui.KEY_MAP["up"]):
        paddle2_vel -= 5
    elif(key == simplegui.KEY_MAP["down"]):
        paddle2_vel += 5

def keyup(key):
    global paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0


def restart_button_handler():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("ReStart", restart_button_handler, 100)


# start frame
new_game()
frame.start()
