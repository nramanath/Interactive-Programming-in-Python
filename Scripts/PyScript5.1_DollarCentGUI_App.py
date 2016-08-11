# Interactive application to convert a float in dollars and cents

import simplegui


# define global value

value = 3.12


# Handle siungle quantity
def convert_units(val, name):
    converted_string = str(val) + " " + name
    if val > 1:
        converted_string = converted_string + 's'
    return converted_string

# conver xx.yy to xx dollars and yy cents
def convert(val):
    dollar = int(val)
    cent = round(100 * (val - dollar))

    dollar_string = convert_units(dollar, "dollar")
    cent_string = convert_units(cent, "cent")

    if(dollar == 0):
        return cent_string
    elif(cent == 0):
        return dollar_string
    elif(dollar == 0 and cent ==0):
        return "broke"
    else:
        return dollar_string+" and "+cent_string

# define draw handler
def draw(canvas):
    canvas.draw_text(convert(value), [100,100], 18, "White")

# define an input field handler
def input_handler(text):
    global value
    value = float(text)

# create a frame
frame = simplegui.create_frame("Converter", 300, 200)

# register event handlers
frame.set_draw_handler(draw)
frame.add_input("Enter value",input_handler,100)

# start frame
frame.start()