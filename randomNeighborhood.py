import random
from LNSUtil import *


# path: lists of paths for all agents
# N : size of neighbourhoods
def randomNeighbourhood(paths, N):
    pathCopy = paths
    degList = deg(pathCopy)
    # print("degList" + str(degList))

    probList = []
    for i in range(0, len(degList), 1):
        for j in range(0, degList[i], 1):
            probList.append(i)

    neighbour = []
    i = 0
    while i < N:
        randomIndex = probList[random.randint(0, len(probList)-1)]
        if (paths[randomIndex] in neighbour):
            continue
        neighbour.append(paths[randomIndex])
        i += 1

    return neighbour