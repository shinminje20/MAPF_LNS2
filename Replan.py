from operator import ne
from tkinter import N
from loadscen import *
from ALNS import *
from collisionneighbourhood import *
from failureBasedNeighbourhood import *
from randomNeighborhood import *
from prioritizedPlanning import *
from LNSUtil import *


def selectNeighbour(paths, neighbourhood_method, numNeighbourhood, width, height, instanceMap):
    neighbourhood = []
    if neighbourhood_method == 0:
        # collision
        neighbourhood = collisionNeighbourhood(
            paths, numNeighbourhood, width, height, instanceMap)
    elif neighbourhood_method == 1:
        # failure
        neighbourhood = failureNeighbourhood(paths, numNeighbourhood)
    else:
        # random
        neighbourhood = randomNeighbourhood(paths, numNeighbourhood)

    return neighbourhood


# replan untill collision free
def replan(paths, numNeighbourhood, width, height, instanceMap, instanceStarts, instanceGoals, ALNS_weight):
    # ALNS_weight = [1, 1, 1]
    # ALNS_r = 0.1

    # index0: collision, index1: failure, index2: random
    neighbourhood_kind = ALNS(ALNS_weight)
    # neighbourhood is P- in the paper (list of paths)
    neighbourhood = selectNeighbour(
        paths, neighbourhood_kind, numNeighbourhood, width, height, instanceMap)

    # newNeighbourhood is P+ in the paper (list of paths)
    newNeighbourhood = prioritized_planning(
        paths, neighbourhood, instanceMap, instanceStarts, instanceGoals)

    newPaths = paths
    for index in neighbourhood:
        # newPaths[index] = None
        newPaths[index] = newNeighbourhood[index]

    # sum of collision pair of all agents
    numCp_neighbourhood = sum(deg(paths))
    numCp_newNeighbourhood = sum(deg(newPaths))

    if (numCp_neighbourhood >= numCp_newNeighbourhood):
        return newPaths
    return paths


def LNS2(numNeighbourhood, width, height, instanceMap, instanceStarts, instanceGoals):
    newPath = prioritized_planning([], list(
        range(0, len(instanceGoals))), instanceMap, instanceStarts, instanceGoals)

    numCp = sum(deg(newPath))
    if (numCp == 0):
        return newPath

    ALNS_weight = [1, 1, 1]
    ALNS_r = 0.1

    while numCp != 0:
        previousCP = numCp
        newPath = replan(newPath, numNeighbourhood, width,
                         height, instanceMap, instanceStarts, instanceGoals, ALNS_weight)
        numCp = sum(deg(newPath))
        ALNS_weight = updateWeight(ALNS_weight, ALNS_r, previousCP, numCp)

    return newPath

if __name__ == "__main__":
    numNeighbourhood = 5
    numAgent = 10
    # instanceMap, instanceStarts, instanceGoals = loadScen(
    #     "empty-8-8-even-1.scen", numAgent)
    instanceMap, instanceStarts, instanceGoals = loadScen(
        'room-64-64-16-even-1.scen', numAgent)
    paths = LNS2(numNeighbourhood, 64, 64, instanceMap,
                instanceStarts, instanceGoals)

    for path in paths:
        print(path)

