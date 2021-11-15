from probSensingMain import moveAgentSixAndSeven
import pickle
import numpy as np

'''
p = 0.3
filename = "dataset"
data_file = open(filename, 'wb')
count = 0
for d in range(10, 70, 10):
	for i in range(100):
		true_grid, true_agent = gen_env(p,d)
		count+=1
		print(count)
		pickle.dump((d,true_grid, true_agent), data_file)
data_file.close()
'''

filename = "dataset2"
open_file = open(filename, 'rb')
#data = pickle.load(open_file)


#print(data)
d = {}
d1 = {}
count = 0
for i in range(180):
	print(i)
	try:
		dim, true_grid, true_target = pickle.load(open_file)
		count+=1

	except EOFError:
		print(count)
		break
	_, move, examine = moveAgentSixAndSeven(true_grid, true_target, (0,0), agentType=6)
	_, move1, examine1 = moveAgentSixAndSeven(true_grid, true_target, (0,0), agentType=7)
	if dim in d.keys():

		d[dim][0] += move
		d[dim][1] += examine
		d[dim][2] += move+examine

		d1[dim][0] += move1
		d1[dim][1] += examine1
		d1[dim][2] += move1+examine1
	else:
		d[dim] = [move, examine, move+examine]
		d1[dim] = [move1, examine1, move1+examine1]


for key in d.keys():
	d[key][0] /= 30
	d[key][1] /= 30
	d[key][2] /= 30

	d1[key][0] /= 30
	d1[key][1] /= 30
	d1[key][2] /= 30

open_file.close()

print("Agent 6: ", d)
print("Agent 7: ", d1)