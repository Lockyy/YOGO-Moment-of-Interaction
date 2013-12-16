import PathfindingNode
import Cell

class RiverFactory:

	def __init__(self, model, configManager):
		self.configManager = configManager
		self.model = model

	# A*/Djikstra's algorithm
	def createRiver(self, start):
		# The starting node's co-ordinates.
		newNode = start

		# The open and closed list.
		# These contain pathfindingNode objects, not just co-ordinates.
		openList = []
		closedList = []

		# The starting node and first focused node.
		currentNode = PathfindingNode.PathfindingNode(newNode)

		# Put the starting node in the open list.
		openList.append(currentNode)

		# Whilst we haven't found the ocean.
		while not self.model.outOfBounds(currentNode.coords) and not self.model.getCell(currentNode.coords).water:
			# If the open list is empty then we have exhausted all possible paths and still not reached the sea.
			# The sea is unreachable from the current location.
			if openList == []:
				print "river failed"
				return False

			# Find the node with the lowest G in the openList.
			currentNode = self.lowestG(openList)

			# Remove that node from the open list and put it on the closed list.
			openList.remove(currentNode)
			closedList.append(currentNode)

			# Go through every directly adjacent tile to the currentNode.
			for x in xrange(-1,2):
				for y in xrange(-1,2):
					# Ignore corner nodes.
					if abs(x) == abs(y):
						continue
					
					# Create new node co-ordinates.
					newNode = [currentNode.coords[0] + x, currentNode.coords[1] + y]

					# If the tile is out of bounds then just ignore it.
					if self.model.outOfBounds(newNode):
						continue
					else:
						newNodeCell = self.model.getCell(newNode)

					# Create new node from those co-ordinates.
					newOpen = PathfindingNode.PathfindingNode(newNode, currentNode)

					# If the tile isn't in the closed list, and is either settleable or is ocean.
					# We include the ocean so we can actually find the ocean for the river to exit into.
					if (newNodeCell.riverPassable or not newNodeCell.land) and not self.inList(newNode, closedList):
						if not self.inList(newNode, openList):
							openList.append(newOpen)
						else:
							# If this node is already in the open list then find out if the new path is more efficient than
							# the old path to it. If it is then replace the parent of the node already in the list with the
							# new node's parent.
							nodeInList = self.getFromList(newNode, openList)
							if nodeInList.getG() > newOpen.getG():
								nodeInList.parent = newOpen.parent

		path = self.getRiversPath(currentNode)

		# Not handling this here lets me deal with making sure the river looks neat elsewhere.
		self.placeRiverTiles(path)

		return True

	def placeRiverTiles(self, path):
		for node in path:
			self.model.placeRiverCell(node.coords)

	def getRiversPath(self, currentNode):
		path = []
		while not currentNode.parent == None:
			path.append(currentNode.parent)
			currentNode = currentNode.parent

		return path

	def inList(self, nodeCoords, nodeList):
		for node in nodeList:
			if node.coords == nodeCoords:
				return True

		return False

	def getFromList(self, nodeCoords, nodeList):
		for node in nodeList:
			if node.coords == nodeCoords:
				return node

		return False

	def lowestG(self, openList):
		g = None
		outputNode = None
		for node in openList:
			if g == None or node.getG() < g:
				g = node.getG()
				outputNode = node

		return outputNode
