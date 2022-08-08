from collisionNeighbourhood import collisionNeighbourhood


#collisionNeighbourhood(paths, N, width, height, instanceMap):


instanceMap = [
	"@@@@@@@@@@",
	"@.@@@@.@.@",
	"@........@",
	"@.@@@@@@.@",
	"@@@@@@@@@@"
	]

paths = [
	[[1, 1], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [1, 8]],
	[[3, 1], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [3, 8]],
	[[2, 8], [2, 7], [2, 6], [2, 5], [2, 4], [2, 3], [2, 2], [2, 1]]
	]

N = 3
width = 10
height = 5




paths2 = [
	[[1, 1], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [1, 8]],
	[[3, 1], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [3, 8]],
	[[2, 8], [2, 7], [2, 6], [1, 6], [1, 6], [1, 6], [1, 6], [2, 6], [2, 5], [2, 4], [2, 3], [2, 2], [2, 1]]
]


selectedNeighbourhood = collisionNeighbourhood(paths2, N, width, height, instanceMap)
print(selectedNeighbourhood)








