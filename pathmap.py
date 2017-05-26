import dstar
import os
import numpy as np
import math

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
    if p3[0] > max(p1[0], p2[0]) or p3[1] > max(p1[1], p2[1]) or p3[0] < min(p1[0], p2[0]) or p3[1] < min(p1[1],p2[1]) :
        return 9999 # as infinite
    elif p1[0]==p2[0]:
        return abs(p3[0]-p1[0])
    elif p1[1]==p2[1]:
        return abs(p3[1]-p1[1])
    return np.linalg.norm(np.cross(p2-p1, p3-p1))/np.linalg.norm(p2-p1)

class PathMap(object):
    def __init__(self, i2b):
        self.im2bin = i2b
        self.barriers = i2b.barriers
        self.waypoint = []
        self.cmd = []
        self.reduced_waypoint = []
        self.reduced_cmd = []
        self.passing_point = [] # list of set. robot must pass this points going through reduced waypoint
        self.update_path(i2b)

    def need_path_update(self, i2b):
        if (self.waypoint == [] or self.waypoint == "NO SOLUTION"): # no path is planned
            return True
        new_barriers = i2b.barriers - self.barriers
        i=len(self.passing_point-1)
        is_in_path = False
        while i >= 0:
            if passing_point(i)&set(i2b.start):
                is_in_path = True
                break
            i = i-1
        if not is_in_path: # if cur pos is too far from planned path (maybe because of inaccuracy)
            return True
        elif (filter(lambda x: x&new_barriers != {}), passing_point[i:]): # if remaining path is blocked
            return True
        else:
            return False

    def update_path(self, i2b):
        # self.barriers = self._setup_barriers(i2b.width+2, i2b.height+2, i2b.barriers)
        self.barriers = i2b.barriers
        self.waypoint = self._find_path(i2b.start, i2b.end, i2b.barriers, i2b.width+2, i2b.height+2)
        if self.waypoint == "NO SOLUTION":
            self.fwrite_path("path.txt")
            return
        else:
            self.cmd = self._waypoint2cmd(i2b.start, list(self.waypoint), i2b.dir)
            self.reduced_waypoint = self._reduce_waypoint()
            self.reduced_cmd = self._waypoint2cmd(i2b.start, list(self.reduced_waypoint), i2b.dir)
            self.passing_point = self._find_passing_point()
            self.fwrite_path("path.txt")

    def fwrite_path(self, txt):
        f = open(txt, 'w')
        if self.waypoint == "NO SOLUTION":
            f.write("NO SOLUTION!!!")
            f_interrupt = open("interrupt.txt", 'w')
            f_interrupt.write("1")
            f_interrupt.close()
        else:
            f.write("width, height: " + str(self.im2bin.width) + ", " + str(self.im2bin.height) + "\n")
            f.write("start: " + str(self.im2bin.start) + "\n")
            f.write("goal: " + str(self.im2bin.end) + "\n")
            f.write("path: " + str(self.waypoint) + " \n")
            f.write("cmd: "  + str(self.cmd) + " \n")
            f.write("reduced_waypoint" + str(self.reduced_waypoint) + " \n")
            f.write("reduced_cmd" + str(self.reduced_cmd) + " \n")
            f.write("passing_point" + str(self.passing_point) + " \n")
        f.close()

    def _find_path(self, start=(2,2), end=(3,3), barriers=set(), map_width=-1, map_height=-1):
        """
        if map_width != -1 and map_height != -1:
            barriers = self._setup_barriers(map_width, map_height, barriers)
        """
        Solver = dstar.Dstar(start, end, barriers, map_width, map_height)
        while 1:
            if Solver.solution:
                break
            Solver.evaluate()
        if Solver.solution == "NO SOLUTION":
            return Solver.solution

        Solver.solution.append(self.im2bin.start)
        Solver.solution.reverse()
        return Solver.solution

    """
    def _setup_barriers(self, width, height, barriers):
        for i in range(0,width):
            for j in (0,height-1):
                barriers.add((i,j))
        for j in range(0,height):
            for i in (0,width-1):
                barriers.add((i,j))
        return barriers
    """
    def _waypoint2cmd(self, start, pos, prev_dir=np.array([1,0])):
        cmd = []
        if pos == []:
            return cmd
        start = np.asarray(pos.pop(0))
        while pos != []:
            end = np.asarray(pos.pop(0))
            cur_dir = unit(end-start)
            sign = np.sign(np.linalg.det([prev_dir, cur_dir])) # if v1 is ccw from v2, then pos
            if sign==0: sign = 1
            cmd.append(rad2deg(sign*(np.arccos(np.clip(np.dot(prev_dir, cur_dir), -1.0, 1.0))))) # angle
            cmd.append(np.linalg.norm(end-start)) #dist
            start = end
            prev_dir = cur_dir
        return cmd

    def _is_reducable(self, p):
        return len(filter((lambda x : _dist(p[0], p[2], x) <= 1.5), self.barriers))==0

    def _reduce_waypoint_1step(self, wp):
        accum = []
        while 1:
            if len(wp) < 3:
                return accum + wp
            elif self._is_reducable(wp[0:3]):
                return accum + [wp[0], wp[2]] + wp[3:]
            else:
                accum = accum + [wp[0]]
                wp = wp[1:]
                continue

    def _reduce_waypoint(self):
        wp = list(self.waypoint)
        while 1:
            prev_len = len(wp)
            wp = self._reduce_waypoint_1step(wp)
            if prev_len == len(wp):
                break
        return wp

    def _find_passing_point_1step(self, a, b):
        passing_point_1step = set()
        for i in range(min(a[0],b[0]), max(a[0],b[0])+1):
            for j in range(min(a[1],b[1]), max(a[1],b[1])+1):
                if _dist(a,b, (i,j)) <= 1.5:
                    passing_point_1step.add((i,j))
        return passing_point_1step

    def _find_passing_point(self):
        passing_point = []
        for i in range(len(self.reduced_waypoint)-1):
            passing_point.append(self._find_passing_point_1step(self.reduced_waypoint[i], self.reduced_waypoint[i+1]))
        passing_point.append(self._find_passing_point_1step(self.im2bin.start, self.reduced_waypoint[len(self.reduced_waypoint)-1]))
        return passing_point
