from collections import deque
from helper import Helper


class PlanHelper:
    
    @classmethod
    def plan(G, start, goal):
        return Helper.a_star(G,start,goal)
    
    @classmethod
    def getPath(self,prevMap, start, goal):
            
        # We could have also used queue.LifoQueue here. But collections.deque is faster and has more options.    
        path = []
        path.append(goal)
        current = goal
        
        while True:
            if current == start:
                break
            path.append(prevMap[current])        
            current = prevMap[current]
             
        return path[::-1]  
    
    @classmethod
    def planAndGetPath(self,G, start, goal):
        solved, prevMap, _ =  Helper.a_star(G,start,goal)
        if(not solved):
            print("Planning.....", start, goal)
            print("Known grid ", G)
            #print("DFS Result ", Helper.DFS(G, start, goal))
            
        return self.getPath(prevMap, start,goal)
    
     