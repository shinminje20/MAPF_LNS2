import heapq
from Utils import *
# from LNS import *

def move(loc, dir):
    directions = [(0, -1), (1, 0), (0,0), (0, 1), (-1, 0)]
    return loc[0] + directions[dir][0], loc[1] + directions[dir][1]

def is_valid_move(next_loc):
    
    if next_loc[0] < 0 or  next_loc[1] < 0 or  next_loc[0] > len(my_map) - 1 or  next_loc[1] > len(my_map[0]) - 1:
        return False
    return True

def get_neighbors(curr_loc):
    next_locs = []
    for dir in range(5):
        next_loc = move(curr_loc, dir)
        
        if is_valid_move(curr_loc, next_loc):
            next_locs.append(next_loc)
    
    return next_locs

def get_valid_nodes(curr_loc, low, high, safe_interval_table):
    
    valid_neighbors = []

    
    neighbor_locations = get_neighbors(curr_loc)
    
    # Algorithm 2 line 2-3
    for next_loc in neighbor_locations:  

        for interval_id, interval in enumerate(safe_interval_table[next_loc]):  
            if interval[1] < low + 1 or high + 1 <= interval[0]:  #find intervals and their id that are not colliding with current_node's interval
                valid_neighbors.append((next_loc, interval_id))

     # Algorithm 2 line 4-5
    for interval_id, interval in enumerate(safe_interval_table[curr_loc]): 
        if interval[0] == high:
            valid_neighbors.append((curr_loc, interval_id))
    
    return valid_neighbors

def get_identical_nodes(node, open_list, closed_list):
    
    identical_nodes = []
    
    for open_node in open_list:
        if open_node['id'] == node['id'] and open_node['loc'] == node['loc'] and open_node['is_goal'] == node['is_goal']:
            identical_nodes.append(open_node)

    for closed_node in closed_list:
        if closed_node['id'] == node['id'] and closed_node['loc'] == node['loc'] and closed_node['is_goal'] == node['is_goal']:
            identical_nodes.append(closed_node)
    
    return identical_nodes

def insert_node(node, open_list, closed_list, h_values, soft_obstacle):
    g_val = node['parent']['g_val'] + 1
    h_val = h_values[node['loc']]
    f_val = g_val + h_val
    c_val = get_c_val(node, closed_list, soft_obstacle)
    n_low = node['interval'][0]
    n_high = node['interval'][1]

    node['g_val'] = g_val
    node['h_val'] = h_val
    node['c_val'] = c_val

    identical_nodes = get_identical_nodes(node, open_list, closed_list)

    for i_node in identical_nodes:
        i_low = i_node['interavl'][0]
        i_high = i_node['interavl'][1]
        i_c_val = i_node['c_val']
        
        if i_low <= n_low and i_c_val <= c_val:
            return
        
        elif n_low <= i_low and c_val <= i_c_val:
            #delete i_node from either open_list, closed_list 그러면 open/closed_list 를 dict 이나 다른 거로 해야대나..
            pass
        elif n_low < i_high and i_low < n_high:
            if n_low < i_low:
                n_high = i_low
            else:
                i_high = n_low
    
    heapq.heappush(open_list, (c_val, node))

def pop_node(open_list):
    _, curr = heapq.heappop(open_list)
    return curr


def expand_node(curr_node, open_list, closed_list, safe_interval_table, hard_obstacle, soft_obstacle, h_values):
    
    valid_neighbors = []
    curr_loc = curr_node['loc']
    node_low = curr_node['interval'][0]
    node_high = curr_node['interval'][1]
    
    valid_neighbors = get_valid_nodes(curr_loc, node_low, node_high, safe_interval_table)

    # Algorithm 2 line 2-3
    for (next_loc, interval_id) in valid_neighbors:
        low = safe_interval_table[next_loc][interval_id][0]
        high = safe_interval_table[next_loc][interval_id][1]
        
        if hard_obstacle.has_key([curr_loc, next_loc]):
            # MAPF_LNS2 깃헙 보고 어케 해야댈지 보자
            low = get_earlieset_arrival_time() # uncolide with hard_obstacle([curr_loc, next_loc])
        else:
            continue
        
        earliest_low = None
        earliest_low = get_earlieset_arrival_time() # uncolide with hard, soft obstacle

        if earliest_low is not None and earliest_low > low:
            
            n1 = {'c_val': 0, 'loc': next_loc, 'g_val': 0, 
                'h_val': h_values[next_loc], 'interval': (low, earliest_low), 
                'id': interval_id, 'is_goal': False, 'parent': curr_node}
            insert_node(n1, open_list, closed_list, h_values, soft_obstacle)

            n2 = {'c_val': 0, 'loc': next_loc, 'g_val': 0, 
                'h_val': h_values[next_loc], 'interval': (earliest_low, high), 
                'id': interval_id, 'is_goal': False, 'parent': curr_node}
            insert_node(n2, open_list, closed_list, h_values, soft_obstacle)
        else:
            n1 = {'c_val': 0, 'loc': next_loc, 'g_val': 0, 
                'h_val': h_values[next_loc], 'interval': (low, high), 
                'id': interval_id, 'is_goal': False, 'parent': curr_node}
            insert_node(n1, open_list, closed_list, h_values, soft_obstacle)


        


# def is_soft_constrainted(node):
#     if soft_obstacle.has_key(node['interval']):

def get_c_val(node, closed_list, soft_obstacle):
    parent_node = node['parent']
    parent_c_val = closed_list[parent_node]['c_val']
    
    cv = 1 if soft_obstacle.has_key(node['interval']) else 0

    n_low = node['interval'][0]
    n_edge = (parent_node['loc'], node['loc'])
    ce = 1 if n_edge in soft_obstacle[n_low] else 0

    return parent_c_val + cv + ce

def get_c_future(curr_loc, timestep, constraint_table):
    c_val = 0
    if len(constraint_table[curr_loc]) > timestep:
        t = timestep + 1
        while t < len(constraint_table[curr_loc]):
            c_val += len(constraint_table[curr_loc][t])
            t += 1
    
    return c_val

# Soft obstacle should look like: {location1: {"time1": ....,
#                                             "time2": [agent1, agent2, agent3,....],
#                                             "time3": [agent1, ...]
#                                              },
#                                  
#                                  location2: {
#                                               "time1": ....,
#                                               "time2": [agent1, agent2, agent3,....]
#                                             }
#                                 }

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
#                                                                 },                  
#                                              } 

def sipps(my_map, start_loc, goal_loc, h_values, agent, hard_obstacle, soft_obstacle):    

    safe_interval_table = build_safe_interval_table(my_map, soft_obstacle, hard_obstacle, goal_loc)  #my_map is avaialble paths excluding walls
    
    root = {'c_val': 0, 'loc': start_loc, 'g_val': 0, 'h_val': h_values[start_loc], 'interval': safe_interval_table[start_loc][1], 'id': 1, 'is_goal': False, 'parent': None}
    lower_bound_timestep = 0

    if hard_obstacle.has_key(goal_loc):
        lower_bound_timestep = max(hard_obstacle[goal_loc]) + 1

    open_list = []
    heapq.heappush(open_list, (0, root))

    closed_list = dict()
    # closed_list = {'c_val': , 'loc': }
    while len(open_list) > 0:
        curr = pop_node(open_list)
        if curr['is_goal']:
            return get_path(curr)
        
        if curr['loc'] == goal_loc and curr['interval'][0] >= lower_bound_timestep:
            c_future = get_c_future(curr['loc'], )
            if c_future == 0:
                return get_path(curr)
            updated_node = curr.copy()
            updated_node['c_val'] = curr['c_val'] + c_future
            # insertNode(open_list, updated_node, closed_list)
        # expandNode(curr, open_list, closed_list, safe_interval_table)
        # P <- P V {n}: closed_list += curr

    raise BaseException('No solutions')