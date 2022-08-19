import random
from LNSUtil import *


# path: lists of paths for all agents
# N : size of neighbourhoods
def randomNeighbourhood(paths, N):
    pathCopy = paths
    degList = deg(pathCopy)
    #print("degList" + str(degList))

    probList = []
    for i in range(0, len(degList), 1):
        probList.append(degList[i] + 1)
    #print(probList)

    agentNumbersList = list(range(len(paths)))
    neighbourhood = set()

    while len(neighbourhood) < N:
        #print("debug")
        randomIndex = random.choices(agentNumbersList, weights = probList, k = 1)
        neighbourhood.add(randomIndex[0])

    return list(neighbourhood)
    # neighbour: list of agent number (not sorted)
