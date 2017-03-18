import solver


def get_path(start=(0,0), end=(3,3), barriers=set(), map_width=3, map_height=3):
	barriers = set()
	(x,y) = start
	barriers = barriers|setup_barriers(map_width, map_height)
	Solver = solver.Star(start, end, barriers)
	while 1:
		if Solver.solution:
			return Solver.solution
		Solver.evaluate()



def setup_barriers(width, height):
    barriers = set()
    for i in range(-1,width+1):
        for j in (-1,height):
            barriers.add((i,j))
    for j in range(-1,height+1):
        for i in (-1,width):
            barriers.add((i,j))
    return barriers