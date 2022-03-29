string = input()
sub = ""
# for every character in the string we add it to the substring
for l in string:
	sub += l
	# after adding each character to the sub, we check if it repeats itself exactly the same through the whole string
	res = ""
	for c in string:
		res += c
		if res == sub:
			res = ""
	# if it does repeat, we break out of the loop
	if res == "":
		break

print(sub)
