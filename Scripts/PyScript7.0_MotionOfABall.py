import simplegui

h = 600
w = 400
radius = 20
position = [w/2 , h/2]

velocity = [-10.0,10.0]

def draw(canvas):
    canvas.draw_circle(position, radius, 2, "Red", "White")

    position[0] += velocity[0]
    position[1] += velocity[1]

    if((position[0] <= radius) or (position[0] + radius >= w)):
        velocity[0] = - velocity[0]

    if((position[1] <= radius) or (position[1] +  radius >= h)):
        velocity[1] = - velocity[1]

frame = simplegui.create_frame("Tracking Motion of a Ball", w,h)

frame.set_draw_handler(draw)

frame.start()