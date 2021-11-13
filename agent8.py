from helper import Helper
from planning import PlanHelper
from exection import Execute
from copy import deepcopy
# generate true_grid
# generate prob_grid
# generate known_grid
# true_target

def solve(true_grid, true_target, start = (0,0)):

	N = true_grid.shape[0]
	known_grid = -1 * np.ones((N,N))
	prob_grid = np.full((N,N), 1/(N**2))
	prob_eval_grid = deepcopy(prob_grid)
	
	target = Execute.reevaluate_target(pos, prob_eval_grid)

	path = PlanHelper.planAndGetPath(known_grid, start, target)
	pos = 0
	
	move_count, examine_count = 0,0

	for i in range(100):
	#while (True):

		# ----- Sense Pos -------
		known_grid = true_grid[path[pos]]
		if true_grid[path[pos]] == 0:
			
			prob_grid = Execute.prob_contains_target(prob_grid, known_grid)
			find_factor = Execute.prob_find_target(prob_grid, known_grid)
			prob_eval_grid = np.multiply(find_factor, prob_grid)
			# should it come before updating others?
			prob_grid[path[pos]] = 0

			next_path = Helper.a_star(known_grid,path[pos-1],target)
			path = path[:pos+1]+next_path

		elif path[pos] == target:
			# check terrain
			if known_grid[pos] == 1:
				#flat
				n = 1
			if known_grid[pos] == 2:
				#hilly
				n = 2
			if known_grid[pos] == 3:
				#forest
				n = 5

			for i in range(n):
				if Execute.checkfortarget(path[pos], true_target, known_grid[path[pos]]):
					examine_count += 1
					prob_grid = Execute.prob_contains_target(prob_grid, known_grid)
					find_factor = Execute.prob_find_target(prob_grid, known_grid)
					prob_eval_grid = np.multiply(find_factor, prob_grid)
					return True, move_count, examine_count

			#target not found ==> reevaluate target
			target = Execute.reevaluate_target(path[pos], prob_eval_grid)
			next_path = Helper.a_star(known_grid, path[pos], target)
			path = path[pos] + next_path

		pos+=1
		move_count+=1
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

