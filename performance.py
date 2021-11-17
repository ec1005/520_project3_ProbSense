#from probSensingMain import moveAgentSixAndSeven
from agent8_new import solve
import pickle
import numpy as np
#import agent9
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
def assignStartNTarget(true_grid, terrain=0):
    start = Helper.create_target(true_grid)
    target = Helper.create_target(true_grid)
    flag = True
    #print(terrain)
    if(terrain>0):
        flag = (true_grid[target] == terrain)
    count=0
    
    while(not flag or true_grid[start] == 0 or true_grid[target]== 0 or not Helper.isMazeSolvable(true_grid,start,target)):
        
        start = Helper.create_target(true_grid)
        target = Helper.create_target(true_grid)
        if(terrain>0 and count<=1000):
            flag = (true_grid[target] == terrain)
        if(count>1000):
            flag=True
    
    return start,target

filename = "dataset2"
open_file = open(filename, 'rb')
#data = pickle.load(open_file)


#print(data)
d = {}
d1 = {}


count = 0
terrains = ["flat", "hilly", "forest"]

for i in range(180):
    
    
    print(i)
      
    try:
        #print("okay")
        dim, true_grid, true_target = pickle.load(open_file)
        start, true_target = assignStartNTarget(true_grid, min(3,int(count/33)+1))
        #terrain = terrains[true_grid[true_target]-1]
        #print("problem")
        count+=1        
        count = count%100
    except EOFError:
        print(count)
        break
    #_, move, examine = agent9.moveAgent9(true_grid, true_target, start, start, agentType=6)

    #if i != 24:
    #   continue
    #print("True Grid:")
    #print(true_grid)
    #print("True Target:")
    #print(true_target)
    #print("start:")
    #print(start)

    #_, move1, examine1 = moveAgentSixAndSeven(true_grid, true_target, start, start, agentType=7)

    _, move, examine = solve(true_grid, true_target, start)
    #_, move2, examine2 = solve(true_grid, true_target, start)
    #_, move, examine = agent9.moveAgent9(true_grid, true_target, start, start, agentType=6)
    if dim in d.keys():

        d[dim][0].append(move) 
        d[dim][1].append(examine)
        d[dim][2].append(move+examine)

        #d1[dim][0].append(move1)
        #d1[dim][1].append(examine1)
        #d1[dim][2].append(move1+examine1)

    else:
        d[dim] = [[move], [examine], [move+examine]]
        #d1[dim] = [[move1], [examine1],[move1+examine1]]
        # d2[dim] = [[move2], [examine2],[move2+examine2]]

print("Agent8")
for key in d.keys():
    print(f"Dim: {key}")
    
    print("Move: ")
    print(d[key][0])

    print("Examine: ")
    print(d[key][1])

    print("Examine+ Move: ")
    print(d[key][2])
    

#print("Agent7")
#for key in d.keys():
#    print(f"Dim: {key}")
    
#    print("Move: ")
#    print(d[key][0])

#    print("Examine: ")
#    print(d[key][1])

#    print("Examine+ Move: ")
#    print(d[key][2])
    


open_file.close()
