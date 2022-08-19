from operator import ne
from tkinter import N
from loadscen import *
from ALNS import *
from collisionneighbourhood import *
from failureBasedNeighbourhood2 import *
from randomNeighborhood import *
from prioritizedPlanning import *
from LNSUtil import *



def selectNeighbour(paths, neighbourhood_method, numNeighbourhood, width, height, instanceMap):
    neighbourhood = []
    method = 0
    if neighbourhood_method == 0:
        # collision
        #print("\ncollisionNeighbourhood")
        method = 0
        neighbourhood = collisionNeighbourhood(
            paths, numNeighbourhood, width, height, instanceMap)
    elif neighbourhood_method == 1:
        # failure
        #print("\nfailureNeighbourhood")
        method = 1
        neighbourhood = failureNeighbourhood(paths, numNeighbourhood)
    else:
        # random
        #print("\nrandomNeighbourhood")
        method = 2
        neighbourhood = randomNeighbourhood(paths, numNeighbourhood)

    return neighbourhood, method


# replan untill collision free
def replan(paths, numNeighbourhood, width, height, instanceMap, instanceStarts, instanceGoals, ALNS_weight, prevCP):
    # ALNS_weight = [1, 1, 1]
    ALNS_r = 0.1

    # index0: collision, index1: failure, index2: random
    neighbourhood_kind = ALNS(ALNS_weight)
    # neighbourhood is P- in the paper (list of paths)
    neighbourhood, method = selectNeighbour(
        paths, neighbourhood_kind, numNeighbourhood, width, height, instanceMap)

    # newNeighbourhood is P+ in the paper (list of paths)
    neighbourhood, newPaths = prioritized_planning(
        paths, neighbourhood, instanceMap, instanceStarts, instanceGoals)

    #print(neighbourhood)
    #print(newPaths)

    newPathsSolution = copy.copy(paths)

    for i in range(len(neighbourhood)):
        if newPaths[i] != None:
            newPathsSolution[neighbourhood[i]] = newPaths[i]

    # sum of collision pair of all agents
    numCp_newPathsSolution = sum(deg(newPathsSolution))

    #print(degID(newPathsSolution))

    ALNS_weight = updateWeight(ALNS_weight, ALNS_r, prevCP, numCp_newPathsSolution, method)


    if (prevCP >= numCp_newPathsSolution):
        #print("new plan", numCp_newPathsSolution)
        return newPathsSolution, numCp_newPathsSolution

    #print("old plan", prevCP)
    return paths, prevCP


def LNS2(numNeighbourhood, width, height, instanceMap, instanceStarts, instanceGoals):
    paths = list(range(len(instanceGoals)))
    neighbourhood, newPaths = prioritized_planning([], list(range(len(instanceGoals))), instanceMap, instanceStarts, instanceGoals)
    for i in range(len(neighbourhood)):
        paths[neighbourhood[i]] = newPaths[i]

    '''
    pathCosts = 0
    for i in range(len(newPath)):
        #print("agent", i, newPath[i])
        pathCosts += len(newPath[i])
    #print(pathCosts)
    #print(degID(newPath))
    '''

    numCp = 0
    numCp = sum(deg(paths))
    if (numCp == 0):
        return paths

    ALNS_weight = [1, 1, 1]
    ALNS_r = 0.1

    while numCp != 0:
        paths, numCp = replan(paths, numNeighbourhood, width,
                         height, instanceMap, instanceStarts, instanceGoals, ALNS_weight, numCp)
        #numCp = sum(deg(newPath))
        #ALNS_weight = updateWeight(ALNS_weight, ALNS_r, previousCP, numCp)

    return paths

if __name__ == "__main__":
    numNeighbourhood = 5
    numAgent = 10
    # instanceMap, instanceStarts, instanceGoals = loadScen(
    #     "empty-8-8-even-1.scen", numAgent)
    instanceMap, instanceStarts, instanceGoals = loadScen(
        'room-32-32-4-even-1.scen', numAgent)
    paths = LNS2(numNeighbourhood, len(instanceMap[0]), len(instanceMap), instanceMap,
                instanceStarts, instanceGoals)

    for path in paths:
        print(path)

