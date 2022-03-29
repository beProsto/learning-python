s = input()
sum = 0
for i in range(0, len(s), 2):
	sum += int(s[i])
print(sum)