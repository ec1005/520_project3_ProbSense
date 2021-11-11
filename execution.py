import numpy as np
import random
from helper import Helper as h

class Execute:
    
    @classmethod
    def breakties(self,curr,listofcells):
        min_d=h.manhattanDist(curr,listofcells[0])
        win_cell=listofcells[0]
        for cell in listofcells[1:]:
            d=h.manhattanDist(curr,cell)
            if(d<min_d):
                min_d=d
                #win_cell=cell
        #return win_cell
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
    def reevaluate_target(self,curr,pg):
        max_prob=0
        for cell,val in np.ndenumerate(pg):
            if(val>max_prob):
                max_prob=val
        l=[]
                
        """ List of cells having equal probabilities..then we use this list to break ties and return 1 cell (new target) """
        for cell,val in np.ndenumerate(pg):
            if(val==max_prob):
                l.append(cell)
        newtarget=self.breakties(curr,l)
        return newtarget

    @classmethod
    def updateboard(self,curr,true_grid,pg,multiplier):
        if(true_grid[curr]==0):
            pg[curr]=0
            multiplier=multiplier*(1/(1-pg[curr]))
        elif(true_grid[curr]==1):
            pg[curr]=pg[curr]*0.2
            multiplier=multiplier*(1/(1-pg[curr]*0.8))
        elif(true_grid[curr]==2):
            pg[curr]=pg[curr]*0.5
            multiplier=multiplier*(1/(1-pg[curr]*0.5))
        else:
            pg[curr]=pg[curr]*0.8
            multiplier=multiplier*(1/(1-pg[curr]*0.2))
        return multiplier