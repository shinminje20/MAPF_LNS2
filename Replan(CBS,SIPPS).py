from operator import ne
from tkinter import N
from turtle import width
from cbs import *
from ALNS import *
from collisionneighbourhood import *
from failureBasedNeighbourhood2 import *
from randomNeighborhood import *
from LNSUtil import *
from pathlib import Path
from SIPPS2 import *


def import_mapf_instance(filename):
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")
    f = open(filename, 'r')
    # first line: #rows #columns
    line = f.readline()
    rows, columns = [int(x) for x in line.split(' ')]
    rows = int(rows)
    columns = int(columns)
    # #rows lines with the map
    my_map = []
    for r in range(rows):
        line = f.readline()
        my_map.append([])
        for cell in line:
            if cell == '@':
                my_map[-1].append(True)
            elif cell == '.':
                my_map[-1].append(False)
    # #agents
    line = f.readline()
    num_agents = int(line)
    # #agents lines with the start/goal positions
    starts = []
    goals = []
    for a in range(num_agents):
        line = f.readline()
        sx, sy, gx, gy = [int(x) for x in line.split(' ')]
        starts.append((sx, sy))
        goals.append((gx, gy))
    f.close()
    return my_map, starts, goals


def selectNeighbour(paths, neighbourhood_kind, numNeighbourhood, width, height, instanceMap):
    neighbourhood = []
    if neighbourhood_kind == 0:
        print("collision satrt")
        # collision
        neighbourhood = collisionNeighbourhood(
            paths, numNeighbourhood, width, height, instanceMap)
        print("collision end")
    elif neighbourhood_kind == 1:
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

    starts = []
    for index in neighbourhood:
        starts.append(instanceStarts[index])

    goals = []
    for index in neighbourhood:
        starts.append(instanceGoals[index])

    cbs = CBSSolver(instanceMap, starts, goals, paths, neighbourhood)
    newNeighbourhood = cbs.find_solution(False)

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

    cbs = CBSSolver(instanceMap, instanceStarts, instanceGoals,
                    [], list(range(len(instanceGoals))))
    newPath = cbs.find_solution(False)

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
    instanceMap, instanceStarts, instanceGoals = import_mapf_instance(
        "test_49.txt")
    width = len(instanceMap)
    height = len(instanceMap[0])
    paths = LNS2(numNeighbourhood, width, height, instanceMap,
                 instanceStarts, instanceGoals)
    print("solution")
    for path in paths:
        print(path)
