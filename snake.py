import os
import time
import threading

# getch() function will simply ask the user for single key input
# without the need to press enter
class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()
class _GetchUnix:
    def __init__(self):
        import tty, sys
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getwch()
getch = _Getch()

# a simple utility function to clear the terminal
if os.name == 'nt':
	def clear_screen():
		os.system('cls')
else:
	def clear_screen():
		os.system('clear')


# We don't actually have to instatiate an object
# this class will contain our global variables
class Global:
	width = 30
	height = 10
	key = ""
	running = True

# Will represent positional data
class Vec2:
	x = 0
	y = 0
	def __init__(self, _x, _y):
		self.x = _x
		self.y = _y
	def add(self, other):
		self.x += other.x
		self.y += other.y

# Will be our actual snake
class Snake:
	parts = []
	length = 0
	direction = Vec2(0, -1)

	def __init__(self):
		# creates the first element, the head
		self.parts.append(Vec2(Global.width / 2, Global.height / 2))
		self.length = 1
	
	# called every frame
	def update(self):
		if Global.key == "a":
			self.direction = Vec2(-1, 0)
		elif Global.key == "d":
			self.direction = Vec2(1, 0)
		elif Global.key == "w":
			self.direction = Vec2(0, -1)
		elif Global.key == "s":
			self.direction = Vec2(0, 1)
		elif Global.key == "e":
			self.eat()
		
		for i in range(self.length-1, 0, -1):
			self.parts[i].x = self.parts[i-1].x
			self.parts[i].y = self.parts[i-1].y
		
		self.parts[0].add(self.direction)

	
	# called when the snake eats something yummy
	def eat(self):
		self.parts.append(Vec2(-10,-10))
		self.length += 1

# clears the screen and draws onto it
# it runs the 'shader' function for every
# position, giving it the x and y values
# the shader should just return one character
def draw_screen(w, h, shader):
	buf = ""
	for y in range(h):
		for x in range(w):
			buf += shader(x, y)
		print(buf)
		buf = ""

# let's create the snake
snake = Snake()

# this is an example of a shader function
def main_shader(x, y):
	if x == snake.parts[0].x and y == snake.parts[0].y:
		return "Y"
	for i in range(snake.length-1, 0, -1):
		if x == snake.parts[i].x and y == snake.parts[i].y:
			return "O"
	return "."

# neat looking loading screen!
for x in range(1, 31):
	loading = x / 30
	w = int(loading * Global.width)
	h = int(loading * Global.height)
	clear_screen()
	draw_screen(w, h, main_shader)
	time.sleep(0.1)

# A title screen that lets the user get read for action :D 
clear_screen()
draw_screen(Global.width, Global.height, main_shader)
print("------------ SNAKE -----------")
print("> Press W, S, A or D to begin! <\n(Press 'Q' to exit.)")
Global.key = getch()
if Global.key == "q":
	exit()

# Our game loop (drawing to the screen, clearing it and game logic)
# will run on a seperate thread whilst the main one will be busy
# checking user input :D
def gameLoop(arg):
	while Global.running:
		snake.update()
		clear_screen()
		draw_screen(Global.width, Global.height, main_shader)
		time.sleep(0.4)

# Creating a thread 
gameLoopThread = threading.Thread(target=gameLoop, args=(1,))
gameLoopThread.start()

# This is the key checking loop
# it runs here, on the main thread 
# and only stops this thread to ask for input
# whilst the second thread is running our game
while True:
	Global.key = getch()
	if Global.key == "q":
		Global.running = False
		break

# When the game is to be ended, we join the threads
gameLoopThread.join()