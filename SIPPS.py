import heapq
from Utils import *
# from LNS import *



# def is_valid_move(next_loc):
    
#     if next_loc[0] < 0 or  next_loc[1] < 0 or  next_loc[0] > len(my_map) - 1 or  next_loc[1] > len(my_map[0]) - 1:
#         return False
#     return True

def get_valid_nodes(my_map, curr_loc, low, high, safe_interval_table):
    
    valid_neighbors = []

    
    neighbor_locations = get_neighbors(curr_loc, my_map)
    
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
    
    for (_, open_node) in open_list:
        if open_node['id'] == node['id'] and open_node['loc'] == node['loc'] and open_node['is_goal'] == node['is_goal']:
            identical_nodes.append(open_node)

    for (_, closed_node) in closed_list:
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
            #delete i_node from either open_list, closed_list
            closed_list = [ x for x in closed_list if x[1] == i_node ]

        elif n_low < i_high and i_low < n_high:
            if n_low < i_low:
                n_high = i_low
            else:
                i_high = n_low
    
    heapq.heappush(open_list, (c_val, node))

def pop_node(open_list):
    _, curr = heapq.heappop(open_list)
    return curr

def get_earlieset_arrival_time(edge, low, high, hard_obstacle, soft_obstacle):

    new_low = low

    if soft_obstacle is not None:

        temp_times = copy(hard_obstacle[edge])

        while temp_times:
            
            time = heapq.heappop(temp_times)

            if time == new_low:
                new_low += 1
        
        temp_times = copy(soft_obstacle[edge])

        while temp_times:
            
            time = heapq.heappop(temp_times)

            if time == new_low:
                new_low += 1

    else:
        temp_times = copy(hard_obstacle[edge])

        while temp_times:
            
            time = heapq.heappop(temp_times)

            if time == new_low:
                new_low += 1

    return new_low if new_low < high else None

def expand_node(my_map, curr_node, open_list, closed_list, safe_interval_table, hard_obstacle, soft_obstacle, h_values):
    
    valid_neighbors = []
    curr_loc = curr_node['loc']
    node_low = curr_node['interval'][0]
    node_high = curr_node['interval'][1]
    
    valid_neighbors = get_valid_nodes(my_map, curr_loc, node_low, node_high, safe_interval_table)

    # Algorithm 2 line 2-3
    for (next_loc, interval_id) in valid_neighbors:
        low = safe_interval_table[next_loc][interval_id][0]
        high = safe_interval_table[next_loc][interval_id][1]
        
        if hard_obstacle.has_key((curr_loc, next_loc)):
            
            low = get_earlieset_arrival_time((curr_loc, next_loc), low, high, hard_obstacle, None) # uncolide with hard_obstacle([curr_loc, next_loc])

            if low is None:
                continue
        
        earliest_low = get_earlieset_arrival_time((curr_loc, next_loc), low, high, hard_obstacle, soft_obstacle) # uncolide with hard, soft obstacle

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

def is_contain_obstacle(node_loc, interval, soft_obstacle):
    
    if node_loc in soft_obstacle:
        temp_times = copy(soft_obstacle[node_loc])

        while temp_times:
            time = heapq.heappop(temp_times)
            if interval[0] <= time and time < interval[1]:
                return True
    
    return False

def is_contain_edge(parent_loc, node_loc, n_low, soft_obstacle):

    if (parent_loc, node_loc) in soft_obstacle:

        temp_times = copy(soft_obstacle[(parent_loc, node_loc)])

        while temp_times:
            time = heapq.heappop(temp_times)
            if time == n_low:
                return True
    
    return False

def get_c_val(node, closed_list, soft_obstacle):
    parent_node = node['parent']
    parent_c_val = parent_node['c_val']
    node_interval = node['interval']
    node_loc = node['loc']
    cv = 1 if is_contain_obstacle(node_loc, node_interval, soft_obstacle) else 0

    n_low = node['interval'][0]
    n_edge = (parent_node['loc'], node['loc'])
    ce = 1 if n_edge in is_contain_edge(parent_node['loc'], node_loc, node_interval[0], soft_obstacle) else 0

    return parent_c_val + cv + ce

def get_c_future(curr_loc, timestep, constraint_table):
    c_val = 0
    if len(constraint_table[curr_loc]) > timestep:
        t = timestep + 1
        while t < len(constraint_table[curr_loc]):
            c_val += len(constraint_table[curr_loc][t])
            t += 1
    
    return c_val

def sipps(my_map, start_loc, goal_loc, h_values, hard_obstacle, soft_obstacle):    

    safe_interval_table = build_safe_interval_table(my_map, soft_obstacle, hard_obstacle)  #my_map is avaialble paths excluding walls

    root = {'c_val': 0, 'loc': start_loc, 'g_val': 0, 'h_val': h_values[start_loc], 'interval': safe_interval_table[start_loc][0], 'id': 1, 'is_goal': False, 'parent': None}
    lower_bound_timestep = 0

    if hard_obstacle.has_key(goal_loc):
        lower_bound_timestep = max(hard_obstacle[goal_loc]) + 1

    open_list = []
    heapq.heappush(open_list, (0, root))

    closed_list = []

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
            insert_node(updated_node, open_list, closed_list, h_values, soft_obstacle)

        expand_node(my_map, curr, open_list, closed_list, safe_interval_table, hard_obstacle, soft_obstacle, h_values)

        heapq.heappush(closed_list, (curr['c_val'], curr))

    # If there is no solution, return None to track of agents who does not have solutions when finding initial paths
    return None

