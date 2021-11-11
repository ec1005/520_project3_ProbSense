import numpy as np
from queue import Queue,PriorityQueue,LifoQueue 
from collections import deque
import time
import random

class Helper:
    
    """GENERATE TRUE GRID || Create Terrain || Generate Target """
    #DIM_GRID = 5
    #DENSITY = 0.3
    
    @classmethod
    def gen_grid(self,p, n):
        G =1* (np.random.rand(n,n)>p)
        while(G[0][0] != 1):
            G =1* (np.random.rand(n,n)>p)
        return G
    
    @classmethod
    def make_terrain(self,grid):
        for cell,val in np.ndenumerate(grid):
            if grid[cell] != 0:
                grid[cell] += random.randint(0,2)
        return grid

    @classmethod
    def create_target(self,grid):
        dim = len(grid)
        i = random.randint(0,dim-1)
        j = random.randint(0,dim-1)
        
        while(grid[(i,j)] == 0):
            i = random.randint(0,dim-1)
            j = random.randint(0,dim-1)
            
        return (i,j)
    
    @classmethod
    def manhattanDist(self,cellA, cellB):
        '''Calculates Manhattan distance between two given cells'''
        return abs(cellB[0]-cellA[0]) + abs(cellB[1]-cellA[1])

    @classmethod
    def generateChildren(self,cell, G):
        """For astar search"""
        n = len(G)
        i,j = cell
        res = []
        if(i>0):
            if abs(G[(i-1,j)])>0:
                res.append((i-1, j))
        if(j>0):
            if abs(G[(i,j-1)])>0:
                res.append((i, j-1))
        if(j<n-1):
            if abs(G[(i, j+1)])>0:
                res.append((i, j+1))
        if(i<n-1):
            if abs(G[(i+1, j)])>0:
                res.append((i+1, j))

        return res



    @classmethod
    def a_star(self,G,start,goal, he=(1,0,0),checkingSolvability=False):
        n = G.shape[0]
        g = {}
        h = {}
        processed = {}
        prev = {}
        numOfCells = 0

        for i in range(n):
            for j in range(n):

                h[(i,j)] = self.manhattanDist((i,j),goal)
                
                g[(i, j)] = n * n  # inifinity for now
                processed[(i, j)] = 0
                prev[(i, j)] = None

        g[start] = 0
        fringe = PriorityQueue()

        fringe.put((g[start] + h[start], start))
        prev[start] = None

        while not fringe.empty():
            (f, curr_node) = fringe.get()        

            if curr_node == goal:
                return (True, prev, numOfCells)

            if not processed[curr_node]:
                numOfCells += 1
                children = self.generateChildren(curr_node, G)
                if(start[0]>=goal[0] and start[1]>=goal[1]):
                    print("CHILDREN ", children)
                for child in children:
                    if g[curr_node] + 1 < g[child]:
                        g[child] = g[curr_node] + 1
                        fringe.put((g[child] + h[child], child))
                        prev[child] = curr_node

                processed[curr_node] = 1
        
        return (False, None, numOfCells)
    
    @classmethod
    def DFS(self,G, start, goal):
        n=G.shape[0]
        processed={}
        prev={}
        
        for i in range(n):
            for j in range(n):
                processed[(i,j)]=0
                prev[(i,j)]=None
        
        prev[start]=None
        fringe=LifoQueue()
        fringe.put(start)
        
        while not fringe.empty():
            current=fringe.get()
            if current==goal:
                return True, prev,None
            else:
                if not processed[current]:
                    children=self.generateChildren(current,G)
                    for child in children:
                        if not processed[child]:
                            fringe.put(child)
                            prev[child]=current
                    processed[current]=1
        return False, None, None
    
    @classmethod
    def isMazeSolvable(self,iGrid, root, goal):
        solved, prevMap,_ = self.DFS(iGrid, root, goal)
        return solved

"""true_grid = Helper.gen_grid(0.3,9)
target = Helper.create_target(true_grid)
while(not Helper.isMazeSolvable(true_grid, (0,0), target)):
    true_grid = Helper.make_terrain(Helper.gen_grid(0.3,9));
    target = Helper.create_target(true_grid)
print(true_grid, target)"""