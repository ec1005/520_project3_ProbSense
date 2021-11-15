from helper import Helper
from planning import PlanHelper
from execution import Execute
from copy import deepcopy
import numpy as np
import time
# generate true_grid
# generate prob_grid
# generate known_grid
# true_target

def solve(true_grid, true_target, start = (0,0)):

	N = true_grid.shape[0]
	known_grid = -1 * np.ones((N,N))
	prob_grid = np.full((N,N), 1/(N**2))
	prob_eval_grid = deepcopy(prob_grid)
	
	target = Execute.reevaluate_target(start, prob_eval_grid, known_grid)
	path = PlanHelper.planAndGetPath(known_grid, start, target)
	pos = 0
	
	
	#print("path:", path)
	move_count, examine_count = 0,0

	#for i in range(min(100,len(path))):
	while (True):
		#print(i)
		# ----- Sense Pos -------
		#print("path[pos]:", path[pos])
		known_grid[path[pos]] = true_grid[path[pos]]
		if true_grid[path[pos]] == 0:
			
			prob_grid = Execute.prob_contains_target(prob_grid, known_grid, path[pos], known_grid[path[pos]])
			#find_factor = Execute.prob_find_target(prob_grid, known_grid)
			#prob_eval_grid = np.multiply(find_factor, prob_grid)
			prob_eval_grid = prob_grid
			# should it come before updating others?
			#prob_grid[path[pos]] = 0
			if(path[pos] == target or not Helper.isMazeSolvable(known_grid,path[pos-1],target)):
				target=Execute.reevaluate_target(path[pos-1], prob_eval_grid,known_grid)
	
			next_path = PlanHelper.planAndGetPath(known_grid, path[pos-1], target)
			path = path[:pos+1]+next_path

		elif path[pos] == target:
			"""print("path[pos]:",path[pos])
			print("known_grid: ", known_grid)
			print("prob_grid: ", prob_grid)"""
			# check terrain
			if known_grid[path[pos]] == 1:
				#flat
				n = 2
			if known_grid[path[pos]] == 2:
				#hilly
				n = 4
			if known_grid[path[pos]] == 3:
				#forest
				n = 12

			for i in range(n):
				if Execute.checkfortarget(path[pos], true_target, known_grid[path[pos]]):
					examine_count += 1
					#prob_grid = Execute.prob_contains_target(prob_grid, known_grid, path[pos], known_grid[path[pos]])
					#find_factor = Execute.prob_find_target(prob_grid, known_grid)
					#prob_eval_grid = np.multiply(find_factor, prob_grid)
					#print("TARGET FOUND", path[pos], len(path))
					return True, move_count, examine_count
				else:
					prob_grid = Execute.prob_contains_target(prob_grid, known_grid, path[pos], known_grid[path[pos]])
					#find_factor = Execute.prob_find_target(prob_grid, known_grid)
					#prob_eval_grid = np.multiply(find_factor, prob_grid)
					prob_eval_grid = prob_grid
					examine_count+=1
			#target not found ==> reevaluate target
			
			target = Execute.reevaluate_target(path[pos], prob_eval_grid,known_grid)
			#print("TARGET NOT FOUND - new target is ", target, examine_count)
			next_path = PlanHelper.planAndGetPath(known_grid, path[pos], target)
			path = path[:pos] + next_path

		pos+=1
		move_count+=1
		if pos == len(path):
			break
	return False, move_count, examine_count









def gen_env(p, N):
	true_grid = Helper.gen_grid(p,N)
	true_grid = Helper.make_terrain(true_grid)
	true_target = Helper.create_target(true_grid)

	while(not Helper.isMazeSolvable(true_grid, (0,0), true_target)):
		true_grid = Helper.gen_grid(p,N)
		true_grid = Helper.make_terrain(true_grid)
		true_target = Helper.create_target(true_grid)

	return true_grid, true_target


tg, tt = gen_env(0.3, 101)
#("true_grid:\n", tg)
#print("true_target:\n", tt)
st = time.time()
print(solve(tg, tt))
print(time.time() - st)