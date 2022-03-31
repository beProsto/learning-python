# import the standard GUI library
import tkinter as tk

# define the initial dimensions of the window
class Initial:
	width = 640
	height = 360
	title = "The Castle Wolfenstein 2: Electric Boogaloo"

# this will store information about our keyboard's state
class Keyboard:
	pressed = {}
def onKeyDown(event):
    if (event.keysym in Keyboard.pressed) != True:
        Keyboard.pressed[event.keysym] = "down"
def onKeyUp(event):
    if (event.keysym in Keyboard.pressed) == True:
        Keyboard.pressed.pop(event.keysym)

# lets us check if a certain key is down
def isKeyDown(key):
	return (key in Keyboard.pressed)

# a monolythic class containerising window construction
class Renderer:
	def __init__(self):
		# create a window
		self.window = tk.Tk()
		# create a canvas (space to draw on, workspace)
		self.canvas = tk.Canvas(self.window, width=Initial.width, height=Initial.height, bg="#3f3f3f", highlightthickness=0)
		# initialise window's size (using the initial width and height)
		self.window.geometry("x".join(map(str, [Initial.width, Initial.height])))
		# set the window's title (using the initial title)
		self.window.title(Initial.title)
		# we want our app to be resizable
		self.canvas.pack(fill="both", expand=True)
		self.width = Initial.width
		self.height = Initial.height
		self.canvas.bind("<Configure>", self.onResize)
		# keypress
		self.window.bind("<KeyPress>", onKeyDown)
		self.window.bind("<KeyRelease>", onKeyUp)
		# wether or not we're fullscreen
		self.isFullscreen = False
		# reference to a function
		self.updateFunc = None
	
	# this will be useful as it will tell us what the current window's size is
	def onResize(self, event):
		self.width = event.width
		self.height = event.height
		self.canvas.config(width=self.width, height=self.height)

	def onUpdate(self):
		self.updateFunc()
		renderer.window.after(16, self.onUpdate) # schedule the game loop function


	# >>>> User functions (API): <<<<

	#  choose fullscreen state
	def fullscreen(self, _bool):
		self.window.attributes("-fullscreen", _bool)
		self.isFullscreen = _bool
	#  exit the programme
	def quit(self):
		self.window.quit()
	#  begin the programme (supply the proper frame update function)
	def start(self, updateFunc):
		self.updateFunc = updateFunc
		renderer.window.after(16, self.onUpdate) # schedule the game loop function
		renderer.window.mainloop() # begin the event loop

renderer = Renderer()

class ImageManager:
	def __init__(self):
		self.images = {}
	
	def getImage(self, name):
		img = self.images.get(name)
		if img == None:
			return self.images.get(name, tk.PhotoImage(file=name))
		return img

imageManager = ImageManager()

# Will represent positional data
class Vec2:
	def __init__(self, _x, _y):
		self.x = _x
		self.y = _y
	def add(self, other):
		self.x += other.x
		self.y += other.y
		return self

class Renderable:
	_x = 0
	_y = 0
	width = 0
	height = 0
	id = 0
	
	def realPosition(self):
		bounds = renderer.canvas.bbox(self.id)
		self.width = bounds[2] - bounds[0]
		self.height = bounds[3] - bounds[1]
		self._x = bounds[0]
		self._y = bounds[1]

	def setPosition(self, pos):
		renderer.canvas.move(self.id, pos.x-self._x, pos.y-self._y)
		self._x = pos.x
		self._y = pos.y
	def getPosition(self):
		return Vec2(self._x, self._y)

	def setX(self, x):
		renderer.canvas.move(self.id, x-self._x, self._y)
		self._x = x
	def setY(self, y):
		renderer.canvas.move(self.id, self._x, y-self._y)
		self._y = y

	def getX(self):
		return self._x
	def getY(self):
		return self._y


class Image(Renderable):
	def __init__(self, img):
		self.id = renderer.canvas.create_image(0, 0, image=img)
		self.realPosition()
		self.setPosition(Vec2(0,0))

class Text(Renderable):
	def __init__(self, text, fill="white", font=("Arial", 12)):
		self.id = renderer.canvas.create_text(0, 0, text=text, fill=fill, font=font)
		self.realPosition()
		self.setPosition(Vec2(0,0))

class App():
	# this will happen at the start of our application
	def __init__(self):
		# we load up an image and scale it down (subsample()) (zoom() would make our image bigger)
		self.img = imageManager.getImage("assets/img/firefox.gif").subsample(5) 
		# we create an image object (the previous one only held image data)
		self.image = Image(self.img)

		# a text object
		self.text = Text("TkInter Test Application!", "#00ffff", ("Helvetica", 20, "bold italic"))
		
		# make it fullscreen
		# renderer.fullscreen(True)
		# makes sure we aren't in a fullscreen toggle loop
		self.hasFullscreenChanged = False

		# we start the game loop
		renderer.start(self.update)

	# this will happen every 16 milliseconds (60 times per second)
	def update(self):
		# we roll the text around the screen:
		# add 1 to text's x
		self.text.setX(self.text.getX() + 1)
		# when it's outside the window
		if self.text.getX() > renderer.width:
			# reposition it behind the window
			self.text.setX(-self.text.width)
		
		# we center the image
		self.image.setPosition(Vec2(
			renderer.width // 2 - self.image.width // 2,
			renderer.height // 2 - self.image.height // 2
		))

		# upon pressing f11, we toggle fullscreen
		if isKeyDown("F11") and not self.hasFullscreenChanged:
			renderer.fullscreen(not renderer.isFullscreen)
			self.hasFullscreenChanged = True
		elif not isKeyDown("F11"):
			self.hasFullscreenChanged = False

		# if we pressed escape, we exit
		if isKeyDown("Escape"):
			renderer.quit()

app = App()