import heapq
from Utils import *

class Node()

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
    ce = parent_node['loc']

    return parent_c_val + cv + ce

def sipps(my_map, start_loc, goal_loc, h_values, agent, hard_obstacle, soft_obstacle):    

    safe_interval_table = build_safe_interval_table()
    
    root = {'c_val': 0, 'loc': start_loc, 'g_val': 0, 'h_val': h_values[start_loc], 'interval': safe_interval_table[start_loc][1], 'id': 1, 'is_goal': False, 'parent': None}
    T = 0

    if hard_obstacle.has_key(goal_loc):
        T = max(hard_obstacle[goal_loc]) + 1

    open_list = []
    push_node(open_list, root)
    closed_list = dict()
    # closed_list = {'c_val': , 'loc': }
    while len(open_list) > 0:
        curr = pop_node(open_list)
        if curr['is_goal']:
            return get_path(curr)
        
        if curr['loc'] == goal_loc and curr['interval'][0] >= T:

