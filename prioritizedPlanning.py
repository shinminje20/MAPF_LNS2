from Utils import *

def prioritized_planning(paths, neighbourhood, instanceMap, instanceAgents):
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
        agentInfo = instanceAgents[agent]
        agentStart = (agentInfo[0], agentInfo[1]) #coordinates are in (x, y), map indexing is in [y][x]
        agentGoal = (agentInfo[2], agentInfo[3])

        #build heuristics table
        h_values = compute_heuristics(instanceMap, agentGoal)
        agentPath = sipps(instanceMap, agentStart, agentGoal, h_values, agent, hard_obstacles, soft_obstacles)

        add_constraints_from_path(soft_obstacles, agentPath)
        newPaths.append(agentPath)

    for i in range(len(neighbourhood)):
        paths[neighbourhood[i]] = newPaths[i]

    return paths


def add_constraints_from_path(constraint_table, path):
	#TODO implement
    pass


def priorityList(neighbourhood):
	PPlist = []
	while len(neighbourhood) > 0:
		index = randrange(0, len(neighbourhood))
		PPlist.append(neighbourhood.pop(index))
	return PPlist
