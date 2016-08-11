#it
# implementation of Spaceship - program template for RiceRocks
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
ROCKS = 10

class ImageInfo:
    def __init__ (self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float ('inf')
        self.animated = animated

    def get_center (self):
        return self.center

    def get_size (self):
        return self.size

    def get_radius (self):
        return self.radius

    def get_lifespan (self):
        return self.lifespan

    def get_animated (self):
        return self.animated



# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector (ang):
    return [math.cos (ang), math.sin (ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__ (self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def increment_angle_vel (self):
        self.angle_vel += .05

    def decrement_angle_vel (self):
        self.angle_vel -= .05

    def get_position (self):
        return self.pos

    def get_radius (self):
        return self.radius

    def update (self):
        global started

        if started:
            # update angle
            self.angle += self.angle_vel

            # update position
            self.pos[0] =  (self.pos[0] + self.vel[0]) % WIDTH
            self.pos[1] =  (self.pos[1] + self.vel[1]) % HEIGHT

            if self.thrust:
                acc = angle_to_vector (self.angle)
                self.vel[0] += acc[0] * .4
                self.vel[1] += acc[1] * .4

            self.vel[0] *= .9
            self.vel[1] *= .9

    def draw (self,canvas):
        global started
        if self.thrust and started:
            canvas.draw_image (self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image (self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")


    def set_thrust (self, on):
        global started
        self.thrust = on
        if started and on :
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()

    def shoot (self):
        global missiles, started
        if started:
            forward = angle_to_vector (self.angle)
            missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
            missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
            missiles.add (Sprite (missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))

# Sprite class
class Sprite:
    def __init__ (self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center ()
        self.image_size = info.get_size ()
        self.radius = info.get_radius ()
        self.lifespan = info.get_lifespan ()
        self.animated = info.get_animated ()
        self.age = 0
        if sound:
            sound.rewind ()
            sound.play ()

    def get_position (self):
        return self.pos

    def get_radius (self):
        return self.radius

    def draw (self, canvas):
        if self.animated:
            canvas.draw_image (self.image, [self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image (self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update (self):
        # update angle
        self.angle += self.angle_vel

        # update position
        self.pos[0] =  (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] =  (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1

        if self.age < self.lifespan:
            return False
        else:
            return True

    def collide (self, other):
        if dist (self.pos, other.get_position ()) <= self.radius + other.get_radius ():
            return True
        else:
            return False


# key handlers to control ship
def keydown_handler (key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel ()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel ()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust (True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot ()

def keyup_handler (key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel ()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel ()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust (False)

def click_handler (pos):
    global started, score, lives, ROCKS
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size ()
    inwidth =  (center[0] - size[0] / 2) < pos[0] <  (center[0] + size[0] / 2)
    inheight =  (center[1] - size[1] / 2) < pos[1] <  (center[1] + size[1] / 2)
    if  (not started) and inwidth and inheight:
        started = True
        score = 0
        lives = 3
        ROCKS = 10
        ship_thrust_sound.rewind ()
        explosion_sound.rewind ()
        missile_sound.rewind ()
        soundtrack.rewind ()
        soundtrack.play ()

def draw_handler (canvas):
    global time, started, score, lives, ROCKS, rocks, my_ship, explosions, missiles

    # animiate background
    time += 1
    wtime =  (time / 4) % WIDTH
    center = debris_info.get_center ()
    size = debris_info.get_size ()
    canvas.draw_image (nebula_image, nebula_info.get_center (), nebula_info.get_size (), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image (debris_image, center, size,  (wtime - WIDTH / 2, HEIGHT / 2),  (WIDTH, HEIGHT))
    canvas.draw_image (debris_image, center, size,  (wtime + WIDTH / 2, HEIGHT / 2),  (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text ("Lives", [50, 50], 22, "White")
    canvas.draw_text ("Score", [680, 50], 22, "White")
    canvas.draw_text (str (lives), [50, 80], 22, "White")
    canvas.draw_text (str (score), [680, 80], 22, "White")

    # draw and update ship
    my_ship.draw (canvas)
    my_ship.update ()

    # process sprite group
    process_sprite_group (rocks, canvas)
    process_sprite_group (explosions, canvas)
    process_sprite_group (missiles, canvas)

    # handling collisions
    if group_collide (rocks, my_ship) > 0:
        lives -= 1
    if lives == 0:
        started = False
        soundtrack.pause ()
        soundtrack.rewind ()
        my_ship = Ship ([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        rocks = set ([])
        missiles = set ([])
        explosions = set ([])
    score += group_group_collide (rocks, missiles) * 10
    if score > 360:
        ROCK_MAX = score // 30
    # draw splash screen if not started
    if not started:
        canvas.draw_image (splash_image, splash_info.get_center (), splash_info.get_size (), [WIDTH / 2, HEIGHT / 2], splash_info.get_size ())

# timer handler that spawns a rock
def rock_spawner ():
    global rocks, my_ship, started, ROCKS, asteroid_info
    rock_pos = [random.randrange (0, WIDTH), random.randrange (0, HEIGHT)]
    rock_vel = [random.random () * .6 - .3, random.random () * .6 - .3]
    rock_avel = random.random () * .2 - .1
    if started:
        if len (rocks) < ROCKS:
            if dist (rock_pos, my_ship.get_position ()) > asteroid_info.get_radius () + my_ship.get_radius () + 10:
                rocks.add (Sprite (rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))

def group_collide (group, other):
    number_of_collisions = 0
    neg_set = set ([])
    for sprite in group:
        if sprite.collide (other):
            explosions.add (Sprite (sprite.pos, [0, 0], 0, 0, explosion_image, explosion_info))
            explosion_sound.rewind ()
            explosion_sound.play ()
            neg_set.add (sprite)
            number_of_collisions += 1
    if len (neg_set) > 0:
        group.difference_update (neg_set)
    return number_of_collisions

def group_group_collide (set1, set2):
    number_of_collisions = 0
    neg_set = set ([])
    for sprite in set1:
        if group_collide (set2, sprite) > 0:
            neg_set.add (sprite)
            number_of_collisions += 1
    if len (neg_set) > 0:
        set1.difference_update (neg_set)
    return number_of_collisions

def process_sprite_group (group, canvas):
    neg_set = set ([])
    for sprite in group:
        if sprite.update ():
            neg_set.add (sprite)
        else:
            sprite.draw (canvas)
    if len (neg_set) > 0:
        group.difference_update (neg_set)

# main intialization
frame = simplegui.create_frame ("Asteroids", WIDTH, HEIGHT)
my_ship = Ship ([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rocks = set ([])
missiles = set ([])
explosions = set ([])

# handlers
frame.set_keyup_handler (keyup_handler)
frame.set_keydown_handler (keydown_handler)
frame.set_mouseclick_handler (click_handler)
frame.set_draw_handler (draw_handler)

timer = simplegui.create_timer (1000.0, rock_spawner)

# get things rolling
timer.start ()
frame.start ()