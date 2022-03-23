# usually imports into an object called "random", now it'll be called "rand"
import random as rand

# we have to have something to set int the first place,
# let it be the range of numbers that our number can be
rangeStart = 1
rangeEnd = 10

# this function will begin our game
def gameLoop():
	# define the globals we're going to use in this function's scope
	global rangeStart
	global rangeEnd
	# sets the magic number
	magicNumber = rand.randint(rangeStart, rangeEnd)
	# tell the user what to do
	print("The magic number is between", rangeStart, "and", rangeEnd, "🏁")
	# infinite loop, only broken when the user says so
	while True:
		userInput = input("Guess the number: ")
		# if the user wants to quit, break out of the loop
		if userInput == "q" or userInput == "quit":
			break
		
		# try-catch block, python throws an exception if the text we want to turn
		# into a number is not, in fact, a number.
		try:
			guess = int(userInput)
		except:
			print("Your guess isn't a number! If you want to exit ( 💀 ), type \"quit\"")
			continue # skips this loop, jumps to the next one
		
		# if the user guessed the number right, we should break the loop
		if guess == magicNumber:
			print("Your guess was right! 🎉")
			break
		elif guess > magicNumber:
			print("Sadly Your guess was bigger than the magic number 😔, try again though!")
		elif guess < magicNumber:
			print("Sadly Your guess was smaller than the magic number 😭, try again though!")

# this function lets the user into the options menu
def optionsMenu():
	# define the globals we're going to use in this function's scope
	global rangeStart
	global rangeEnd
	# print the user's options
	print("Welcome to the menu screen! 🤚")
	# infinite loop, only broken when the user says so
	while True:
		print("If you want to set the range the magic number can be in, press '1'.")
		print("If you want to back out to the main menu, press '2'.")
		userInput = input("Choose the option: ")
		# try-catch block, python throws an exception if the text we want to turn
		# into a number is not, in fact, a number.
		try:
			option = int(userInput)
		except:
			print("Your input isn't a number!")
			continue # skips this loop, jumps to the next one
		
		# The user's options
		if option == 2:
			break
		elif option == 1:
			try:
				rangeStartTemp = int(input("The start of the range: "))
				rangeEndTemp = int(input("The end of the range: "))
			except:
				print("Your choosing isn't a number! To try again, type \"1\"")
				continue # skips this loop, jumps to the next one
			if(rangeStartTemp<rangeEndTemp):
				rangeStart = rangeStartTemp
				rangeEnd = rangeEndTemp
				print("The range is now:", rangeStart, "->", rangeEnd)
			else:
				print("The range is wrong! 💀")
		else:
			print("That is not an option! 🤚")

# print the user's options
print("Welcome to \"Guess the magic number\"! 🔥")
# infinite loop, only broken when the user says so
while True:
	print("If you want to start the game, press '1'.")
	print("If you want to see the options menu, press '2'.")
	print("If you want to exit, type \"quit\".")
	userInput = input("What do you wanna do: ")
	# if the user wants to quit, break out of the loop
	if userInput == "q" or userInput == "quit":
		break

	# try-catch block, python throws an exception if the text we want to turn
	# into a number is not, in fact, a number.
	try:
		option = int(userInput)
	except:
		print("Your input isn't a number! If you want to exit out of the game, type \"quit\"")
		continue # skips this loop, jumps to the next one

	if option == 1:
		gameLoop()
	elif option == 2:
		optionsMenu()
	else:
		print("That is not a valid option!")

# when the loop is broken, the program ends
print("Thanks for playing! 👀")