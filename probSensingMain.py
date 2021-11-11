from numpy import true_divide
import numpy as np
from execution import Execute
from helper import Helper

from planning import PlanHelper

def moveAgentSix(true_grid, actual_target, goal, start = (0,0), agentType = 6):
        
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
        print(path, curr)
        ## ------- MOVE ----------
        curr = path[pIndex]
        trace.append(curr)
        isPathBlocked = False
        known_grid[curr] = true_grid[curr]
        
        ## ------- Is the current cell blocked? -------------
        if(true_grid[curr] == 0):
            print(curr,"Cell is blocked")            
            p_multiplier = Execute.updateboard(curr,true_grid, pg, p_multiplier)
            pg = np.multiply(p_multiplier, pg)
            p_multiplier = 1
            print(pg)
            trace.pop()
            if(curr == goal):
                goal = Execute.reevaluate_target(curr,pg)
            path = PlanHelper.planAndGetPath(known_grid, path[pIndex-1], goal)
            pIndex=0
        elif(curr==goal):
             ## ------- If current the planned goal is reached, check if target is found. If found, game over -------------
            
            isTargetFound = Execute.checkfortarget(curr, actual_target, true_grid[curr])
            #print("At expected Goal ",goal, " Target found? ",isTargetFound)
            if(isTargetFound):
                return goal;
            else:
                #print("Target not found at ",goal)
                ## ---------- If target not found, update the board -----------
                p_multiplier = Execute.updateboard(curr,true_grid, pg, p_multiplier)
                pg = np.multiply(p_multiplier, pg)
                p_multiplier = 1
                goal = Execute.reevaluate_target(curr,pg)
                path = PlanHelper.planAndGetPath(known_grid, curr, goal)
                pIndex = 0
        else:
            pIndex+=1
                
    return Execute.reevaluate_target(curr,pg)   

DIM = 5
true_grid = Helper.gen_grid(0.3,DIM)
true_grid = Helper.make_terrain(true_grid)
target = Helper.create_target(true_grid)
while(not Helper.isMazeSolvable(true_grid, (0,0), target)):
    true_grid = Helper.make_terrain(Helper.gen_grid(0.3,DIM));
    target = Helper.create_target(true_grid)
print(true_grid, target)

discoveredTarget = moveAgentSix(true_grid, target, (0,0))
print(discoveredTarget, target)
        
        
    
        
