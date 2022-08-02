import random
# weight1 = weight of first neighbourhood search
# weight2 =  weight of second neighbourhood search
# r = user-specified reation fator that controls how quickly the weight react to the changes in the
#     relative success in reducing the CP
# cp1 = the number of collision pair before replan
# cp = the number of collision pair after replan


def ALND(weight):
    # use index to distiguish neighbourhood (0,1)
    population = [0, 1]
    return random.choices(population, weights=weight, k=1)[0]


def updateWeight(weight, r, cp1, cp2):
    cp = cp1-cp2
    weight = r * max(0, cp) + (1-r)
    return weight


if __name__ == "__main__":

    # for a in range(0, 10, 1):

    # default value (weight of each neighbour and r)
    weight = [1, 1]
    r = 0.1

    # index 0: collision, index 1: failure
    selectedNeighbour = ALND(weight)

    # selecting neighbour...

    # find out collision pair, using deg function in failureBasedNeighbourhoodSearch
    cp1 = 15

    # replanning...

    # find out collision pair, using deg function in failureBasedNeighbourhoodSearch
    cp2 = 4

    weight[selectedNeighbour] = updateWeight(
        weight[selectedNeighbour], r, cp1, cp2)

    '''
    when we merge our code, code will be specified more.
    '''

    print(selectedNeighbour)
    print(weight)
