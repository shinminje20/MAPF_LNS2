from loadscen import *
from prioritizedPlanning import *
from Utils import *
from LNSUtil import *
import heapq


numAgents = 10
instanceMap, instanceStarts, instanceGoals = loadScen('room-32-32-4-even-1.scen', numAgents)


#run PP for initial plan
paths = []
neighbourhood = list(range(numAgents))
newPaths = prioritized_planning(paths, neighbourhood, instanceMap, instanceStarts, instanceGoals)

for i in range(len(neighbourhood)):
	paths[neighbourhood[i]] = newPaths[i]

collisions = degID(newPaths)
print('collisions', collisions)

pathCosts = 0
for i in range(len(newPaths)):
    print("agent", i, newPaths[i])
    pathCosts += len(newPaths[i])

print(pathCosts)









