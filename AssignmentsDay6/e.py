s = input()
alice = 0
bob = 0
for f in s:
	if f == "A":
		alice += 1
	elif f == "B":
		bob += 1
if alice == bob:
	print("DRAW")
elif alice > bob:
	print("ALICE")
else:
	print("BOB")