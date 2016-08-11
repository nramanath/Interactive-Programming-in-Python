# template for "Stopwatch: The Game"
import simplegui

# define global variables
display_string = "0:00.0"
time, score, attempts = 0, 0, 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(number):
    # A:BC.D
    global display_string
    D = number % 10
    number -= D
    number /= 10
    A =  number / 60
    BC = number %  60
    BC = "%02d"%BC
    display_string = str(A) + ":" + str(BC)+ "." + str(D)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button_handler():
    timer.start()

def stop_button_handler():
    global time, score, attempts
    timer.stop()
    attempts += 1
    if(time % 10 == 0):
        score += 1

def reset_button_handler():
    global display_string, time, score, attempts
    display_string = "0:00.0"
    timer.stop()
    time, score, attempts = 0, 0, 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time = time + 1
    format(time)

# define draw handler
def draw(canvas):
    canvas.draw_text(display_string, [100,160], 40, "Red")
    canvas.draw_text(str(score) + "/" + str(attempts), [250,40], 30, "Green")

# create frame
frame = simplegui.create_frame("StopWatch The Game", 300, 300)
timer = simplegui.create_timer(100, timer_handler)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button("Start", start_button_handler, 75)
frame.add_button("Stop", stop_button_handler, 75)
frame.add_button("Reset", reset_button_handler, 75)

# start frame
frame.start()

# Please remember to review the grading rubric
