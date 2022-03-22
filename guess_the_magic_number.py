import random as rand

# sets the magic
magicNumber = rand.randint(1,10) 
# infinite loop, only broken when the user says so
while True:
	userInput = input()
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

# when the loop is broken, the program ends
print("Thanks for playing! 👀")