from random import randrange

def collisionNeighbourhood(paths, N):
	#create collision graph
	timepos = {}
	numAgents = len(paths)
	for i in range(numAgents): #agent number
		for j in range(len(path)): #time step
			state = (path[j][0], path[j][1], j) #(x, y, t)
			if state not in timepos:
				timepos[state] = []
			timepos[state].append(i)

	adjlist = {}
	values = list(timepos.values())
	for cluster in values:
		if len(cluster) > 1:
			for agent in cluster:
				adjlist[agent] = []
				for agent2 in cluster:
					if agent != agent2
						adjlist[agent].append(agent2)

	#select random vertex and get it's connected component
	adjlistKeySet = list(adjlist.keys())	
	neighbourhood = [ adjlistKeySet[randrange(0, len(adjlistKeySet))] ]
	index = 0
	visited = {}
	visited[neighbourhood[0]] = 1
	while index < len(neighbourhood):
		for nextVertex in adjlist[neighbourhood[index]]:
			if nextVertex not in visited:
				neighbourhood.append(nextVertex)
				visited[nextVertex] = 1
		index += 1

	if len(neighbourhood) < N:
		#random walk collisions fill
	elif len(neighbourhood) > N:
		#random walk on connected component







#collision list
#make collision graph from collision list
# select random vertex and find it's largest connected component V'c
# if V'c < N, neighbourhood = V'c + random walk collisions
# else random walk on V'c until N vertices selected

#random











