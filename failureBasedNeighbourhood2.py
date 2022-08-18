import random
from LNSUtil import *
import sys


def findA1(degList):
    probList = []
    for i in range(0, len(degList), 1):
        for j in range(0, degList[i], 1):
            probList.append(i)
    # both range inclusive
    ramdonIndex = random.randint(0, len(probList)-1)
    result = probList[ramdonIndex]
    return result


def whenVisit(path, goal):
    for i, loc in enumerate(path):
        if loc == goal:
            return i
    return 0


def whenVisitList(paths, agents, goal):
    visitTimeList = []
    for agent in agents:
        visitTimeList.append(whenVisit(paths[agent], goal))
    return visitTimeList


def minVisitTimeAgent(paths, agents, goal):
    minTime = sys.maxsize
    minAgent = -1
    for agent in agents:
        timestep = whenVisit(paths[agent], goal)
        if timestep < minTime:
            minTime = timestep
            minAgent = agent
    return minAgent


def makeVisitTimeWithPathDic(visitTimeList, As):
    # sorted one
    dic = {}
    for i, visitTime in enumerate(visitTimeList):
        if visitTime not in dic:
            dic[visitTime] = []
        dic[visitTime].append(As[i])
    sortedkeys = list(dic.keys())
    sortedkeys.sort()
    return dic, sortedkeys


def failureNeighbourhood(paths, n):
    paths_sets = []
    for i, path in enumerate(paths):
        paths_sets.append(set())
        for pos in path:
            paths_sets[i].add(pos)

    degList = deg(paths)
    a1Id = findA1(degList)

    neighbourhood = [a1Id]

    As = []
    a1Start = paths[a1Id][0]
    for i, path in enumerate(paths_sets):
        if a1Start in path:
            As.append(i)

    Ag = []
    for i in range(len(paths_sets)):
        if paths[i][-1] in paths_sets[a1Id]:
            Ag.append(i)
    print("Ag")
    print(Ag)

    union = set(Ag).union(set(As))

    remain = set()
    for i in range(len(paths)):
        if i not in union:
            remain.add(i)

    if len(union) == 0:
        return neighbourhood
    elif len(As) + len(Ag) < n-1:
        neighbourhood.extend(As)
        neighbourhood.extend(Ag)
        diff = n - len(neighbourhood)
        for j in range(diff):
            randomNeighbour = random.randrange(len(neighbourhood))
            arr = []
            for agent in remain:
                if paths[randomNeighbour][-1] in paths_sets[agent]:
                    arr.append(agent)
            neighbourhood.append(arr[random.randrange(len(arr))])
    else:
        if len(As) == 0:
            for x in range(n):
                neighbourhood.append(Ag[x])
        elif len(Ag) >= n-1:
            minAgent = minVisitTimeAgent(paths, As, paths[a1Id][0])
            neighbourhood.append(minAgent)
            for x in range(n-1):
                neighbourhood.append(Ag[x])
        else:
            visitTimeList = whenVisitList(paths, As, paths[a1Id][0])
            sortedDic, sortedKeys = makeVisitTimeWithPathDic(visitTimeList, As)
            for A in Ag:
                neighbourhood.append(A)
            for key in sortedKeys:
                if len(neighbourhood) + len(sortedDic[key]) < n:
                    neighbourhood.append(sortedDic[key])
                else:
                    count = n - len(neighbourhood)
                    for i in range(count):
                        neighbourhood.append(sortedDic[key][i])

    return list(set(neighbourhood))
