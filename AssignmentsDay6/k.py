s = input()
prev = "0"
ans = "YES"
for c in s:
	if c == "1" and prev == "1":
		ans = "NO"
		break
	prev = c
print(ans)