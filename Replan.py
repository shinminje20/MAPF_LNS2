from operator import ne

from ALNS import *


def ALNS():
    # from ALNS import *
    pass


def updateWeight(weight, r, cp1, cp2):
    # from ALNS import *
    pass


def collisionNeighbourhood(paths, N, width, height, instanceMap):
    # from collisionNeighbourhood import collisionNeighbourhood
    pass


def faulureNeighbourhood(pahts, N):
    # from faulureNeighbourhood import faulureNeighbourhood
    pass


def randomNeighbourhood(paths, N):
    # from randomNeighbourhood import randomNeighbourhood
    pass


def prioritized_planning(paths, neighbourhood, instanceMap, instanceAgents):
    # from prioritizedPlanning import *
    pass


def compare(cord1, cord2):
    # from LNSUtil import *
    pass


def deg(path):
    # from LNSUtil import *
    pass


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
    ''' 
        please let me know if I put correct paramter for PP 
    '''

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
    ''' 
        please revise paramter of PP for first path
    '''
    firstPath = prioritized_planning(instanceMap)
    numCp = sum(deg(firstPath))
    if (numCp == 0):
        return firstPath

    ALNS_weight = [1, 1, 1]
    ALNS_r = 0.1

    while numCp != 0:
        previousCP = numCp
        newPath = replan(firstPath, numNeighbourhood, width,
                         height, instanceMap, ALNS_weight)
        numCp = sum(deg(newPath))
        ALNS_weight = updateWeight(ALNS_weight, ALNS_r, previousCP, numCp)

    return newPath


if __name__ == "__main__":
    print("aa")
