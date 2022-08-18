from loadscen import *
from prioritizedPlanning import *
from Utils import *
import heapq


numAgents = 10
#instanceMap, instanceStarts, instanceGoals = loadScen('Berlin_1_256-even-1.scen', numAgents)
instanceMap, instanceStarts, instanceGoals = loadScen('empty-8-8-even-1.scen', numAgents)


#run PP for initial plan
paths = []
neighbourhood = list(range(numAgents))
newPaths = prioritized_planning(paths, neighbourhood, instanceMap, instanceStarts, instanceGoals)

for i in range(len(neighbourhood)):
	paths[neighbourhood[i]] = newPaths[i]


for path in newPaths:
	print(path)












