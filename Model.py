import Cell
import random
import time
import MountainFactory
import RiverFactory
import ContinentsFactory

class Model(object):

	def __init__(self, configManager):
		self.configManager 		= configManager

		self.worldCellHeight	= self.configManager.WORLDDISPLAYHEIGHT / self.configManager.CELLSIZE
		self.worldCellWidth		= self.configManager.WORLDDISPLAYWIDTH / self.configManager.CELLSIZE

		self.area = self.worldCellWidth * self.worldCellHeight

		self.landArea = 0

		self.createWorld()

		self.focusCell = (0, 0)

	def createWorld(self):
		print "World generation started"

		# Seed the random number generator.
		self.seed = self.configManager.WORLDGENSEED
		print "World gen seed: " + str(self.seed)

		random.seed(self.seed)

		self.world = self.newWorld()

		self.createContinents()

		self.placeMountainRanges(self.configManager.MOUNTAINRANGECOUNT)

		self.placeRivers(self.configManager.RIVERCOUNT)


	# Create the empty world.
	# Every cell is a generic cell object.
	def newWorld(self):
		print "Generating empty world"
		world = []
		for x in xrange(self.worldCellWidth):
			column = []
			# Iterate through SCREENHEIGHT by CELLSIZE to get number of rows.
			# Append item to column at each loop to create each cell's slot.
			for y in xrange(self.worldCellHeight):
				column.append(Cell.Cell())
			# Append each column to the overall board.
			world.append(column)

		return world

	def createContinents(self):
		continentsFactory = ContinentsFactory.ContinentsFactory(self, self.configManager)

		continentsFactory.createContinents()

	def placeMountainRanges(self, count):
		mountainFactory = MountainFactory.MountainFactory(self, self.configManager)

		for x in xrange(count):
			mountainFactory.createMountainRange()

	def placeRivers(self, count):
		riverFactory = RiverFactory.RiverFactory(self, self.configManager)

		for x in xrange(count):
			startPosition = self.getRandomCell()
			while self.validRiverStartLocation(startPosition):
				startPosition = self.getRandomCell()

			riverFactory.createRiver(startPosition)

	def validRiverStartLocation(self, (x, y)):
		cell = self.getCell((x, y))

		if cell.mountain:
			return True

	def getRandomCell(self):
		x = random.randint(0, self.worldCellWidth - 1)
		y = random.randint(0, self.worldCellHeight - 1)

		return x, y

	def getCell(self, (x, y)):
		return self.world[x][y]

	def replaceCell(self, (x, y), newCell):
		self.world[x][y] = newCell

	def outOfBounds(self, (x, y)):
		if x < 0 or y < 0 or x >= self.worldCellWidth or y >= self.worldCellHeight:
			return True
		else:
			return False

	def setFocusCell(self, (x, y)):
		self.setCellChanged(self.focusCell)

		self.focusCell = (x, y)

	def getFocusCell(self):
		return self.getCell(self.focusCell)

	def setCellChanged(self, (x, y), YESNO = True):
		self.getCell((x, y)).changed = YESNO

	def cellChanged(self, (x, y)):
		changed = self.world[x][y].changed

		return changed

	def getCellColour(self, (x, y)):
		cell = self.getCell((x, y))

		colour = cell.colour

		if colour != cell.lastColourDisplayed or cell.changed == True:
			cell.changed = True
		else:
			cell.changed = False

		cell.lastColourDisplayed = colour

		return colour