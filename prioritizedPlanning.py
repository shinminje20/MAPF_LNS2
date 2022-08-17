from Utils import *
import heapq

def prioritized_planning(paths, neighbourhood, instanceMap, instanceStarts, instanceGoals):
	#randomize order of neighbourhood
    neighbourhood = priorityList(neighbourhood)

    #build vertex and edge constraints from paths
    #paths of agents in neighbourhood => soft obstacles
    #paths of agents not in neighbourhood => hard obstacles

    #build hard constraints table
    neighbourhood_set = set(neighbourhood)
    hard_obstacles = {}
    for i in range(len(paths)):
        if i not in neighbourhood_set:
            #TODO implement
            add_constraints_from_path(hard_obstacles, paths[i])

    #build heuristics table

    #execute prioritized planning
    # at each iteration, add to soft obstacles using found path
    newPaths = []

    soft_obstacles = {}
    for agent in neighbourhood:
        agentStart = instanceStarts[agent] #coordinates are in (x, y), map indexing is in [y][x]
        agentGoal = instanceGoals[agent]

        #build heuristics table
        h_values = compute_heuristics(instanceMap, agentGoal)
        agentPath = sipps(instanceMap, agentStart, agentGoal, h_values, agent, hard_obstacles, soft_obstacles)

        add_constraints_from_path(soft_obstacles, agentPath)
        newPaths.append(agentPath)

    #for i in range(len(neighbourhood)):
    #    paths[neighbourhood[i]] = newPaths[i]

    return newPaths
    #newPaths[i] corresponds to agent at neighbourhood[i]


def add_constraints_from_path(constraint_table, path):
    #add vertex constraint for time 0
    if path[0] not in constraint_table:
        constraint_table[path[0]] = []
    constraint_table[path[0]].heappush(0)

    for i in range(1, len(path)):
        #add vertex constraint
        if path[i] not in constraint_table:
            constraint_table[path[i]] = []
        constraint_table[path[i]].heappush(i)

        #add edge constraint
        if (path[i], path[i-1]) not in constraint_table:
            constraint_table[(path[i], path[i-1])] = set()
        constraint_table[(path[i], path[i-1])].add(i)

    return constraint_table


def priorityList(neighbourhood):
	PPlist = []
	while len(neighbourhood) > 0:
		index = randrange(0, len(neighbourhood))
		PPlist.append(neighbourhood.pop(index))
	return PPlist
