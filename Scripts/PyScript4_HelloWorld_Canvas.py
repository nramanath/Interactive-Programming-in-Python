# Drawing Canvas

# Computer monitor - 2D grid of pixels stored in frame buffer

# Computers update the monitor based on the frame buffer at rate of
# around 60-72 times a second - refresh rate

# Many applications will registr a special function called a
# "draw handler"

# In code skulptor , register a draw handler using simpleGUI command
# CodeSkulptor calls the draw handler at around 60 times / second

# Draw handler updates the canvas using a collection of draw commands that
# include draw_text, draw_line, draw_circle

# simplwgui.create_frame("Title", width, height)

# the top left corner is (0,0)
# width extending from left to right
# height extending from top to bottom

import simplegui

# steps
# define the draw_handler
# create the frame
# register the draw_handler
# start frame

def draw(canvas):
    canvas.draw_text("Hello Ramanathan!",[75,75], 20, "White")
    canvas.draw_circle([75,75], 2, 2, "Red")

frame = simplegui.create_frame("Test",300,300)

frame.set_draw_handler(draw)

frame.start()