import numpy as np
import random
from helper import Helper as h
from copy import deepcopy 
fnProb = [0,0.2,0.5,0.8,0.65]
class Execute:
    
    @classmethod
    def breakties(self,curr,listofcells):
        ''' Breakties within cells of same prbabilities by manhattan distance'''
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
        return random.choice(l)

    @classmethod
    def checkfortarget(self,curr,target,terrain):
        '''examines the current cell for target, gives false negatives on case to case basis'''
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
        '''finds a new target based on probability grid'''
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

    @classmethod
    def prob_contains_target(self,prob_grid, known_grid, xy, terrain_xy):
        case = 0
        if known_grid[xy] == 0:
            case = 1
        elif known_grid[xy] == 1:
            case = 0.8

        elif known_grid[xy] == 2:
            case = 0.5

        elif known_grid[xy] == 3:
            case = 0.2

        factor = 1/(1-(prob_grid[xy]*case))

        prob_grid = np.multiply(factor,prob_grid)
        
        prob_grid[xy] = prob_grid[xy]*(1-case)

        return prob_grid

    @classmethod
    def prob_find_target(self,prob_grid, known_grid):

        factor = deepcopy(prob_grid)
        factor[factor == -1] = 0.7 * 0.5
        factor[factor == 1] = 0.8
        factor[factor == 2] = 0.5
        factor[factor == 3] = 0.2

        #prob_grid = np.multiply(factor, prob_grid)
        return factor