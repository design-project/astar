import solver
import os
import numpy as np

def unit(vector):
	return vector/np.linalg.norm(vector)

def rad2deg(rad):
	result = rad * 180 / np.pi
	return round(result, 3)


class PathMap(object):
	def __init__(self, im2bin):
		barriers = self._setup_barriers(im2bin.width, im2bin.height, im2bin.barriers)
		waypoint = self._find_path(im2bin.start, im2bin.end, im2bin.barriers, im2bin.width, im2bin.height)
		cmd = self._waypoint2cmd(im2bin.start, self.waypoint, im2bin.dir)

	def fwrite_path(txt):
		f = open(txt, 'w')
		f.write("start: " + str(im2bin.start) + "\n")
		f.write("goal: " + str(im2bin.end) + "\n")
		f.write("path: " + str(self.waypoint) + " \n")
		f.write("cmd: "  + str(cmd) + " \n")

	def _find_path(self, start=(2,2), end=(3,3), barriers=set(), map_width=-1, map_height=-1):
		if map_width != -1 and map_height != -1:
			barriers = self._setup_barriers(map_width, map_height, barriers)
		Solver = solver.Star(start, end, barriers)
		while 1:
			if Solver.solution:
				break
			Solver.evaluate()
		return Solver.solution

	def _setup_barriers(self, width, height, barriers):
	    for i in range(0,width):
	        for j in (0,height-1):
	            barriers.add((i,j))
	    for j in range(0,height):
	        for i in (0,width-1):
	            barriers.add((i,j))
	    return barriers

	def _waypoint2cmd(self, start, pos, prev_dir=np.array([1,0])):
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

