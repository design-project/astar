import solver
import os
import numpy as np

def get_path(start=(2,2), end=(3,3), barriers=set(), map_width=5, map_height=5):
	f = open("path.txt", 'w')
	if map_width != -1 and map_height != -1:
		barriers = setup_barriers(map_width, map_height, barriers)
	Solver = solver.Star(start, end, barriers)
	while 1:
		if Solver.solution:
			break
		Solver.evaluate()
	f.write("start: " + str(start) + "\n")
	f.write("goal: " + str(end) + "\n")
	#f.write("barriers: " + str(barriers) + "\n")
	f.write("path: " + str(Solver.solution) + " \n")
	f.write("cmd: "  + str(coord2cmd(start, Solver.solution)) + " \n")
	return Solver.solution

def setup_barriers(width, height, barriers):
    for i in range(0,width):
        for j in (0,height-1):
            barriers.add((i,j))
    for j in range(0,height):
        for i in (0,width-1):
            barriers.add((i,j))
    return barriers

def coord2cmd(start, pos, prev_dir=np.array([1,0])):
	"""
	Returns the commands corresponding to the path points

		>>> coord2cmd([(1,2),(1,3),(2,3)])
		[0.0, 1.0, 1.5707963267948966, 1.0]
		[angle, dist, angle, dist]
	"""
	cmd = []
	if pos == []:
		return cmd
	while pos != []:
		end = np.asarray(pos.pop())
		cur_dir = unit(end-start)
		sign = np.sign(np.linalg.det([prev_dir, cur_dir])) # if v1 is ccw from v2, then pos
		if sign==0: sign = 1
		cmd.append(rad2deg(sign*(np.arccos(np.clip(np.dot(prev_dir, cur_dir), -1.0, 1.0))))) # angle
		cmd.append(np.linalg.norm(end-start)) #dist
		start = end
		prev_dir = cur_dir
	return cmd

def unit(vector):
	return vector/np.linalg.norm(vector)

def rad2deg(rad):
	result = rad * 180 / np.pi
	return round(result, 3)

print(coord2cmd((1,1),[(1,2),(1,3),(2,3)]))


"""
test

for x1 in range(-1, 2):
	for y1 in range(-1, 2):
		for x2 in range(-1, 2):
			for y2 in range(-1, 2):
				if (x1==0 and y1==0) or (x2==0 and y2==0):
					continue
				print("prev_dir: " + str([x1,y1]) + " cur_dir: " + str([x2,y2]))
				prev_dir = unit(np.array([x1,y1]))
				cur_dir = unit(np.array([x2,y2]))
				sign = np.sign(np.linalg.det([cur_dir,prev_dir]))
				if sign==0: sign = 1
				print(sign* rad2deg(np.arccos(np.clip(np.dot(prev_dir, cur_dir), -1.0, 1.0))))
"""