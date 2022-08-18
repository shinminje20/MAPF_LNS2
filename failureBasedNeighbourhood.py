from operator import ne
import random
from time import time
from LNSUtil import *


# find a1 (probability proportional to deg(i)
# input: list of degree (return of 'def' function) ex. [2,3]
# prolist ex. [0,0,1,1,1]
# return: int (id of agent) from 0 to n-1
def findA1(degList):
    probList = []
    for i in range(0, len(degList), 1):
        for j in range(0, degList[i], 1):
            probList.append(i)
    # both range inclusive
    ramdonIndex = random.randint(0, len(probList)-1)
    result = probList[ramdonIndex]
    return result


def makeUnion(list1, list2):
    final_list = []
    minLength = len(list1)
    min = list1.copy()
    max = list2.copy()
    if (len(list1) > len(list2)):
        minLength = len(list2)
        min = list2
        max = list1
    temp = []
    for i in range(0, minLength, 1):
        if (min[i] in max):
            final_list.append(min[i])
            temp.append(min[i])
    for i in temp:
        max.remove(i)
        min.remove(i)
    if (min != None):
        for x in min:
            final_list.append(x)
    if (max != None):
        for j in max:
            final_list.append(j)
    return final_list

# return: remained path out of all path


def difference(allPath, neighbour):
    diff = allPath.copy()
    for i in neighbour:
        if (i in allPath):
            allPath.remove(i)
    return diff


def whenVisit(path, goal):
    timestep = 0
    for i in range(0, len(path), 1):
        if path[i] == goal:
            timestep = i
    return timestep


def whenVisitList(pathList, goal):
    visitTimeList = []
    for i in range(0, len(pathList), 1):
        timestep = whenVisit(pathList[i], goal)
        visitTimeList.append(timestep)
    return visitTimeList


def makeVisitTimeWithPathDic(visitTimeList, As):
    # sorted one
    dic = {}
    i = 0
    for path in tuple(As):
        dic[visitTimeList[i]] = tuple(path)
        i += 1
    sortedkeys = list(dic.keys())
    sortedkeys.sort()

    # print(dic)

    sortedDic = {}
    for w in sortedkeys:
        sortedDic[w] = list(dic[w])

    return sortedDic, sortedkeys


# n=the number of neighbour
# path, example. path = [   [(1,1),(2,2)], [(1,1),(2,2)] ...]
def failureNeighbourhood(path, n):
    pathCopy = path.copy()

    # add a1 to neighbour
    # a1 = [(1,1),(1,2)]
    degList = deg(pathCopy)
    a1Id = findA1(degList)
    a1 = pathCopy[a1Id]
    neighbour = []
    neighbourIndex = []
    neighbour.append(a1)
    neighbourIndex.append(path.index(a1))
    pathCopy.remove(a1)

    As = []
    a1Start = a1[0]  # start point of a1
    for eachAgent in pathCopy:
        if (a1Start in eachAgent):
            As.append(eachAgent)
            # pathCopy.remove(eachAgent)

    Ag = []
    for eachAgent2 in pathCopy:
        if (eachAgent2[len(eachAgent2)-1] in a1):
            Ag.append(eachAgent2)
            # pathCopy.remove(eachAgent)

    union = makeUnion(As, Ag)

    # paths which is not selected as neighbour
    remain = difference(pathCopy, union)

    if len(union) == 0:
        return neighbour
    elif len(union) < n-1:
        for i in range(0, len(union), 1):
            neighbour.append(union[i])
            neighbourIndex.append(path.index(union[i]))
        diff = n-len(neighbour)
        for j in range(0, diff, 1):
            randomNeighbour = neighbour[random.randint(
                0, len(neighbour)-1)]  # a(j) from neighbour
            arr = []
            for k in range(0, len(remain), 1):
                if (randomNeighbour[len(randomNeighbour)-1] in remain[k]):
                    arr.append(remain[k])
            if (len(arr) == 0):
                continue
            randomIndex = random.randint(
                0, len(arr)-1)
            neighbour.append(arr[randomIndex])
            neighbourIndex.append(path.index(arr[randomIndex]))
    else:
        if (len(As) == 0):
            for x in range(0, n-1, 1):
                neighbour.append(Ag[x])
                neighbourIndex.append(path.index(Ag[x]))
        elif(len(Ag) >= n-1):
            visitTimeList = whenVisitList(As, a1[0])
            minIndex = visitTimeList.index(min(visitTimeList))
            neighbour.append(As[minIndex])
            for x in range(0, n-2, 1):
                neighbour.append(Ag[x])
                neighbourIndex.append(path.index(Ag(x)))

        else:
            visitTimeList = whenVisitList(As, a1[0])
            sortedDic, sortedKeys = makeVisitTimeWithPathDic(visitTimeList, As)
            for v in range(0, len(Ag), 1):
                neighbour.append(Ag[v])
            for g in range(0, n-1-len(Ag), 1):
                neighbour.append(sortedDic[sortedKeys[0]])
                neighbourIndex.append(path.index(sortedDic[sortedKeys[0]]))
                del sortedDic[sortedKeys[0]]

    return list(set(neighbourIndex))
