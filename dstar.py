class Dstar(object):
    def __init__(self, start, end, barriers, width, height):
        self.start, self.end = start, end
        self.width, self.height = width, height
        self.barriers = barriers
        self.setup()

    def setup(self):
        self.closed_set = set((self.start,)) #Set of cells already evaluated
        self.open_set   = set() #Set of cells to be evaluated.
        self.came_from = {} #Used to reconstruct path once solved.
        self.gx = {self.start:0} #Cost from start to current position.
        self.hx = {} #Optimal estimate to goal based on heuristic.
        self.fx = {} #Distance-plus-cost heuristic function.
        self.current = self.start
        self.current = self.find_next()
        self.solution = []
        self.solved = False

    def get_neighbors(self):
        neighbors = set()
        for (i,j) in [(1,0),(0,1),(-1,0),(0,-1)]:
            check = (self.current[0]+i,self.current[1]+j)
            if check not in (self.barriers|self.closed_set):
                if check[0]>0 and check[1]>0 and check[0]<self.width and check[1]<self.height:
                    neighbors.add(check)
        return neighbors

    def find_next(self):
        next_cell = None
        next_gx = self.gx[self.current] + 1
        for cell in self.get_neighbors():
            if cell not in self.open_set:
                self.open_set.add(cell)
            elif cell in self.gx and next_gx >= self.gx[cell]:
                continue

            x,y = abs(self.end[0]-cell[0]),abs(self.end[1]-cell[1])
            self.came_from[cell] = self.current
            self.gx[cell] = next_gx
            self.hx[cell] = x+y
            self.fx[cell] = self.gx[cell]+self.hx[cell]
            if not next_cell or self.fx[cell]<self.fx[next_cell]:
                    next_cell = cell
        return next_cell

    def get_path(self,cell):
        """Recursively reconstruct the path. No real need to do it recursively."""
        while cell in self.came_from:
            self.solution.append(cell)
            cell = self.came_from[cell]

    def evaluate(self):
        """Core logic for executing the astar algorithm."""
        if self.open_set and not self.solved:
            for cell in self.open_set:
                if (self.current not in self.open_set) or (self.fx[cell]<self.fx[self.current]):
                    self.current = cell
            if self.current == self.end:
                self.get_path(self.current)
                self.solved = True
            self.open_set.discard(self.current)
            self.closed_set.add(self.current)
            self.current = self.find_next()
        elif not self.solution:
            self.solution = "NO SOLUTION"
