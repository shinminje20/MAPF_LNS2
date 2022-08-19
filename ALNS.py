import random
# weight1 = weight of first neighbourhood search
# weight2 =  weight of second neighbourhood search
# r = user-specified reation fator that controls how quickly the weight react to the changes in the
#     relative success in reducing the CP
# cp1 = the number of collision pair before replan
# cp = the number of collision pair after replan


def ALNS(weight):
    # use index to distiguish neighbourhood (0,1,2)
    # index0: collision, index1: failure, index2: random
    population = [0, 1, 2]
    return random.choices(population, weights=weight, k=1)[0]


def updateWeight(weight, r, cp1, cp2, method):
    cp = cp1-cp2
    weight[method] = r * max(0, cp) + (1-r)
    return weight


if __name__ == "__main__":

    # default value (weight of each neighbour and r)
    weight = [1, 1, 1]
    r = 0.1

    for a in range(0, 5, 1):
        # selecting a way out of 3 neighbourhood search
        selectedNeighbour = ALNS(weight)

        # selelct agent for neigbhourhood

        # find out collision pair before replanning in neighbourhood, using deg function in failureBasedNeighbourhoodSearch
        cp1 = 10

        # replanning...

        # find out collision pair, using deg function in failureBasedNeighbourhoodSearch
        cp2 = 5

        weight[selectedNeighbour] = updateWeight(
            weight[selectedNeighbour], r, cp1, cp2)

        print(selectedNeighbour)
        print(weight)
