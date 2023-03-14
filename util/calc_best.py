# A script that calculates the maximum score of a chart file.

import json

targ = "test.json"

fin = open("../audio/" + targ, "r")
dat = json.loads(fin.read())["notes"]
fin.close()

s = 0
for i in range(0, 4):
	s += len(dat[i])

print(s*20)