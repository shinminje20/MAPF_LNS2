from collisionneighbourhood import *
from prioritizedPlanning import *
from Replan import *
from Utils import *
from LNSUtil import *
import heapq

#collisionNeighbourhood(paths, N, width, height, instanceMap):


instanceMapTxt = [
	"@@@@@@@@@@",
	"@.@@@@.@.@",
	"@........@",
	"@.@@@@@@.@",
	"@@@@@@@@@@"
	]

instanceMap = []
for row in instanceMapTxt:
	instanceMap.append(list(map(lambda c : True if c == '.' else False, row)))


instanceStarts = [(1, 1), (1, 3), (8, 2)]
instanceGoals = [(8, 1), (8, 3), (1, 2)]
paths = [
	[(1, 1), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (8, 1)],
	[(1, 3), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (8, 3)],
	[(8, 2), (7, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (1, 2)]
	]

N = 3
width = 10
height = 5

collisions = len(degID(paths))
#print(collisions)

ALNS_weight = [1, 1, 1]
while collisions > 0:
    newPath, collisions = replan(paths, 2, width, height, instanceMap, instanceStarts, instanceGoals, ALNS_weight, collisions)

#solution = LNS2(2, width, height, instanceMap, instanceStarts, instanceGoals)




'''
paths2 = (
	((1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (1, 8)),
	((3, 1), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (3, 8)),
	((2, 8), (2, 7), (2, 6), (1, 6), (1, 6), (1, 6), (1, 6), (2, 6), (2, 5), (2, 4), (2, 3), (2, 2), (2, 1))
)


#selectedNeighbourhood = collisionNeighbourhood(paths2, N, width, height, instanceMap)
#print(selectedNeighbourhood)

constraintTable = dict()
add_constraints_from_path(constraintTable, paths(0))
print(constraintTable)
add_constraints_from_path(constraintTable, paths(1))
print(constraintTable)
add_constraints_from_path(constraintTable, paths(2))
print(constraintTable)
'''



