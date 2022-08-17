from operator import ne
from tkinter import N
from loadscen import *
from ALNS import *
from collisionneighbourhood import *
from failureBasedNeighbourhood import *
from randomNeighborhood import *
from prioritizedPlanning import *
from LNSUtil import *


def selectNeighbour(paths, neighbourhood_kind, numNeighbourhood, width, height, instanceMap):
    neighbourhood = []
    neighbourhoodIndex_inPath = []
    if neighbourhood_kind == 0:
        # collision
        neighbourhood = collisionNeighbourhood(
            paths, numNeighbourhood, width, height, instanceMap)
    elif neighbourhood_kind == 1:
        # failure
        neighbourhood = faulureNeighbourhood(paths, numNeighbourhood)
    else:
        # random
        neighbourhood = randomNeighbourhood(paths, numNeighbourhood)

    for agent in neighbourhood:
        index = paths.index(agent)
        neighbourhoodIndex_inPath.append(index)

    return neighbourhood, neighbourhoodIndex_inPath


# replan untill collision free
def replan(paths, numNeighbourhood, width, height, instanceMap, ALNS_weight):
    # ALNS_weight = [1, 1, 1]
    # ALNS_r = 0.1

    # index0: collision, index1: failure, index2: random
    neighbourhood_kind = ALNS(ALNS_weight)
    # neighbourhood is P- in the paper (list of paths)
    neighbourhood, neighbourhoodIndex_inPath = selectNeighbour(
        paths, neighbourhood_kind, numNeighbourhood, width, height, instanceMap)

    # newNeighbourhood is P+ in the paper (list of paths)
    newNeighbourhood = prioritized_planning(
        paths, neighbourhoodIndex_inPath, instanceMap, neighbourhood)

    newPaths = paths
    for index in neighbourhoodIndex_inPath:
        # newPaths[index] = None
        newPaths[index] = newNeighbourhood[index]

    # sum of collision pair of all agents
    numCp_neighbourhood = sum(deg(paths))
    numCp_newNeighbourhood = sum(deg(newPaths))

    if (numCp_neighbourhood >= numCp_newNeighbourhood):
        return newPaths
    return paths


def LNS2(numNeighbourhood, width, height, instanceMap,):
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
                         height, instanceMap, ALNS_weight)
        numCp = sum(deg(newPath))
        ALNS_weight = updateWeight(ALNS_weight, ALNS_r, previousCP, numCp)

    return newPath


if __name__ == "__main__":
    numNeighbourhood = 2
    instanceMap, instanceStarts, instanceGoals = loadScen(
        "empty-8-8-even-1.scen", 5)
    print(instanceStarts)
    print(instanceGoals)
    path = LNS2(numNeighbourhood, 8, 8, instanceMap,
                instanceStarts, instanceGoals)
