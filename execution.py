import numpy as np
import random
from helper import Helper as h

fnProb = [0,0.2,0.5,0.8,0.65]
class Execute:
    
    @classmethod
    def breakties(self,curr,listofcells):
        min_d=h.manhattanDist(curr,listofcells[0])
        win_cell=listofcells[0]
        for cell in listofcells[1:]:
            d=h.manhattanDist(curr,cell)
            if(d<min_d):
                min_d=d
        l=[] #list of cells 
        for cell in listofcells:
            if(h.manhattanDist(curr,cell)==min_d):
                l.append(cell)
        return random.choices(l)[0]

    @classmethod
    def checkfortarget(self,curr,target,terrain):
        if(curr!=target):
            return False
        else:
            n=random.uniform(0,1)
            if(terrain==1):
                return n<0.8
            elif(terrain==2):
                return n<0.5
            elif(terrain==3):
                return n<0.2
    
    @classmethod
    def reevaluate_target(self,curr,pg, known_grid, agentType=6):
        max_prob=0
        for cell,val in np.ndenumerate(pg):
            if(agentType==7):
                val = val*(1-fnProb[int(known_grid[cell])])
            if(val>max_prob):
                max_prob=val
        l=[]      
        """ List of cells having equal probabilities..then we use this list to break ties and return 1 cell (new target) """
        for cell,val in np.ndenumerate(pg):
            if(agentType==7):
                val = val*(1-fnProb[int(known_grid[cell])])
            if(val==max_prob):
                l.append(cell)
        newtarget=self.breakties(curr,l)
        
        while(not h.isMazeSolvable(known_grid,curr,newtarget)):
            known_grid[newtarget] =0        
            self.updateboard(newtarget,0,pg)
            newtarget = self.reevaluate_target(curr,pg,known_grid)
        return newtarget
    
    @classmethod
    def reevaluate_goal_agent7(self,curr,pg, known_grid):
        max_prob=0
        fnProb = [0,0.2,0.5,0.8,0.65]
        for cell,val in np.ndenumerate(pg):
            find_prob = val*(1-fnProb[known_grid[cell]])
            if(find_prob>max_prob):
                max_prob=find_prob
        l=[]
        """ List of cells having equal probabilities..then we use this list to break ties and return 1 cell (new target) """
        for cell,val in np.ndenumerate(pg):
            find_prob = val*(1-fnProb[known_grid[cell]])
            if(find_prob==max_prob):
                l.append(cell)
        newtarget=self.breakties(curr,l)
        
        while(not h.isMazeSolvable(known_grid,curr,newtarget)):
            known_grid[newtarget] =0        
            self.updateboard(newtarget,0,pg)
            newtarget = self.reevaluate_goal_agent7(curr,pg,known_grid)
        
        return newtarget
    @classmethod
    def updateboard(self,curr,terrain,pg):
        multiplier = 1
        if(terrain==0):
            pg[curr]=0
            multiplier=(1/(1-pg[curr]))
        elif(terrain==1):
            pg[curr]=pg[curr]*0.2
            multiplier=(1/(1-pg[curr]*0.8))
        elif(terrain==2):
            pg[curr]=pg[curr]*0.5
            multiplier=(1/(1-pg[curr]*0.5))
        else:
            pg[curr]=pg[curr]*0.8
            multiplier=(1/(1-pg[curr]*0.2))
        
        pg = np.multiply(multiplier, pg)
        return pg