import heapq
from Utils import *

def build_safe_interval_table():
    pass

def pop_node(open_list):
    pass

def push_node(open_list, node):
    pass

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

def sipps(my_map, start_loc, goal_loc, h_values, agent, hard_obstacle, soft_obstacle):    

    safe_interval_table = build_safe_interval_table()
    
    root = {'c_val': 0, 'loc': start_loc, 'g_val': 0, 'h_val': h_values[start_loc], 'interval': safe_interval_table[start_loc][1], 'id': 1, 'is_goal': False, 'parent': None}
    lower_bound_timestep = 0

    if hard_obstacle.has_key(goal_loc):
        lower_bound_timestep = max(hard_obstacle[goal_loc]) + 1

    open_list = []
    push_node(open_list, root)
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