import solver
import os
import numpy as np
import tmp_im2bin as im2bin

def unit(vector):
	return vector/np.linalg.norm(vector)

def rad2deg(rad):
	result = rad * 180 / np.pi
	return round(result, 3)

def _dist(p1, p2, p3):
	""" p1, p2 makes line l1. return dist between l1 and p3"""
	p1 = np.array(p1)
	p2 = np.array(p2)
	p3 = np.array(p3)
	if p3[0] > max(p1[0], p2[0]) or p3[1] > max(p1[1], p2[1]):
		return 9999 # as infinite
	return np.linalg.norm(np.cross(p2-p1, p3-p1))/np.linalg.norm(p2-p1)


class PathMap(object):
	def __init__(self, im2bin):
		barriers = self._setup_barriers(im2bin.width, im2bin.height, im2bin.barriers)
		waypoint = self._find_path(im2bin.start, im2bin.end, im2bin.barriers, im2bin.width, im2bin.height)
		cmd = self._waypoint2cmd(im2bin.start, waypoint, im2bin.dir)

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

	def _is_reducable(self, p):
		return len(filter((lambda x : _dist(p[1], p[3], x) <= 1), self.barriers))==0

	def _reduce_waypoint_1step(self, wp):
		accum = []
		while 1:
			if len(wp) < 3:
				return accum + wp
			elif _is_reducable(wp[0:3]):
				return accum + [wp[0], wp[2]] + wp[3:]
			else:
				accum = accum + [wp[0]]
				wp = wp[1:]
				continue

	def _reduce_waypoint(self):
		wp = self.waypoint
		while 1:
			prev_len = len(wp)
			wp = _reduce_waypoint_1step(wp)
			if prev_len == len(wp):
				break
		return wp

