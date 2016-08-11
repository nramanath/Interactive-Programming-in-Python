# SimpleGUI program template

# Import the module
import simplegui

# Define the global variables
counter = 0

# Define "Helper" functions
def increment():
    global counter
    counter = counter + 1

# Define the classes

# Define event handler functions
def tick():
    increment()
    print counter

def buttonpress():
    global counter
    counter = 0

# Create a frame
frame = simplegui.create_frame("SimpleGUI Test Frame", 200, 200)
frame.add_button("Click Me", buttonpress)

# Regsiter event handlers
timer = simplegui.create_timer(1000, tick)

# Start frame and timers
frame.start()
timer.start()