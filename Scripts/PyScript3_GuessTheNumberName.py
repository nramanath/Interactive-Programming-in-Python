# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random


num_range = 100
secret_number = 0
remaining_guesses = 7

# helper function to start and restart the game
def new_game():
    global secret_number, num_range, remaining_guesses
    if(num_range == 100):
        remaining_guesses = 7
    else:
        remaining_guesses = 10

    print ""
    print "New Game. Range is from 0 to",num_range
    secret_number = random.randrange(num_range)
    print "Number of remaining guesses is",remaining_guesses

def reduce_guess():
    global remaining_guesses, secret_number
    remaining_guesses = remaining_guesses - 1
    print "Number of remaining guesses is",remaining_guesses

def range100():
    global num_range
    num_range = 100
    new_game()


def range1000():
    global num_range
    num_range = 1000
    new_game()

def input_guess(guess):
    global secret_number, num_range, remaining_guesses
    result = ""
    print ""
    print "Guess was", guess
    guess = float(guess)
    reduce_guess()
    if(guess == secret_number):
        result = "Correct!"
    elif(guess > secret_number):
        result = "Higher"
    else:
        result = "Lower"

    print result

    if(result == "Correct!"):
        new_game()
    if(remaining_guesses == 0):
        print "You ran out of guesses ! ! ! The number was", secret_number
        new_game()

# creating frame
f = simplegui.create_frame("Guess the number",200,200)

# registering event handlers for control elements and start frame
f.add_button("Range is [0,100)", range100, 200)
f.add_button("Range is [0,1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

new_game()
