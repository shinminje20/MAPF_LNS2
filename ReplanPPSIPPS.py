from loadscen import *
from ALNS import *
from collisionneighbourhood import *
from failureBasedNeighbourhood2 import *
from randomNeighborhood import *
from prioritizedPlanning import *
from LNSUtil import *
import time as timer

# replan untill collision free
def replan(paths, numNeighbourhood, width, height, instanceMap, instanceStarts, instanceGoals, ALNS_weight, prevCP, start):
    # select a neighbourhood construction method

    # 0: collision, 1: failure, 2: random
    neighbourhood_kind = ALNS(ALNS_weight)

    if neighbourhood_kind == 0:
        neighbourhood = collisionNeighbourhood(paths, numNeighbourhood, width, height, instanceMap)
    elif neighbourhood_kind == 1:
        neighbourhood = failureNeighbourhood(paths, numNeighbourhood)
    else:
        neighbourhood = randomNeighbourhood(paths, numNeighbourhood)

    #run modified prioritized planning to get replanned paths
    neighbourhood, newPaths = prioritized_planning(paths, neighbourhood, instanceMap, instanceStarts, instanceGoals)

    #construct new paths solution and update variables
    newPathsSolution = copy.copy(paths)
    for i in range(len(neighbourhood)):
        if newPaths[i] != None:
            newPathsSolution[neighbourhood[i]] = newPaths[i]

    numCp_newPathsSolution = sum(deg(newPathsSolution))

    ALNS_weight = updateWeight(ALNS_weight, 0.1, prevCP, numCp_newPathsSolution, neighbourhood_kind)

    if (prevCP >= numCp_newPathsSolution):
        return newPathsSolution, numCp_newPathsSolution

    return paths, prevCP


def LNS2PP(numNeighbourhood, width, height, instanceMap, instanceStarts, instanceGoals):
    paths = list(range(len(instanceGoals)))
    neighbourhood, newPaths = prioritized_planning([], list(range(len(instanceGoals))), instanceMap, instanceStarts, instanceGoals)
    for i in range(len(neighbourhood)):
        paths[neighbourhood[i]] = newPaths[i]

    numCp = 0
    numCp = sum(deg(paths))
    if (numCp == 0):
        return paths, 0

    ALNS_weight = [1, 1, 1]
    ALNS_r = 0.1

    start = timer.time()
    replan_count = 0
    while numCp != 0:
        paths, numCp = replan(paths, numNeighbourhood, width, height, instanceMap, instanceStarts, instanceGoals, ALNS_weight, numCp, start)
        replan_count += 1
            
    return paths, replan_count

# if __name__ == "__main__":
#     numNeighbourhood = 5
#     numAgent = 10
#     instanceMap, instanceStarts, instanceGoals = loadScen(
#         'room-32-32-4-even-1.scen', numAgent)
#     paths = LNS2(numNeighbourhood, len(instanceMap[0]), len(instanceMap), instanceMap,
#                 instanceStarts, instanceGoals)

#     for path in paths:
#         print(path)

