from numpy import true_divide
import numpy as np
from execution import Execute
from helper import Helper
import time

from planning import PlanHelper

def moveAgentSixAndSeven(true_grid, actual_target, goal, start = (0,0), agentType = 6):
        
    n = len(true_grid)   
    known_grid = -1*np.ones([n,n])
    pg = np.full((n,n),1/n**2)
    p_multiplier = 1
    
    movements, examinations = 0,0
    trace = []
    
    path = PlanHelper.planAndGetPath(known_grid,(0,0), goal)
    pIndex = 0
    curr = path[pIndex]
    prev = None
    
    while(pIndex>=0):
        ## ------- MOVE ----------
        
        curr = path[pIndex]
        trace.append(curr)
        isPathBlocked = False
        known_grid[curr] = true_grid[curr]
        
        ## ------- Is the current cell blocked? -------------
        if(true_grid[curr] == 0):  
            #if(known_grid[curr] != 0):
                #print("ERROR here")         
            pg = Execute.updateboard(curr,true_grid[curr], pg)
            trace.pop(-1)
            if(curr == goal or not Helper.isMazeSolvable(known_grid,path[pIndex-1], goal)):
                goal = Execute.reevaluate_target(path[pIndex-1],pg,known_grid,agentType=agentType) 
            if(goal1 == goal):
                print("OMG WTF", curr, goal)
            
            #goal = goal1
                       
            path = PlanHelper.planAndGetPath(known_grid, path[pIndex-1], goal)
            pIndex=0
        elif(curr==goal):
             ## ------- If current the planned goal is reached, check if target is found. If found, game over -------------
            
            isTargetFound = Execute.checkfortarget(curr, actual_target, true_grid[curr])
            if(isTargetFound):
                return goal, len(trace), examinations;
            else:
                ## ---------- If target not found, update the board -----------
                examinations+=1
                pg = Execute.updateboard(curr,true_grid[curr], pg)
                goal1 = Execute.reevaluate_target(curr,pg, known_grid,agentType=agentType)  
                if(goal1 == goal):
                    print("OMG WTF", curr, goal)        
                goal = goal1   
                           
                path = PlanHelper.planAndGetPath(known_grid, curr, goal)
                pIndex = 0
        else:
            pIndex+=1
                
    return Execute.reevaluate_target(curr,pg,known_grid, agentType=agentType), len(trace), examinations  

DIM = 31
#true_grid = Helper.gen_grid(0.3,DIM)
#true_grid = Helper.make_terrain(true_grid)
#target = Helper.create_target(true_grid)
#while(not Helper.isMazeSolvable(true_grid, (0,0), target)):
#    true_grid = Helper.make_terrain(Helper.gen_grid(0.3,DIM));
#    target = Helper.create_target(true_grid)
#print(true_grid, target)
#start_time = time.time();
#discoveredTarget = moveAgentSixAndSeven(true_grid, target, (0,0), agentType=6)
#print(discoveredTarget, target)
#print(time.time()-start_time)
#start_time = time.time()
#discoveredTarget = moveAgentSixAndSeven(true_grid, target, (0,0), agentType=7)
#print(discoveredTarget, target)
#print(time.time()-start_time)
"""true_grid = np.block([[3, 2, 0, 3, 0],
 [1, 0, 1, 1, 2],
 [0, 2, 0, 0, 3],
 [0, 3, 1, 0, 0],
 [0, 2, 2, 0, 2]])

target = (0,0)
print(true_grid, target)
discoveredTarget = moveAgentSixAndSeven(true_grid, target, (0,0), agentType=6)
print(discoveredTarget, target)"""
        
        
    
        
