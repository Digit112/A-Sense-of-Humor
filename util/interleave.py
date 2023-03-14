# A script that takes two chart files and interleaves them into a single one.

import json

ekob = open("../audio/1.json", "r")
edat = json.loads(ekob.read())["notes"]
ekob.close()

ship = open("../audio/2.json", "r")
sdat = json.loads(ship.read())["notes"]
ship.close()

new_notes = [[], [], [], []]
for c in range(0, 4):
	e_cur = 0
	s_cur = 0
	
	while True:
		if e_cur < len(edat[c]) and s_cur < len(sdat[c]):
			if edat[c][e_cur] < sdat[c][s_cur]:
				new_notes[c].append(edat[c][e_cur])
				e_cur += 1
			elif edat[c][e_cur] > sdat[c][s_cur]:
				new_notes[c].append(sdat[c][s_cur])
				s_cur += 1
			else:
				new_notes[c].append(edat[c][e_cur])
				e_cur += 1
				s_cur += 1
				
		elif e_cur < len(edat[c]):
			new_notes[c].append(edat[c][e_cur])
			e_cur += 1
			
		elif s_cur < len(sdat[c]):
			new_notes[c].append(sdat[c][s_cur])
			s_cur += 1
		
		else:
			break

ekob = open("audio/ekob.json", "r")
edat = json.loads(ekob.read())
ekob.close()
edat["notes"] = new_notes

fout = open("audio/test.json", "w")
fout.write(json.dumps(edat))
fout.close()
	