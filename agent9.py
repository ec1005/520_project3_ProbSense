import numpy as np
from execution import Execute
from helper import Helper
import time
from planning import PlanHelper
import random

def gen_dyn_env(p,n):
    true_grid = Helper.gen_grid(p,n)
    true_grid = Helper.make_terrain(true_grid)
    start = Helper.create_target(true_grid)
    target = Helper.create_target(true_grid)
    
    while(not Helper.isMazeSolvable(true_grid,start,target)):
        start = Helper.create_target(true_grid)
        target = Helper.create_target(true_grid)
    
    return true_grid,start,target

def genAllNeighbours(kg,curr):
    i,j = curr
    res = []
    
    for indi in range(i-1,i+2):
        if(indi < 0 or indi >= len(kg)):
            continue
        for indj in range(j-1, j+2):
            if(indj < 0 or indj >= len(kg)):
                continue
            if(kg[(indi, indj)] != 0):
                res.append((indi, indj))
    return res

def sense(kg,curr, tt):
    children = genAllNeighbours(kg,curr)
    if tt in children:
        return True
    return False

def moveTarget(tg, curr):
    i,j = curr
    n = len(tg)
    #arr = [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]
    arr = Helper.generateChildren(curr, tg)
    ind = random.randint(0,len(arr)-1)
    
    while(tg[arr[ind]] == 0):
        ind = random.randint(0,3)
    
    return arr[ind]

def noOfMoveableDirections(kg, curr):
    return len(Helper.generateChildren(curr,kg))

def checkForTargetA9(curr, actual_target):
    return curr==actual_target

def calculateIntermediateProbWhenNotSensed(pg,kg, blockedCells, curr):
    den = pg.shape[0]**2 - blockedCells -1
    pg = 1*(kg!=0)
    pg[curr] = 0
    pg = np.multiply((1/den), pg)    
    return pg

def calculateIntermediateProbWhenSensed(pg,kg, curr):
    neighbourList = genAllNeighbours(kg, curr)
    n=len(kg)
    temp_grid = np.zeros((n,n))
    for neighbour in neighbourList:
        probOfNeigh = 1/len(neighbourList)
        children = Helper.generateChildren(neighbour,kg)
        for child in children:
            temp_grid[child] += probOfNeigh*(1/len(children))
    
    pg = temp_grid
    return pg

def moveAgent9(true_grid, actual_target, goal, start, agentType = 6):
    n = len(true_grid)   
    known_grid = -1*np.ones([n,n])
    pg = np.full((n,n),1/n**2)
    p_multiplier = 1
    
    '''Function Aliases for ease of reference below'''
    nmd = noOfMoveableDirections
    gan = genAllNeighbours
    
    movements, examinations = 0,0
    trace = []
    
    path = PlanHelper.planAndGetPath(known_grid,start, goal)
    pIndex = 0
    curr = path[pIndex]
    prev = None
    startExamining = False
    blockedCells = 0
    
    while(pIndex>=0):
        ## ------- MOVE --------
        
        curr = path[pIndex]
        trace.append(curr)
        isPathBlocked = False
        known_grid[curr] = true_grid[curr]
        #print(curr, actual_target)
        
        ## ------- Is the current cell blocked? -------------
        if(true_grid[curr] == 0):  
            blockedCells+=1
            pg = Execute.updateboard(curr,true_grid[curr], pg)
            trace.pop(-1)
            #if(curr == goal or not Helper.isMazeSolvable(known_grid,path[pIndex-1], goal)):
            goal = Execute.reevaluate_target(path[pIndex-1],pg,known_grid,agentType=agentType) 
            path = PlanHelper.planAndGetPath(known_grid, path[pIndex-1], goal)
            pIndex=0
            
        elif(not sense(known_grid, curr, actual_target)): 
            if(startExamining == True):
                examinations+=1
                if(checkForTargetA9(curr, actual_target)):
                    return curr, len(trace), examinations          
            startExamining = False            
            pg = calculateIntermediateProbWhenNotSensed(pg, known_grid, blockedCells, curr)
            if(curr == goal):                
                goal = Execute.reevaluate_target(path[pIndex],pg,known_grid,agentType=agentType)
                path = PlanHelper.planAndGetPath(known_grid, path[pIndex], goal)
                pIndex = 0
            else:
                pIndex+=1
            
        else:
            #print("TARGET IS IN ONE OF THE NEARBY CELLS")
            if(startExamining == True):
                examinations+=1
                if(checkForTargetA9(curr, actual_target)):
                    return curr, len(trace), examinations
                """if(curr==goal):
                    goal = Execute.reevaluate_target(curr,pg,known_grid,agentType=agentType)
                    path = PlanHelper.planAndGetPath(known_grid, path[pIndex], goal)
                    pIndex = 0
                else:                    
                    pIndex+=1"""
            #else:
            startExamining = True            
            pg = calculateIntermediateProbWhenSensed(pg, known_grid,curr)
            goal = Execute.reevaluate_target(curr,pg,known_grid,agentType=agentType)
            path = PlanHelper.planAndGetPath(known_grid, path[pIndex], goal)
            pIndex = 0
            
            #print(pg, goal)
        
        actual_target = moveTarget(true_grid,actual_target)
       
        #pIndex+=1
                
    return Execute.reevaluate_target(curr,pg,known_grid, agentType=agentType), len(trace), examinations

tg, start, tt = gen_dyn_env(0.3, 31)
print(tg,start,tt)

print(moveAgent9(tg, tt, start, start, agentType=6))