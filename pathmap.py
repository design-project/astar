import dstar
import os
import numpy as np

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
        self.waypoint = []
        self.barriers = set()
        self.update(i2b)

    def is_blocked(self, i2b):
        if (self.waypoint == [] or self.waypoint == "NO SOLUTION"):
            return True
        elif (set(self.waypoint) & i2b.barriers):
            return True
        else:
            return False

    def update(self, i2b):
        self.im2bin = i2b
        # self.barriers = self._setup_barriers(i2b.width+2, i2b.height+2, i2b.barriers)
        self.barriers = i2b.barriers
        self.waypoint = self._find_path(i2b.start, i2b.end, i2b.barriers, i2b.width+2, i2b.height+2)
        if self.waypoint == "NO SOLUTION":
            return
        else:
            self.cmd = self._waypoint2cmd(i2b.start, list(self.waypoint), i2b.dir)
            self.reduced_waypoint = self._reduce_waypoint()
            self.reduced_cmd = self._waypoint2cmd(i2b.start, list(self.reduced_waypoint), i2b.dir)


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
            f.write("reduced_path" + str(self.reduced_waypoint) + " \n")
            f.write("reduced_cmd" + str(self.reduced_cmd) + " \n")
        f.close()

    def _find_path(self, start=(2,2), end=(3,3), barriers=set(), map_width=-1, map_height=-1):
        if map_width != -1 and map_height != -1:
            barriers = self._setup_barriers(map_width, map_height, barriers)
        Solver = dstar.Dstar(start, end, barriers, map_width, map_height)
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
        start = np.asarray(start)
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
        return len(filter((lambda x : _dist(p[0], p[2], x) <= 1), self.barriers))==0

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
        wp = wp+[self.im2bin.start]
        while 1:
            prev_len = len(wp)
            wp = self._reduce_waypoint_1step(wp)
            if prev_len == len(wp):
                break
        wp.pop()
        return wp
