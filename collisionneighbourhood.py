from random import randrange
import time
import heapq

def collisionNeighbourhood(paths, N, width, height, instanceMap):
	print("colneigh")
	#organize paths into lookup dictionary
	timepos = {} # {y, x, t}: [agents...]
	numAgents = len(paths)
	for i in range(numAgents): #agent number
		for j in range(0, len(paths[i])): #vertex collisions
			state = (paths[i][j][0], paths[i][j][1], j) #(y, x, t)
			if state not in timepos:
				timepos[state] = set()
			timepos[state].add(i)

		for j in range(1, len(paths[i])): #edge collisions
			#direction of travel
			travelState = (paths[i][j-1][0], paths[i][j-1][1], paths[i][j][0], paths[i][j][1], j) #(y, x, y', x', t)
			#opposing edge constraint
			inverseState = (paths[i][j][0], paths[i][j][1], paths[i][j-1][0], paths[i][j-1][1], j)
			if travelState not in timepos:
				timepos[travelState] = set()
			timepos[travelState].add(i)
			if inverseState not in timepos:
				timepos[inverseState] = set()
			timepos[inverseState].add(i)

	#create collision graph as adjacency lists
	adjlist = {} # {agent#}: {agents...}
	values = list(timepos.values())
	for cluster in values:
		if len(cluster) > 1:
			for agent in cluster:
				if agent not in adjlist:
					adjlist[agent] = set()
				for agent2 in cluster:
					if agent != agent2:
						adjlist[agent].add(agent2)

	#select random vertex and get it's connected component
	adjlistKeys = list(adjlist.keys())
	connectedComp = [ adjlistKeys[randrange(0, len(adjlistKeys))] ]
	index = 0
	visited = set()
	visited.add(connectedComp[0])
	while index < len(connectedComp):
		for nextVertex in adjlist[connectedComp[index]]:
			if nextVertex not in visited:
				connectedComp.append(nextVertex)
				visited.add(nextVertex)
		index += 1
	
	neighbourhood = []

	if len(connectedComp) < N:
		#distance based non-random fill with other agents
		#get random member and pos/time
		#calculate manhattan distance to other agents
		#pick closest not-yet-visited
		#repeat until filled
		neighbourhood.extend(list(visited))
		while len(neighbourhood) < N:
			# select random member of connectedComp
			startMember = neighbourhood[randrange(len(neighbourhood))]

			# choose random time,pos in member's path
			startTime = randrange(len(paths[startMember]))
			startPos = paths[startMember][startTime]

			#calculate manhattan distance to non-visited agents
			distanceToAgents = []
			for i in range(len(paths)):
				if i not in visited:
					agentPos = paths[i][startTime] if startTime < len(paths[i]) else paths[i][-1]
					distance = abs(agentPos[0]-startPos[0]) + abs(agentPos[1]-startPos[1])
					heapq.heappush(distanceToAgents, (distance, i))

			#pick from heap to fill N without restarting
			while len(neighbourhood) < N:
				nextAgent = heapq.heappop(distanceToAgents)
				neighbourhood.append(nextAgent[1])
		'''
		print("random walk fill")
		#random walk to find collisions to fill size N neighbourhood
			#use timepos dictionary to check collisions
		neighbourhood.extend(connectedComp)
		while len(neighbourhood) < N:
			# select random member of connectedComp
			startMember = neighbourhood[randrange(0, len(neighbourhood))]

			# choose random time,pos in member's path
			startTime = randrange(0, len(paths[startMember]))
			startPos = paths[startMember][startTime]

			# random walk until collision with unvisited agent -> add
			moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
			currPos = startPos
			nextCollidableAgentFound = False
			startTime = time.clock_gettime_ns(time.CLOCK_REALTIME)
			while nextCollidableAgentFound == False:
				# select random eligible move
				nextPos = randomValidMove(currPos, instanceMap, width, height)
				# perform move if eligible
				if nextPos == None:
					#None move was found, end loop and restart or do nothing?
					print("debug1")
					nextCollidableAgentFound = True
					break
				else:
					searchTime = time.clock_gettime_ns(time.CLOCK_REALTIME)
					if searchTime - startTime > 5000000000:
						break
					print(nextPos, len(visited), len(neighbourhood))
					currPos = nextPos
					# check for other agents at this time step
					state = (currPos[0], currPos[1], startTime)
					if (currPos[0], currPos[1], startTime) in timepos:
						for agent in timepos[state]:
							if agent not in visited:
								neighbourhood.append(agent)
								visited[agent] = 1
								nextCollidableAgentFound = True
								break
		'''
	elif len(connectedComp) >= N:
		print("connectedComp subset")
		revisited = {}
		revisited[connectedComp[0]] = 1
		neighbourhood.append(connectedComp[0])

		#random walk on connected component
		currVertex = connectedComp[0]
		while len(neighbourhood) < N:
			#move to random adjacent vertex
			tempList = list(adjlist[currVertex])
			currVertex = tempList[randrange(0, len(tempList))]
			if currVertex not in revisited:
				neighbourhood.append(currVertex)
				revisited[currVertex] = 1

	return neighbourhood

def randomValidMove(currPos, instanceMap, width, height):
	moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
	validMoves = []
	for move in moves:
		nextPos = [currPos[0] + move[0], currPos[1] + move[1]]
		if (nextPos[0] >= 0 
			and nextPos[0] < height 
			and nextPos[1] >= 0 
			and nextPos[1] < width 
			and instanceMap[nextPos[0]][nextPos[1]] == True):
			validMoves.append(nextPos)
	if len(validMoves) > 0:
		return validMoves[randrange(0, len(validMoves))]
	else:
		return None


