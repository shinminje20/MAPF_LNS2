def loadScen(scenarioFile, numAgents):
	f = open(scenarioFile, 'r')
	line = f.readline() #version text
	line = f.readline() #first agent
	tokens = line.split('\t') 
	#[0] ???
	#[1] map name
	#[2] map width
	#[3] map height
	#[4] start x
	#[5] start y
	#[6] goal x
	#[7] goal y
	#[8] ???
	mapName = tokens[1]
	mapWidth = int(tokens[2])
	mapHeight = int(tokens[3])
	f2 = open('map/'+mapName, 'r')
	mapline = f2.readline() #advance to map data
	mapline = f2.readline()
	mapline = f2.readline()
	mapline = f2.readline()
	instanceMapTxt = []
	for i in range(mapHeight):
		instanceMapTxt.append(f2.readline().strip())
	f2.close()

	instanceMap = []
	for y in instanceMapTxt:
		instanceMap.append(list(map(lambda c : True if c == '.' else False, y)))

	instanceStarts = []
	instanceGoals = []
	instanceStarts.append((int(tokens[4]), int(tokens[5])))
	instanceGoals.append((int(tokens[6]), int(tokens[7])))
	for i in range(2, numAgents+1):
		tokens = f.readline().split()
		if len(tokens) == 0:
			break;
		instanceStarts.append((int(tokens[4]), int(tokens[5])))
		instanceGoals.append((int(tokens[6]), int(tokens[7])))
	f.close()

	return instanceMap, instanceStarts, instanceGoals
	#instanceStarts = [(x, y)]
	#instanceGoals = [(x, y)]
	#instanceMap = [[True/False, ...], ...]























