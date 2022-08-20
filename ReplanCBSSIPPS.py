from CBSSIPPS import *
from ALNS import *
from collisionneighbourhood import *
from failureBasedNeighbourhood2 import *
from randomNeighborhood import *
from prioritizedPlanning import *
from LNSUtil import *
from pathlib import Path
from SIPPS2 import *
from loadscen import *
import time as timer

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


# replan untill collision free
def replan(paths, numNeighbourhood, width, height, instanceMap, instanceStarts, instanceGoals, ALNS_weight, prevCP, timeLimit, start):
    # select a neighbourhood construction method
    currTime = timer.time()
    if currTime - start >= timeLimit:
        return None, None
        
    # 0: collision, 1: failure, 2: random
    neighbourhood_kind = ALNS(ALNS_weight)

    neighbourhood = []
    if neighbourhood_kind == 0:
        print('collisionNeighbourhood')
        neighbourhood = collisionNeighbourhood(paths, numNeighbourhood, width, height, instanceMap)
    elif neighbourhood_kind == 1:
        print('failureNeighbourhood')
        neighbourhood = failureNeighbourhood(paths, numNeighbourhood)
    else:
        print('randomNeighbourhood')
        neighbourhood = randomNeighbourhood(paths, numNeighbourhood)

    #run modified prioritized planning to get replanned paths
    #neighbourhood, newPaths = prioritized_planning(paths, neighbourhood, instanceMap, instanceStarts, instanceGoals)

    neighbourhoodStarts = []
    neighbourhoodGoals = []
    for i in range(len(neighbourhood)):
        neighbourhoodStarts.append(instanceStarts[neighbourhood[i]])
        neighbourhoodGoals.append(instanceGoals[neighbourhood[i]])

    cbs = CBSSolver(instanceMap, neighbourhoodStarts, neighbourhoodGoals, paths, neighbourhood)
    newPaths = cbs.find_solution(False)

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


def LNS2CBS(numNeighbourhood, width, height, instanceMap, instanceStarts, instanceGoals, timeLimit):
    paths = list(range(len(instanceGoals)))
    neighbourhood, newPaths = prioritized_planning([], list(range(len(instanceGoals))), instanceMap, instanceStarts, instanceGoals)
    for i in range(len(neighbourhood)):
        paths[neighbourhood[i]] = newPaths[i]

    numCp = 0
    numCp = sum(deg(paths))
    start = timer.time()    
    if (numCp == 0):
        return paths, start

    ALNS_weight = [1, 1, 1]
    ALNS_r = 0.1


    while numCp != 0:
        paths, numCp = replan(paths, numNeighbourhood, width, height, instanceMap, instanceStarts, instanceGoals, ALNS_weight, numCp, timeLimit, start)
        if paths == None:
            return None, None

    return paths, start


if __name__ == "__main__":
    numNeighbourhood = 5
    numAgent = 10
    instanceMap, instanceStarts, instanceGoals = loadScen('room-32-32-4-even-11.scen', numAgent)
    paths = LNS2(numNeighbourhood, len(instanceMap[0]), len(instanceMap), instanceMap,
                instanceStarts, instanceGoals)
    print("solution")
    for path in paths:
        print(path)
