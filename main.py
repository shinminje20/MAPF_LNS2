from loadscen import *
from prioritizedPlanning import *
from Utils import *
import heapq


numAgents = 1
#instanceMap, instanceStarts, instanceGoals = loadScen('Berlin_1_256-even-1.scen', numAgents)
instanceMap, instanceStarts, instanceGoals = loadScen('empty-8-8-even-1.scen', numAgents)


#run PP for initial plan
paths = []

newPaths = prioritized_planning(paths, list(range(numAgents)), instanceMap, instanceStarts, instanceGoals)

for path in newPaths:
	print(path)












