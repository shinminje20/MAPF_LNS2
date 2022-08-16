import heapq
import copy

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
        if not next_loc[0] < 0 or  next_loc[1] < 0 or  next_loc[0] > len(my_map) - 1 or  next_loc[1] > len(my_map[0]) - 1:
            next_locs.append(next_loc)
    
    return next_locs

def compute_heuristics(my_map, goal):
    # Use Dijkstra to build a shortest-path tree rooted at the goal location
    open_list = []
    closed_list = dict()
    root = {'loc': goal, 'cost': 0}
    heapq.heappush(open_list, (root['cost'], goal, root))
    closed_list[goal] = root
    while len(open_list) > 0:
        (cost, loc, curr) = heapq.heappop(open_list)
        for dir in range(5):
            child_loc = move(loc, dir)
            child_cost = cost + 1
            if child_loc[0] < 0 or child_loc[0] >= len(my_map) \
               or child_loc[1] < 0 or child_loc[1] >= len(my_map[0]):
               continue
            if my_map[child_loc[0]][child_loc[1]]:
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
    path = []
    curr = goal_node
    while curr is not None:
        path.append(curr['loc'])
        curr = curr['parent']
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

def build_unsafe_intervals(soft_obstacles, hard_obstacles):

    hard_intervals = dict()

    for (vertex, times) in hard_obstacles.items():
        
        intervals = []

        prev = None
        low = None
        high = None
        
        temp_times = copy(times)
        while temp_times:
            time = heapq.heappop(temp_times)
            
            if prev is None:
                prev = time
                low = time
                high = time
                continue
            
            if prev + 1 == time:
                high = time
            else:
                intervals.append((low, high))
                prev = time
                low = time
                high = time

        hard_intervals[vertex] = intervals
    
    soft_intervals = dict()

    for (vertex, times) in soft_obstacles.items():
        
        intervals = []

        prev = None
        low = None
        high = None
        
        temp_times = copy(times)

        while temp_times:
            time = heapq.heappop(temp_times)
            
            if prev is None:
                prev = time
                low = time
                high = time
                continue
            
            if prev + 1 == time:
                high = time
            else:
                intervals.append((low, high))
                prev = time
                low = time
                high = time

        soft_intervals[vertex] = intervals

    return soft_intervals, hard_intervals

def merge_intervals(A, B):
    
    i = j = 0
    res = []
    while i < len(A) or j < len(B):
        if i==len(A):
            curr = B[j]
            j+=1
        elif j==len(B):
            curr = A[i]
            i+=1
        elif A[i][0] < B[j][0]:
            curr = A[i]
            i+=1
        else:
            curr = B[j]
            j+=1
        if res and res[-1][-1] >= curr[0]:
            res[-1][-1] = max(res[-1][-1],curr[-1])
        else:
            res.append(curr)
    
    return res

def build_safe_interval_table(locations, soft_obstacles, hard_obstacles):

    soft_unsafe_intervals, hard_unsafe_intervals = build_unsafe_intervals(soft_obstacles, hard_obstacles)

    safe_interval_table = dict()

    for v in locations:
        
        hard_intervals = []
        soft_intervals = []

        if v in hard_unsafe_intervals:
            hard_intervals = hard_unsafe_intervals[v]

        if v in soft_unsafe_intervals:
            soft_intervals = soft_unsafe_intervals[v]

        unsafe_intervals = merge_intervals(hard_intervals, soft_intervals)

        time = 0
        safe_intervals = []
        
        for (low, hi) in unsafe_intervals:
            safe_intervals.append((time, low))
            time = hi + 1
        
        safe_interval_table[v] = safe_intervals

    return safe_interval_table