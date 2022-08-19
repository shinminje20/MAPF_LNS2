import heapq
from Utils2 import *
# from LNS import *




'''
structure interval table with seperate empty/soft intervals and refactor codebase

- moving from curr_loc to next_loc within time window of max(lows) min(highs)
- determine if dominant empty or early soft + later empty
- insert nodes (1 or 2 split)
    - between low of current node and low of next node, count soft obstacle collisions
        - dominant empty: +0 collisions
        - early soft: +1 collisions
        - later empty: count collisions in interval table
        also, count soft-edge collisions






'''








def get_valid_nodes(my_map, curr_loc, low, high, safe_interval_table):
    
    valid_neighbors = []

    neighbor_locations = get_neighbors(curr_loc, my_map)
    
    for next_loc in neighbor_locations:
        #print(next_loc, my_map[next_loc[1]][next_loc[0]])
        for i in range(len(safe_interval_table[next_loc])):
            interval = safe_interval_table[next_loc][i]
        #for interval_id, interval in enumerate(safe_interval_table[next_loc]):  
            #find safe intervals that overlap with current node's interval
            #can reduce conditions: if low+1 in interval or high in interval
            if interval[0] <= high and interval[0] >= low + 1 \
                or interval[1] <= high + 1 and interval[1] > low + 1 \
                or low + 1 >= interval[0] and low + 1 < interval[1] \
                or high >= interval[0] and high < interval[1]:
                valid_neighbors.append((next_loc, i))
    
    return valid_neighbors

def insert_node(node, open_list, key_heap, visited_list, h_values, soft_obstacle, count_tie_break):
    g_val = node['parent']['g_val'] + (node['interval'][0] - node['parent']['interval'][0])
    node['g_val'] = g_val
    h_val = h_values[node['loc']]
    f_val = g_val + h_val
    c_val = node['c_val']
    
    n_low = node['interval'][0]
    n_high = node['interval'][1]

    node_sig = (node['loc'], node['id'], node['is_goal'])
    node_sig_2 = (c_val, n_low, n_high)

    identical_nodes = []

    if node_sig in visited_list:
        identical_nodes = list(visited_list[node_sig].values())

    for i_node in identical_nodes:
        i_low = i_node[0]['interval'][0]
        i_high = i_node[0]['interval'][1]
        i_c_val = i_node[0]['c_val']
        i_node_sig_2 = (i_c_val, i_low, i_high)
        
        if i_low <= n_low and i_c_val <= c_val: #previous node is dominant, don't insert node
            return
        
        elif n_low <= i_low and c_val <= i_c_val: #node is better than previously added node, remove i_node
            if i_node[1] in open_list:
                open_list.pop(i_node[1])
            visited_list[node_sig].pop(i_node_sig_2)

        elif n_low < i_high and i_low < n_high: #node has different complementary times, update to disjoint intervals and add
            if n_low < i_low:
                n_high = i_low
            else:
                updated_i_node = copy.copy(visited_list[node_sig][i_node_sig_2][0])
                updated_i_node['interval'] = (updated_i_node['interval'][0], n_low)
                #visited_list[node_sig][i_node_sig_2][0] = updated_i_node

    combined_heuristic = (c_val, g_val + h_val, -g_val)
    tie_break = 0
    if combined_heuristic in count_tie_break:
        tie_break = count_tie_break[combined_heuristic]
        count_tie_break[combined_heuristic] -= 1
    else:
        tie_break = 0
        count_tie_break[combined_heuristic] = -1
    key = (combined_heuristic[0], combined_heuristic[1], combined_heuristic[2], tie_break)

    heapq.heappush(key_heap, key)
    open_list[key] = node
    if node_sig not in visited_list:
        visited_list[node_sig] = {}
    if node_sig_2 not in visited_list[node_sig]:
        visited_list[node_sig][node_sig_2] = {}    
    visited_list[node_sig][node_sig_2] = (node, key)


    #heapq.heappush(open_list, ((combined_heuristic[0], combined_heuristic[1], combined_heuristic[2], tie_break), node))

    #put in visited list too

def pop_node(open_list):
    _, curr = heapq.heappop(open_list)
    return curr

def get_earliest_arrival_time(curr_loc, edge, low, high_limit, hard_obstacle, soft_obstacle):

    hard_edge_times = set()
    soft_vertex_times = set()
    soft_edge_times = set()

    if hard_obstacle != None and edge in hard_obstacle:
        hard_edge_times = hard_obstacle[edge]

    if soft_obstacle != None:
        if curr_loc in soft_obstacle:
            soft_vertex_times = soft_obstacle[curr_loc]
        if edge in soft_obstacle:
            soft_edge_times = soft_obstacle[edge]

    new_low = low
    while new_low < high_limit:
        if new_low in hard_edge_times or new_low in soft_vertex_times or new_low in soft_edge_times:
            new_low += 1
        else:
            return new_low
    return new_low

def hard_edge_check(edge, low, high_limit, hard_obstacle):
    hard_edge_times = set()
    if hard_obstacle != None and edge in hard_obstacle:
        hard_edge_times = hard_obstacle[edge]

    new_low = low
    while new_low < high_limit:
        if new_low in hard_edge_times:
            new_low += 1
        else:
            return new_low
    return None

def expand_node(my_map, curr_node, open_list, key_heap, visited_list, safe_interval_table, hard_obstacle, soft_obstacle, h_values, count_tie_break):
    valid_neighbors = []
    curr_loc = curr_node['loc']
    node_low = curr_node['interval'][0]
    node_high = curr_node['interval'][1]
    
    valid_neighbors = get_valid_nodes(my_map, curr_loc, node_low, node_high, safe_interval_table)
    print("valid_neighbors", valid_neighbors)
    # Algorithm 2 line 2-3
    for (next_loc, interval_id) in valid_neighbors:
        low = safe_interval_table[next_loc][interval_id][0]
        high = safe_interval_table[next_loc][interval_id][1]

        high_limit = min(node_high, high)
        low_limit = max(node_low+1, low)

        earliest_low = get_earliest_arrival_time(curr_loc, (curr_loc, next_loc), low_limit, high_limit, hard_obstacle, soft_obstacle) # uncolide with hard, soft obstacle

        if earliest_low > low_limit and earliest_low < high_limit is not None and earliest_low > low:
            #print("neighbour", next_loc, interval_id, "intervals", low, earliest_low, high)

            n1 = {'c_val': curr_node['c_val'] + 1, 'loc': next_loc, 'g_val': 0, 
                'h_val': h_values[next_loc], 'interval': (low_limit, earliest_low), 
                'id': interval_id, 'is_goal': False, 'parent': curr_node}
            insert_node(n1, open_list, key_heap, visited_list, h_values, soft_obstacle, count_tie_break)

            n2 = {'c_val': curr_node['c_val'], 'loc': next_loc, 'g_val': 0, 
                'h_val': h_values[next_loc], 'interval': (earliest_low, high), 
                'id': interval_id, 'is_goal': False, 'parent': curr_node}
            insert_node(n2, open_list, key_heap, visited_list, h_values, soft_obstacle, count_tie_break)
        else:
            #print("neighbour", next_loc, interval_id, "interval", low, high)

            c_val = curr_node['c_val']
            earliest_soft_low = low_limit
            if earliest_low == high_limit: #interval is all soft
                earliest_soft_low = hard_edge_check((curr_loc, next_loc), low_limit, high_limit, hard_obstacle)
                if earliest_soft_low == None:
                    continue
                c_val += 1
            n1 = {'c_val': c_val, 'loc': next_loc, 'g_val': 0, 
                'h_val': h_values[next_loc], 'interval': (earliest_soft_low, high), 
                'id': interval_id, 'is_goal': False, 'parent': curr_node}
            insert_node(n1, open_list, key_heap, visited_list, h_values, soft_obstacle, count_tie_break)

def is_contain_obstacle(node_loc, interval, soft_obstacle):
    
    if node_loc in soft_obstacle:
        temp_times = copy.copy(soft_obstacle[node_loc])

        while len(temp_times) > 0:
            time = heapq.heappop(temp_times)
            if interval[0] <= time and time < interval[1]:
                return True
    
    return False

def is_contain_edge(parent_loc, node_loc, n_low, soft_obstacle):

    if (parent_loc, node_loc) in soft_obstacle:

        temp_times = copy.copy(soft_obstacle[(parent_loc, node_loc)])

        while len(temp_times) > 0:
            time = heapq.heappop(temp_times)
            if time == n_low:
                return True
    
    return False

def get_c_val(node, soft_obstacle, hard_obstacle):
    parent_node = node['parent']
    parent_c_val = 0
    if parent_node != None:
        parent_c_val = parent_node['c_val']

    node_interval = node['interval']
    node_loc = node['loc']
    cv = 1 if is_contain_obstacle(node_loc, node_interval, soft_obstacle) else 0

    ce = 0
    if parent_node != None:
        n_low = node['interval'][0]
        n_edge = (parent_node['loc'], node['loc'])
        ce = 1 if is_contain_edge(parent_node['loc'], node_loc, node_interval[0], soft_obstacle) else 0

    return parent_c_val + cv + ce

def get_c_future(curr_loc, soft_obstacle, n_low):
    c_future = 0
    
    if curr_loc in soft_obstacle:
        temp_times = copy.copy(soft_obstacle[curr_loc])
        
        while len(temp_times) > 0:
            time = heapq.heappop(temp_times)
            if time > n_low:
                c_future = len(temp_times) + 1    # Since all of rest of times in temp_times will be greater than n_low from now, 
                break                             # thus len(temp_times) + 1 (+1 for counting popped time just now).
    
    return c_future

def sipps(my_map, start_loc, goal_loc, h_values, hard_obstacle, soft_obstacle):    

    safe_interval_table = build_safe_interval_table(my_map, hard_obstacle)  #my_map is avaialble paths excluding walls
    print("hard_obstacle", hard_obstacle)
    print("soft_obstacle", soft_obstacle)
    print("safe_interval_table", safe_interval_table)

    temp1 = h_values[start_loc]
    temp2 = safe_interval_table[start_loc][0]

    root = {'c_val': 0, 'loc': start_loc, 'g_val': 0, 'h_val': h_values[start_loc], 'interval': safe_interval_table[start_loc][0], 'id': 1, 'is_goal': False, 'parent': None}
    lower_bound_timestep = 0

    if goal_loc in hard_obstacle:
        lower_bound_timestep = max(hard_obstacle[goal_loc]) + 1

    key_heap = []
    count_tie_break = {}
    count_tie_break[(0, 0, 0)] = -1 #c_val, g_val    
    open_list = {}
    heapq.heappush(key_heap, (0, 0, 0, 0))
    open_list[(0, 0, 0, 0)] = root
    visited_list = {}
    visited_list[(root['loc'], root['id'], root['is_goal'])] = {}
    visited_list[(root['loc'], root['id'], root['is_goal'])][(root['c_val'], root['interval'][0], root['interval'][1])] = (root, (0, 0, 0, 0))

    closed_list = []
    count = 0
    while len(key_heap) > 0:
        currKey = heapq.heappop(key_heap)
        #print(key_heap)
        if currKey not in open_list:
            continue

        curr = open_list[currKey]
        count += 1
        print(curr['c_val'], curr['loc'], curr['interval'][0])

        if curr['is_goal']:
            print("count", count)
            return get_path(curr)

        if curr['loc'] == goal_loc and curr['interval'][0] >= lower_bound_timestep:
            c_future = get_c_future(curr['loc'], soft_obstacle, curr['interval'][0])
            
            if c_future == 0:
                print("count", count)
                return get_path(curr)

            updated_node = curr.copy()
            updated_node['is_goal'] = True
            updated_node['c_val'] = curr['c_val'] + c_future
            insert_node(updated_node, open_list, key_heap, visited_list, h_values, soft_obstacle, count_tie_break)

        expand_node(my_map, curr, open_list, key_heap, visited_list, safe_interval_table, hard_obstacle, soft_obstacle, h_values, count_tie_break) 
        

    # If there is no solution, return None to track of agents who does not have solutions when finding initial paths
    print("none", count)
    return None

#SIPPS needs to compare based on f(n), and take the solution with lowest c_val?
