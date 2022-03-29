s = input()
sinv = ""
for i in range(len(s)-1, -1, -1):
	sinv += s[i]
if(sinv == s):
	print("YES")
else:
	print("NO")