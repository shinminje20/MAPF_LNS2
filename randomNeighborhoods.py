import random

# same function in failureBasedNeighbourhoods


def compare(cord1, cord2):
    if cord1[0] == cord2[0]:
        if cord1[1] == cord2[1]:
            return True

    return False

# same function in failureBasedNeighbourhoods


def deg(path):
    degList = []
    deg = 0
    for firstPath in range(0, len(path), 1):
        for secondPath in range(0, len(path), 1):
            if(path[firstPath] == path[secondPath]):
                continue
            length = len(path[firstPath])
            if (len(path[firstPath]) > len(path[secondPath])):
                length = len(path[secondPath])
            for timestep in range(0, length, 1):
                if compare(path[firstPath][timestep], path[secondPath][timestep]):
                    deg += 1
                    break
        degList.append(deg)
        deg = 0
    return degList


# path: lists of paths for all agents
# N : size of neighbourhoods
def randomNeighbourhoods(paths, N):
    pathCopy = paths
    degList = deg(pathCopy)
    # print("degList" + str(degList))

    probList = []
    for i in range(0, len(degList), 1):
        for j in range(0, degList[i], 1):
            probList.append(i)

    # print("probList" + str(probList))

    neighbour = []
    i = 0
    while i < N:
        randomIndex = probList[random.randint(0, len(probList)-1)]
        # print("randomIndex" + str(randomIndex))
        if (paths[randomIndex] in neighbour):
            # print("continue")
            continue
        # print("added" + str(paths[randomIndex]))
        neighbour.append(paths[randomIndex])
        i += 1

    return neighbour


if __name__ == "__main__":
    print("..")
    # print(randomNeighbourhoods(path, 2))