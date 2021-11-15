from agent8 import gen_env, solve
import pickle
import numpy as np

'''
p = 0.3

filename = "dataset2"
data_file = open(filename, 'wb')

count = 0
for d in range(10, 70, 10):
	for i in range(30):
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
count = 0
for i in range(180):
	print(i)
	try:
		dim, true_grid, true_target = pickle.load(open_file)
		count+=1
	except EOFError:
		print(count)
		break
	_, move, examine = solve(true_grid, true_target)
	if dim in d.keys():

		d[dim][0] += move
		d[dim][1] += examine
		d[dim][2] += move+examine
	else:
		d[dim] = [move, examine, move+examine]


for key in d.keys():
	d[key][0] /= 30
	d[key][1] /= 30
	d[key][2] /= 30

open_file.close()

print(d)
