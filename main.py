from loadscen import *

instanceMap, instanceStarts, instanceGoals = loadScen('Berlin_1_256-even-1.scen', 10)

print('Berlin_1_256-even-1.scen')
for y in instanceMap:
	print(y)

for i in range(len(instanceStarts)):
	print('agent', i, 'start:', instanceStarts[i])

for i in range(len(instanceGoals)):
	print('agent', i, 'goal:', instanceGoals[i])


#instanceMap: list of strings
#legend:
#	. 	- empty vertex
#	@	- wall
#	T 	- ???

# instance agents contains a list of tuples composed coordinates (start x, start y, goal x, goal y)




#run PP w/ SIPPS until stopped
#produces a list of paths


#run neighbourhood selection
#	generate list of collisions, hard and soft
#	select






