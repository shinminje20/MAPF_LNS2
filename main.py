from loadscen import *
from prioritizedPlanning import *
from Utils import *
import heapq


numAgents = 10
instanceMap, instanceStarts, instanceGoals = loadScen('Berlin_1_256-even-1.scen', numAgents)

#run PP for initial plan
paths = []

newPaths = prioritized_planning(paths, list(range(numAgents)), instanceMap, instanceStarts, instanceGoals)

print(newPaths)












