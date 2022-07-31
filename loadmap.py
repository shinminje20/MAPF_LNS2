
def loadScenario(scenarioFile):
	f = open('scen/' + scenarioFile + '.scen', 'r')
	line = f.readline() #version text
	line = f.readline() #first agent
	tokens = line.split('\t') 
	#[1] map name
	#[2] map width
	#[3] map height
	#[4] start x
	#[5] start y
	#[6] goal x
	#[7] goal y
	mapName = tokens[1]
	mapWidth = int(tokens[2])
	mapHeight = int(tokens[3])
	f2 = open('map/'+mapName, 'r')
	mapline = f2.readline() #advance to map data
	mapline = f2.readline()
	mapline = f2.readline()
	mapline = f2.readline()
	instanceMap = []
	for i in range(mapHeight):
		instanceMap.append(f2.readline().strip())



	#print(tokens)
	f2.close()
	f.close()


loadScenario('Berlin_1_256-even-1')



























