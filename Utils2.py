import heapq
import copy
import sys

def get_sum_of_cost(paths):
    rst = 0
    for path in paths:
        rst += len(path) - 1
    return rst

def move(loc, dir):
    directions = [(0, -1), (1, 0), (0,0), (0, 1), (-1, 0)]
    return loc[0] + directions[dir][0], loc[1] + directions[dir][1]

def get_neighbors(curr_loc, my_map):
    next_locs = []
    for dir in range(5):
        next_loc = move(curr_loc, dir)
        
        # check is valid move
        if next_loc[0] >= 0 and next_loc[1] >= 0 and next_loc[0] < len(my_map[0]) and next_loc[1] < len(my_map) and my_map[next_loc[1]][next_loc[0]] == True:
            next_locs.append(next_loc)
    
    return next_locs

def compute_heuristics(my_map, goal):
    # Use Dijkstra to build a shortest-path tree rooted at the goal location
    open_list = []
    closed_list = dict()
    root = {'loc': goal, 'cost': 0}
    heapq.heappush(open_list, (root['cost'], goal, root))
    closed_list[goal] = root
    i = 0
    while len(open_list) > 0:
        i += 1
        (cost, loc, curr) = heapq.heappop(open_list)
        #print(cost, loc, curr)
        for dir in range(5):
            child_loc = move(loc, dir)
            child_cost = cost + 1
            if child_loc[0] < 0 or child_loc[0] >= len(my_map[0]) \
                or child_loc[1] < 0 or child_loc[1] >= len(my_map):
                continue
            if not my_map[child_loc[1]][child_loc[0]]:
                continue
            child = {'loc': child_loc, 'cost': child_cost}
            if child_loc in closed_list:
                existing_node = closed_list[child_loc]
                if existing_node['cost'] > child_cost:
                    closed_list[child_loc] = child
                    # open_list.delete((existing_node['cost'], existing_node['loc'], existing_node))
                    heapq.heappush(open_list, (child_cost, child_loc, child))
            else:
                closed_list[child_loc] = child
                heapq.heappush(open_list, (child_cost, child_loc, child))

    # build the heuristics table
    h_values = dict()
    for loc, node in closed_list.items():
        h_values[loc] = node['cost']
    return h_values

def get_location(path, time):
    if time < 0:
        return path[0]
    elif time < len(path):
        return path[time]
    else:
        return path[-1]  # wait at the goal location

def get_path(goal_node):
    #start from goal node going up to parent node
    #add location of goal node
    path = [goal_node['loc']]
    prevNode = goal_node
    node = goal_node['parent']
    while node != None:
        time = prevNode['interval'][0] - node['interval'][0]
        for i in range(time):
            path.append(node['loc'])
        prevNode = node
        node = node['parent']
    path.reverse()
    return path

# safe_interval_table should look like this:
#       
#       safe_interval_table[location][interval_id] = [low, high)
#       Ditctionary that is consists of: 
#                        safe_interval_table = {
#                                                   'location1': {
#                                                                   [(low, high), (low2, high2), (low3, high3)...]   # id is the position of each interval (they are in chronological order)
#                                                                 },
#                                                   'location2': {
#                                                                   [(low, high), (low2, high2), (low3, high3)...],    

def build_safe_interval_table(my_map, hard_obstacles, soft_obstacles):

    safe_interval_table = dict()
    locations = []
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == True:
                locations.append((j, i))

    for v in locations:
        intervals = []

        hard_times = []
        if v in hard_obstacles:
            hard_times = copy.copy(hard_obstacles[v])
        soft_times = []
        if v in soft_obstacles:
            soft_times = copy.copy(soft_obstacles[v])

        next_time = 0
        next_time_from = 0
        start_from = 0 #0:clear, 1:soft, 2:hard
        interval_low = 0 
        interval_top = 0 #include top time in interval, ie. [low, top] == [low, top+1) == [low, high)

        if len(hard_times) + len(soft_times) == 0:
            intervals.append((0, sys.maxsize, 0))
        else:
            while len(hard_times) + len(soft_times) > 0:
                #get next time and from which heap
                if len(hard_times) == 0:
                    next_time = heapq.heappop(soft_times)
                    next_time_from = 1
                elif len(soft_times) == 0:
                    next_time = heapq.heappop(hard_times)
                    next_time_from = 2
                elif soft_times[0] < hard_times[0]:
                    next_time = heapq.heappop(soft_times)
                    next_time_from = 1
                else:
                    next_time = heapq.heappop(hard_times)
                    next_time_from = 2


                if next_time_from == start_from:

                    if next_time == interval_top + 1: #direct interval continuation
                        interval_top = next_time
                        continue #skip next interval start setup

                    else: #interval gap, obstacle interval ended and intermediate empty interval inferred
                        #if soft interval add [low, top+1), if hard interval do nothing
                        if start_from == 1:
                            intervals.append((interval_low, interval_top+1, 1))
                        
                        #add empty interval
                        intervals.append((interval_top+1, next_time, 0))

                else: #next_time_from != start_from, automatic interval demarcation
                    if start_from == 0: #only happens on first loop iteration setup
                        if next_time != 0: #[0, next_time) is clear, add clear interval, set up interval tracking variables
                            intervals.append((0, next_time, 0))    

                    if start_from == 1: #after first loop
                        intervals.append((interval_low, interval_top+1, start_from))
                    
                    if next_time > interval_top + 1: #intermediate clear interval
                        intervals.append((interval_top+1, next_time, 0))

                # next interval start setup
                start_from = next_time_from
                interval_low = next_time
                interval_top = next_time

            #add interval for last time sequence if soft
            if start_from == 1:
                intervals.append((interval_low, interval_top+1, 1))
            #add interval for last clear to infinity
            intervals.append((interval_top+1, sys.maxsize, 0))




        safe_interval_table[v] = intervals

    return safe_interval_table