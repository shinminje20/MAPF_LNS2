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
    #print(neighbor_locations)
    
    # Algorithm 2 line 2-3
    for next_loc in neighbor_locations:  
        #print(next_loc, my_map[next_loc[1]][next_loc[0]])
        for interval_id, interval in enumerate(safe_interval_table[next_loc]):  
            #find safe intervals that overlap with current node's interval
            if interval[0] <= high and interval[0] >= low + 1 \
                or interval[1] <= high + 1 and interval[1] > low + 1 \
                or low + 1 >= interval[0] and low + 1 < interval[1] \
                or high >= interval[0] and high < interval[1]:
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

def insert_node(node, open_list, closed_list, h_values, soft_obstacle, count_tie_break):
    g_val = node['parent']['g_val'] + 1
    h_val = h_values[node['loc']]
    f_val = g_val + h_val
    c_val = get_c_val(node, soft_obstacle)
    
    n_low = node['interval'][0]
    n_high = node['interval'][1]

    node['g_val'] = g_val
    node['h_val'] = h_val
    node['c_val'] = c_val

    identical_nodes = get_identical_nodes(node, open_list, closed_list)

    for i_node in identical_nodes:
        i_low = i_node['interval'][0]
        i_high = i_node['interval'][1]
        i_c_val = i_node['c_val']
        
        if i_low <= n_low and i_c_val <= c_val:
            return
        
        elif n_low <= i_low and c_val <= i_c_val: #node is better than previously added node
            #delete i_node from either open_list, closed_list
            closed_list = [ x for x in closed_list if x[1] == i_node ]

        elif n_low < i_high and i_low < n_high:
            if n_low < i_low:
                n_high = i_low
            else:
                i_high = n_low

    combined_heuristic = (c_val, g_val + h_val, -g_val)
    if combined_heuristic in count_tie_break:
        tie_break = count_tie_break[combined_heuristic]
        count_tie_break[combined_heuristic] -= 1
        heapq.heappush(open_list, ((combined_heuristic[0], combined_heuristic[1], combined_heuristic[2], tie_break), node))
    else:
        count_tie_break[combined_heuristic] = -1
        heapq.heappush(open_list, ((combined_heuristic[0], combined_heuristic[1], combined_heuristic[2], 0), node))

def pop_node(open_list):
    _, curr = heapq.heappop(open_list)
    return curr

def get_earlieset_arrival_time2(edge, low, high, hard_obstacle, soft_obstacle):

    new_low = low

    if edge in hard_obstacle:
        temp_times = []
        temp_times.extend(hard_obstacle[edge])
        while len(temp_times) > 0:
            time = heapq.heappop(temp_times)
            if time == new_low:
                new_low += 1

    if soft_obstacle != None:
        if edge in soft_obstacle:
            temp_times = []
            temp_times.extend(soft_obstacle[edge])
            while len(temp_times) > 0:
                time = heapq.heappop(temp_times)
                if time == new_low:
                    new_low += 1

    return new_low if new_low < high else None


def get_earlieset_arrival_time(edge, low, high, hard_obstacle, soft_obstacle):

    new_low = low

    if soft_obstacle is not None:

        temp_times = copy(hard_obstacle[edge])

        while len(temp_times) > 0:
            
            time = heapq.heappop(temp_times)

            if time == new_low:
                new_low += 1
        
        temp_times = copy(soft_obstacle[edge])

        while len(temp_times) > 0:
            time = heapq.heappop(temp_times)

            if time == new_low:
                new_low += 1

    else:
        temp_times = copy(hard_obstacle[edge])

        while len(temp_times) > 0:
            time = heapq.heappop(temp_times)

            if time == new_low:
                new_low += 1

    return new_low if new_low < high else None

def expand_node(my_map, curr_node, open_list, closed_list, safe_interval_table, hard_obstacle, soft_obstacle, h_values, count_tie_break):
    valid_neighbors = []
    curr_loc = curr_node['loc']
    node_low = curr_node['interval'][0]
    node_high = curr_node['interval'][1]
    
    valid_neighbors = get_valid_nodes(my_map, curr_loc, node_low, node_high, safe_interval_table)
    #print(valid_neighbors)
    # Algorithm 2 line 2-3
    for (next_loc, interval_id) in valid_neighbors:
        low = safe_interval_table[next_loc][interval_id][0]
        high = safe_interval_table[next_loc][interval_id][1]
        
        if (curr_loc, next_loc) in hard_obstacle:
            
            low = get_earlieset_arrival_time2((curr_loc, next_loc), low, high, hard_obstacle, None) # uncolide with hard_obstacle([curr_loc, next_loc])

            if low is None:
                continue
        
        earliest_low = get_earlieset_arrival_time2((curr_loc, next_loc), low, high, hard_obstacle, soft_obstacle) # uncolide with hard, soft obstacle

        if earliest_low is not None and earliest_low > low:
            
            n1 = {'c_val': 0, 'loc': next_loc, 'g_val': 0, 
                'h_val': h_values[next_loc], 'interval': (low, earliest_low), 
                'id': interval_id, 'is_goal': False, 'parent': curr_node}
            insert_node(n1, open_list, closed_list, h_values, soft_obstacle, count_tie_break)

            n2 = {'c_val': 0, 'loc': next_loc, 'g_val': 0, 
                'h_val': h_values[next_loc], 'interval': (earliest_low, high), 
                'id': interval_id, 'is_goal': False, 'parent': curr_node}
            insert_node(n2, open_list, closed_list, h_values, soft_obstacle, count_tie_break)
        else:
            n1 = {'c_val': 0, 'loc': next_loc, 'g_val': 0, 
                'h_val': h_values[next_loc], 'interval': (low, high), 
                'id': interval_id, 'is_goal': False, 'parent': curr_node}
            insert_node(n1, open_list, closed_list, h_values, soft_obstacle, count_tie_break)

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

def get_c_val(node, soft_obstacle):
    parent_node = node['parent']
    parent_c_val = parent_node['c_val']
    node_interval = node['interval']
    node_loc = node['loc']
    cv = 1 if is_contain_obstacle(node_loc, node_interval, soft_obstacle) else 0

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
    #print(safe_interval_table)

    temp1 = h_values[start_loc]
    temp2 = safe_interval_table[start_loc][0]

    root = {'c_val': 0, 'loc': start_loc, 'g_val': 0, 'h_val': h_values[start_loc], 'interval': safe_interval_table[start_loc][0], 'id': 1, 'is_goal': False, 'parent': None}
    lower_bound_timestep = 0

    if goal_loc in hard_obstacle:
        lower_bound_timestep = max(hard_obstacle[goal_loc]) + 1

    open_list = []
    visited_list = {}
    count_tie_break = {}
    count_tie_break[(0, 0, 0)] = -1 #c_val, g_val
    heapq.heappush(open_list, ((0, 0, 0, 0), root))
    visited_list[(root['loc'], root['id'], root['is_goal'])] = root

    closed_list = []
    count = 0
    while len(open_list) > 0:
        curr = pop_node(open_list)
        count += 1
        if curr['is_goal']:
            print(count)
            return get_path(curr)

        if curr['loc'] == goal_loc and curr['interval'][0] >= lower_bound_timestep:
            c_future = get_c_future(curr['loc'], soft_obstacle, curr['interval'][0])
            
            if c_future == 0:
                print(count)
                return get_path(curr)

            updated_node = curr.copy()
            updated_node['is_goal'] = True
            updated_node['c_val'] = curr['c_val'] + c_future
            insert_node(updated_node, open_list, closed_list, h_values, soft_obstacle, count_tie_break)



        expand_node(my_map, curr, open_list, closed_list, safe_interval_table, hard_obstacle, soft_obstacle, h_values, count_tie_break)

        combined_heuristic = (curr['c_val'], curr['g_val'] + curr['h_val'], -curr['g_val'])
        if combined_heuristic in count_tie_break:
            tie_break = count_tie_break[combined_heuristic]
            count_tie_break[combined_heuristic] -= 1
            heapq.heappush(closed_list, ((combined_heuristic[0], combined_heuristic[1], combined_heuristic[2], tie_break), curr))
        else:
            count_tie_break[(curr['c_val'], curr['g_val'])] = -1
            heapq.heappush(closed_list, ((combined_heuristic[0], combined_heuristic[1], combined_heuristic[2], 0), curr))
        
        

    # If there is no solution, return None to track of agents who does not have solutions when finding initial paths
    print("none")
    return None

#SIPPS needs to compare based on f(n), and take the solution with lowest c_val?
