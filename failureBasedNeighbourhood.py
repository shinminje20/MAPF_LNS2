from operator import ne
import random
from time import time

from toml import TomlDecodeError


def compare(cord1, cord2):
    if cord1[0] == cord2[0]:
        if cord1[1] == cord2[1]:
            return True

    return False


# find degree of each agent in collision graph
# input: path [ [path of agent1], [path of agent2] ...]
# [path of agent1] = [(1,2),(1,3),(1,4)...]
# return: list of degree of each agent
# ex. [1,2,3,4 ...]
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


# n=the number of neighbour
# path, example. path = [   [(1,1),(2,2)], [(1,1),(2,2)] ...]
def failure(path, n):
    pathCopy = path

    # add a1 to neighbour
    # a1 = [(1,1),(1,2)]
    degList = deg(pathCopy)
    a1Id = findA1(degList)
    a1 = pathCopy[a1Id]
    neighbour = []
    neighbour.append(a1)
    pathCopy.remove(a1)

    print("a1" + str(a1))

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

    print("As" + str(As))
    print("Ag" + str(Ag))

    union = makeUnion(As, Ag)

    remain = difference(pathCopy, union)

    if len(union) == 0:
        return neighbour
    elif len(union) < n-1:
        for i in range(0, len(union), 1):
            neighbour.append(union[i])
        diff = n-len(neighbour)
        for j in range(0, diff, 1):
            randomNeighbour = neighbour[random.randint(0, len(neighbour)-1)]
            arr = []
            for k in range(0, len(remain), 1):
                if (randomNeighbour[len(randomNeighbour)-1] in remain[k]):
                    arr.append(remain[k])
            neighbour.append(arr[random.randint(0, len(arr)-1)])
    else:
        if (len(As) == 0):
            print("+=======")
            print(len(As))
            print(Ag)
            print(neighbour)
            for x in range(0, n-1, 1):
                neighbour.append(Ag[x])
        elif(len(Ag) >= n-1):
            visitTimeList = whenVisitList(As, a1[0])
            minIndex = visitTimeList.index(min(visitTimeList))
            neighbour.append(As[minIndex])
            for x in range(0, n-2, 1):
                neighbour.append(Ag[x])
                '''랜덤으로 하라는데 그냥 순서대로 해도?'''

        else:
            visitTimeList = whenVisitList(As, a1[0])
            for v in range(0, len(Ag), 1):
                neighbour.append(Ag[v])
            for g in range(0, n-1-len(Ag), 1):
                minIndex = visitTimeList.index(min(visitTimeList))
                neighbour.append(As[minIndex])
                visitTimeList[minIndex] = 99999999999999999
                ''' 다른방법 찾기'''

    return neighbour


if __name__ == "__main__":
    print(failure(path2, 2))
