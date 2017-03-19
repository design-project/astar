import solver
import os


def get_path(start=(0,0), end=(3,3), barriers=set(), map_width=4, map_height=4):
	os.chdir("C:\\Users\\jmpark8187\\Documents\\Python\\pathfinding")
	f = open("path.txt", 'w')
	(x,y) = start
	barriers = setup_barriers(map_width, map_height, barriers)
	Solver = solver.Star(start, end, barriers)
	while 1:
		if Solver.solution:
			f.write("start: " + str(start) + "\n")
			f.write("goal: " + str(end) + "\n")
			f.write("barriers: " + str(barriers) + "\n")
			f.write("path: " )
			for x in Solver.solution:
				f.write(str(x) + ", ")
			return Solver.solution
		Solver.evaluate()



def setup_barriers(width, height, barriers):
    for i in range(0,width):
        for j in (0,height-1):
            barriers.add((i,j))
    for j in range(0,height):
        for i in (0,width-1):
            barriers.add((i,j))
    return barriers