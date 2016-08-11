# implementation of card game - Memory

import simplegui
import random

NUMBER_OF_CARDS = 16
FONT_FACE = "serif"
FONT_SIZE =75
FONT_COLOR = "Red"

# helper function to initialize globals
def init():
    global cards, exposed, state, moves
    cards = list(range(0,NUMBER_OF_CARDS/2)) * 2
    random.shuffle(cards)
    exposed = [False] * NUMBER_OF_CARDS
    state = []
    moves = 0
    label.set_text("Moves = " + str(moves))


def update_state(selected):
    global state # list storing clicked cards position
    global exposed, cards, moves

    exposed[selected] = True
    if len(state) == 0:
        moves += 1
    elif len(state) == 1:
        if cards[state[0]] == cards[selected]:
            # exposed the pair
            exposed[state.pop()] = True
            return
    elif len(state) == 2:
        exposed[state.pop()] = False
        exposed[state.pop()] = False
        moves += 1
    state.append(selected)
    label.set_text("Moves = " + str(moves))


# define event handlers
def mouse_click(pos):
    # add game state logic here
    global state
    selected = int(pos[0]/50);
    if exposed[selected] == False:
        update_state(selected)


# cards are logically 50x100 pixels in size
def draw(canvas):
    global cards
    for idx in range(NUMBER_OF_CARDS):
        if exposed[idx]:
            text_width = frame.get_canvas_textwidth(str(cards[idx]),FONT_SIZE,FONT_FACE)
            canvas.draw_text(str(cards[idx]),(idx*50+(50-text_width)/2,FONT_SIZE),FONT_SIZE,FONT_COLOR,FONT_FACE)
        else:
            canvas.draw_polygon([(idx*50,0),((idx+1)*50,0),((idx+1)*50,100),(idx*50,100),(idx*50,0)],1,"Red","Green")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("ReStart", init)
label = frame.add_label("Moves")


# initialize global variables
init()


# register event handlers
frame.set_mouseclick_handler(mouse_click)
frame.set_draw_handler(draw)


# get things rolling
frame.start()

# Always remember to review the grading rubric