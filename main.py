from loadscen import *
from prioritizedPlanning import *
from Utils import *
from LNSUtil import *
import heapq


numAgents = 3
instanceMap, instanceStarts, instanceGoals = loadScen('room-64-64-16-even-1.scen', numAgents)


#run PP for initial plan
paths = []
neighbourhood = list(range(numAgents))
newPaths = prioritized_planning(paths, neighbourhood, instanceMap, instanceStarts, instanceGoals)

for i in range(len(neighbourhood)):
	paths[neighbourhood[i]] = newPaths[i]

collisions = sum(deg(paths))
print('collisions', collisions)

for path in newPaths:
	print(path)












