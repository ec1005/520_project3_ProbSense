from agent8 import gen_env, solve
import pickle
import numpy as np

'''
p = 0.3

filename = "dataset"
data_file = open(filename, 'wb')


for d in range(10, 70, 10):
	for i in range(100):
		true_grid, true_agent = gen_env(p,d)
	pickle.dump((d,true_grid, true_agent), data_file)

data_file.close()

'''
filename = "dataset"
open_file = open(filename, 'rb')
#data = pickle.load(open_file)


#print(data)
d = {}
for i in range(6):
	d[i] = [0,0,0]
	for k in range(100):
		_, true_grid, true_target = pickle.load(open_file)
		_, move, examine = solve(true_grid, true_target)

		d[i][0] += move
		d[i][1] += examine
		d[i][2] += move+examine

	d[i][0] /= 100
	d[i][1] /= 100
	d[i][2] /= 100

open_file.close()

print(d)