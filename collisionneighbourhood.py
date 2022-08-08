from random import randrange

def collisionNeighbourhood(paths, N, width, height, instanceMap):
	#create collision graph as adjacency lists
	#organize paths into lookup dictionary
	timepos = {} # {y, x, t}: [agents...]
	numAgents = len(paths)
	for i in range(numAgents): #agent number
		for j in range(len(path)): #time step
			state = (path[i][j][0], path[i][j][1], j) #(y, x, t)
			if state not in timepos:
				timepos[state] = []
			timepos[state].append(i)


	adjlist = {} # {agent#}: [agents...]
	values = list(timepos.values())
	for cluster in values:
		if len(cluster) > 1:
			for agent in cluster:
				adjlist[agent] = []
				for agent2 in cluster:
					if agent != agent2
						adjlist[agent].append(agent2)

	#select random vertex and get it's connected component
	adjlistKeys = list(adjlist.keys())
	connectedComp = [ adjlistKeys[randrange(0, len(adjlistKeys))] ]
	index = 0
	visited = {}
	visited[connectedComp[0]] = 1
	while index < len(connectedComp):
		for nextVertex in adjlist[connectedComp[index]]:
			if nextVertex not in visited:
				connectedComp.append(nextVertex)
				visited[nextVertex] = 1
		index += 1

	
	neighbourhood = []

	if len(connectedComp) < N:
		#random walk to find collisions to fill size N neighbourhood
			#use timepos dictionary to check collisions
		neighbourhood.extend(connectedComp)
		while len(neighbourhood) < N:
			# select random member of connectedComp
			startMember = neighbourhood[randrange(0, len(neighbourhood))]

			# choose random pos in member's path
			startTime = randrand(0, len(paths[startMember]))
			startPos = paths[startMember][startTime]

			# random walk until collision with unvisited agent -> add
			moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
			currPos = startPos
			nextAgentCollisionFound = False
			while nextAgentCollisionFound == False:
				# select random move
				move = moves[randrange(0, len(moves))]
				nextPos = [currPos[0] + move[0], currPos[1] + move[1]]
				# perform move if eligible
				if (instanceMap[nextPos[0]][nextPos[1]] != '.' 
					or nextPos[0] < 0 
					or nextPos[0] >= height 
					or nextPos[1] < 0 
					or nextPos[1] >= width):
					continue
				else
					currPos = nextPos
					# check for collisions
					# calculate minimum travel time from startPos
					deltaTime = abs(currPos[0] - startPos[0]) + abs(currPos[1] - startPos[1])
					nextAgentCollisionFound = False
					state = (currPos[0], currPos[1], startTime + deltaTime)
					if (currPos[0], currPos[1], startTime + deltaTime) in timepos:
						for agent in timepos[state]:
							if agent not in visited:
								neighbourhood.append(agent)
								visited[agent] = 1
								nextAgentCollisionFound = True
								break
	elif len(connectedComp) > N:
		revisited = {}
		revisited[connectedComp[0]] = 1
		neighbourhood.append(connectedComp[0])
		#random walk on connected component
		currVertex = connectedComp[0]
		while len(neighbourhood) < N:
			#move to random adjacent vertex
			currVertex = adjlist[currVertex][randrand(0, len(adjlist[currVertex]))]
			if currVertex not in revisited:
				neighbourhood.append(currVertex)
				revisited[currVertex] = 1

	return neighbourhood



def priorityList(neighbourhood):
	PPlist = []
	while len(neighbourhood) > 0:
		index = randrange(0, len(neighbourhood))
		PPlist.append(neighbourhood.pop(index))
	return PPlist




#collision list
#make collision graph from collision list
# select random vertex and find it's largest connected component V'c
# if V'c < N, neighbourhood = V'c + random walk collisions
# else random walk on V'c until N vertices selected

#random











