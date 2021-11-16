from probSensingMain import moveAgentSixAndSeven
import pickle
import numpy as np
import agent9
from helper import Helper

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
def assignStartNTarget(true_grid):
    start = Helper.create_target(true_grid)
    target = Helper.create_target(true_grid)
    
    while(true_grid[start] == 0 or true_grid[target]== 0 or not Helper.isMazeSolvable(true_grid,start,target)):
        
        start = Helper.create_target(true_grid)
        target = Helper.create_target(true_grid)
    
    return start,target

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
		#print("okay")
		dim, true_grid, true_target = pickle.load(open_file)
		start, true_target = assignStartNTarget(true_grid)
		#print("problem")
		count+=1
	except EOFError:
		print(count)
		break
	#_, move, examine = agent9.moveAgent9(true_grid, true_target, start, start, agentType=6)
	
	#if i != 24:
	#	continue
	#print("True Grid:")
	#print(true_grid)
	#print("True Target:")
	#print(true_target)
	#print("start:")
	#print(start)

	_, move1, examine1 = moveAgentSixAndSeven(true_grid, true_target, start, start, agentType=7)
	
	_, move, examine = moveAgentSixAndSeven(true_grid, true_target, start, start, agentType=6)
	
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