import solver
import os
import numpy as np
import interface
import pygame as pg

width = 22
height = 14

class im2bin(object):
    def __init__(self, State):
    	self.grid_size = 1
    	self.start = State.start_cell
    	self.end = State.goal_cell
    	self.width = State.width
    	self.height = State.height
    	self.barriers = State.barriers
        self.direction = (1,0)

    def set_grid_size(self, size):
    	grid_size = size
    	_update(size)

    def _update(self, size):
    	print "update start, end, width, height, obstacle"