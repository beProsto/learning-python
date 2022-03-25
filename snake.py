import os
import time
import threading
import random

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
	width = 20
	height = 10
	key = ""
	running = True
	lost = False

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

# This will be the screen we will draw each frame 
class Screen:
	display = []
	clear_cell = "."

	def __init__(self):
		for y in range(Global.height):
			for x in range(Global.width):
				self.display.append(self.clear_cell)
	
	def draw(self, x, y, c):
		if x >= 0 and x < Global.width and y >= 0 and y < Global.height:
			self.display[int(y * Global.width + x)] = c
	
	def clear(self, x, y):
		if x >= 0 and x < Global.width and y >= 0 and y < Global.height:
			self.display[int(y * Global.width + x)] = self.clear_cell
	
	def get(self, x, y):
		if x >= 0 and x < Global.width and y >= 0 and y < Global.height:
			return self.display[int(y * Global.width + x)]
		else:
			return self.clear_cell
	
	def isClear(self, x, y):
		if x >= 0 and x < Global.width and y >= 0 and y < Global.height and self.display[int(y * Global.width + x)] != self.clear_cell:
			return False
		else:
			return True


screen = Screen()

# This will be the food for our snake
class Food:
	pos = Vec2(8, 2)

	def __init__(self):
		screen.draw(self.pos.x, self.pos.y, "@")

	def reposition(self):
		while True:
			x = random.randint(0, Global.width-1)
			y = random.randint(0, Global.height-1)
			if screen.isClear(x, y):
				self.pos = Vec2(x, y)
				screen.draw(self.pos.x, self.pos.y, "@")
				return

food = Food()

# Will be our actual snake
class Snake:
	parts = []
	length = 0
	direction = Vec2(0, -1)

	def __init__(self):
		# creates the first element, the head
		self.parts.append(Vec2(Global.width / 2, Global.height / 2))
		self.length = 1
		screen.draw(self.parts[0].x, self.parts[0].y, "Y")
	
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
		# elif Global.key == "e":
		# 	self.eat()
		
		screen.clear(self.parts[0].x, self.parts[0].y)
		screen.clear(self.parts[self.length-1].x, self.parts[self.length-1].y)
		
		for i in range(self.length-1, 0, -1):
			self.parts[i].x = self.parts[i-1].x
			self.parts[i].y = self.parts[i-1].y
			screen.draw(self.parts[i].x, self.parts[i].y, "O")
			if i != 1 and self.parts[0].x == self.parts[i].x and self.parts[0].y == self.parts[i].y:
				Global.lost = True
				return
		
		self.parts[0].add(self.direction)
		screen.draw(self.parts[0].x, self.parts[0].y, "Y")

		if self.parts[0].x >= Global.width or self.parts[0].x < 0 or self.parts[0].y >= Global.height or self.parts[0].y < 0:
			Global.lost = True
		
		if self.parts[0].x == food.pos.x and self.parts[0].y == food.pos.y:
			food.reposition()
			self.eat()
	
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
	return screen.display[y * Global.width + x]

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
print("-" * int((Global.width-7)/2) + "- SNAKE " + "-" * int((Global.width-7)/2))
print("> Press W, S, A or D to begin! <\n(Press Q to exit.)")
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
		if Global.lost:
			print("You've Lost! Press Q to quit!")
			Global.running = False

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