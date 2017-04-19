# Path finding from the image taken by drone

### im2bin:
* class im2bin
>* public member variable
>>* grid_size: int, size of each grid
>>* start: tuple, xy coord of sumo position e.g. (1,2)
>>* end: tuple, xy coord of destination e.g. (10,15)
>>* width: int, number of horizontal grid cells
>>* height: int, number of vertical grid cells
>>* barriers: set of tuples, xy coord of each obstacles e.g. {(1,1),(1,2),(1,3)}
>>* direction: tuple, unit vector indicating cur direction of sumo e.g. (0.707, 0.707)
>* public method
>>* set_grid_size: set grid size, update all related variables

### pathmap:
* class PathMap
>* public method
>>* fwrite_path: make a txt file containing path waypoints and correspoding cmds


### solver:
* using A* get grid map and return way points
* from solver.py is from Mekire's find-a-way-astar-pathfinding
* https://github.com/Mekire/find-a-way-astar-pathfinding.git
