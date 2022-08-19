def compare(cord1, cord2):

    if cord1[0] == cord2[0] and cord1[1] == cord2[1]:
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
        for secondPath in range(firstPath + 1, len(path), 1):
            if(path[firstPath] == path[secondPath]):
                continue
            length = len(path[secondPath]) if len(path[firstPath]) > len(path[secondPath]) else len(path[firstPath])
            for timestep in range(0, length, 1):
                if compare(path[firstPath][timestep], path[secondPath][timestep])\
                    or (timestep > 0 and compare(path[firstPath][timestep-1], path[secondPath][timestep]) and compare(path[firstPath][timestep], path[secondPath][timestep-1])):
                    deg += 1
                    break
        degList.append(deg)
        deg = 0
    return degList


def degID(path):
    degList = []
    for firstPath in range(0, len(path), 1):
        for secondPath in range(firstPath + 1, len(path), 1):
            if(path[firstPath] == path[secondPath]):
                continue
            length = len(path[secondPath]) if len(path[firstPath]) > len(path[secondPath]) else len(path[firstPath])
            for timestep in range(0, length, 1):
                if compare(path[firstPath][timestep], path[secondPath][timestep]):
                    degList.append((firstPath, secondPath, timestep))
                    break
                elif timestep > 0 and compare(path[firstPath][timestep-1], path[secondPath][timestep]) and compare(path[firstPath][timestep], path[secondPath][timestep-1]):
                    degList.append((firstPath, secondPath, timestep-1, timestep))
                    break
    return degList