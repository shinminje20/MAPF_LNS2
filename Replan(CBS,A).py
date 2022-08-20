from operator import ne
from tkinter import N
from turtle import width
from loadscen import *
from cbs import *
from ALNS import *
from collisionneighbourhood import *
from failureBasedNeighbourhood2 import *
from randomNeighborhood import *
from LNSUtil import *
from pathlib import Path
from single_agent_planner import a_star
import copy


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


def selectNeighbour(paths, neighbourhood_method, numNeighbourhood, width, height, instanceMap):
    neighbourhood = []
    method = 0
    if neighbourhood_method == 0:
        # collision
        # print("\ncollisionNeighbourhood")
        method = 0
        neighbourhood = collisionNeighbourhood(
            paths, numNeighbourhood, width, height, instanceMap)
    elif neighbourhood_method == 1:
        # failure
        # print("\nfailureNeighbourhood")
        method = 1
        neighbourhood = failureNeighbourhood(paths, numNeighbourhood)
    else:
        # random
        # print("\nrandomNeighbourhood")
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
    starts = []
    for index in neighbourhood:
        starts.append(instanceStarts[index])

    goals = []
    for index in neighbourhood:
        goals.append(instanceGoals[index])

    cbs = CBSSolver(instanceMap, starts, goals)
    newNeighbourhood = cbs.find_solution(False)

    # print(neighbourhood)
    # print(newPaths)

    newPathsSolution = copy.copy(paths)

    for i in range(len(neighbourhood)):
        if newNeighbourhood[i] != None:
            newPathsSolution[neighbourhood[i]] = newNeighbourhood[i]

    # sum of collision pair of all agents
    numCp_newPathsSolution = sum(deg(newPathsSolution))

    # print(degID(newPathsSolution))

    ALNS_weight = updateWeight(
        ALNS_weight, ALNS_r, prevCP, numCp_newPathsSolution, method)

    if (prevCP >= numCp_newPathsSolution):
        #print("new plan", numCp_newPathsSolution)
        return newPathsSolution, numCp_newPathsSolution

    #print("old plan", prevCP)
    return paths, prevCP


def LNS2(numNeighbourhood, width, height, instanceMap, instanceStarts, instanceGoals):
    paths = list(range(len(instanceGoals)))

    h_values = []
    for goal in instanceGoals:
        h_values.append(compute_heuristics(instanceMap, goal))

    newPaths = []
    for i in range(len(instanceGoals)):
        path = a_star(instanceMap, instanceStarts[i], instanceGoals[i], h_values[i], range(
            len(instanceGoals)), [])
        newPaths.append(path)
    for i in range(len(paths)):
        paths[paths[i]] = newPaths[i]

    numCp = 0
    numCp = sum(deg(paths))
    if (numCp == 0):
        return paths

    ALNS_weight = [1, 1, 1]
    ALNS_r = 0.1

    while numCp != 0:
        print("start neighbour search")
        paths, numCp = replan(paths, numNeighbourhood, width,
                              height, instanceMap, instanceStarts, instanceGoals, ALNS_weight, numCp)
    return paths


if __name__ == "__main__":
    numNeighbourhood = 3
    instanceMap, instanceStarts, instanceGoals = import_mapf_instance(
        "test_24.txt")
    width = len(instanceMap)
    height = len(instanceMap[0])
    paths = LNS2(numNeighbourhood, width, height, instanceMap,
                 instanceStarts, instanceGoals)
    print("solution")
    for path in paths:
        print(path)
