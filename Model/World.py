import random
import time
import Cell
import MountainFactory
import RiverFactory
import ContinentsFactory
import ForestFactory

class World(object):

	def __init__(self, configManager):
		self.configManager = configManager

		self.worldCellHeight	= self.configManager.WORLDDISPLAYHEIGHT / self.configManager.CELLSIZE
		self.worldCellWidth		= self.configManager.WORLDDISPLAYWIDTH / self.configManager.CELLSIZE

		self.area = self.worldCellWidth * self.worldCellHeight

		self.landArea = 0

		# The cell that the user has clicked. This cell's details are displayed in the sidebar.
		# Also, when y is pressed this cell will become the village.
		self.focusCell = (0, 0)

		self.seed = self.configManager.WORLDGENSEED
		random.seed(self.seed)
		print "World generation started"
		# Print the seed to the log file. People can recover it if they really want it that way.
		print "World gen seed: " + str(self.seed)

		self.world = self.newWorld()
		self.worldGenStage = 1
		self.worldGenStageMessage = "land"
		self.worldGenDone = False
		self.year = 1

	def createWorld(self):
		self.createContinents()

		self.placeMountainRanges(self.configManager.MOUNTAINRANGECOUNT)

		self.placeRivers(self.configManager.RIVERCOUNT)

		self.placeForests(self.configManager.FORESTCOUNT)

	# Advance world gen one step at a time.
	def createWorldStep(self):
		if self.worldGenStage == 1:
			self.createContinents()
			self.worldGenStage += 1
			self.worldGenStageMessage = "mountains"
			return

		if self.worldGenStage == 2:
			self.placeMountainRanges(self.configManager.MOUNTAINRANGECOUNT)
			self.worldGenStage += 1
			self.worldGenStageMessage = "rivers"
			return

		if self.worldGenStage == 3:
			self.placeRivers(self.configManager.RIVERCOUNT)
			self.worldGenStage += 1
			self.worldGenStageMessage = "forests"
			return

		if self.worldGenStage == 4:
			self.placeForests(self.configManager.FORESTCOUNT)
			self.worldGenStage += 1
			self.worldGenStageMessage = "done"
			self.worldGenDone = True
			return

	# Create the empty world.
	# Every cell is a generic cell object.
	def newWorld(self):
		print "Generating empty world"
		world = []
		for x in xrange(self.worldCellWidth):
			column = []
			# Append item to column at each loop to create each cell's slot.
			for y in xrange(self.worldCellHeight):
				column.append(Cell.Cell(self.configManager))
			# Append each column to the overall world.
			world.append(column)

		return world

	# Create the continents factory and produce the continents.
	def createContinents(self):
		continentsFactory = ContinentsFactory.ContinentsFactory(self, self.configManager)

		continentsFactory.createContinents()

	# Create the mountain factory and produce the mountain ranges.
	def placeMountainRanges(self, count):
		mountainFactory = MountainFactory.MountainFactory(self, self.configManager)

		for x in xrange(count):
			mountainFactory.createMountainRange()

	# Create the river factory and produce the rivers.
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

	# Create the forest factory and produce the forests.
	def placeForests(self, count):
		forestFactory = ForestFactory.ForestFactory(self, self.configManager)

		for x in xrange(count):
			forestFactory.createForest()

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

	# Get whether a cell has changed since the last game window draw.
	def setCellChanged(self, (x, y), YESNO = True):
		self.getCell((x, y)).changed = YESNO

	def cellChanged(self, (x, y)):
		changed = self.world[x][y].changed

		return changed

	def getCellColour(self, (x, y)):
		cell = self.getCell((x, y))

		colour = cell.colour

		# Keep track of whether the cell has changed colour or not.
		if colour != cell.lastColourDisplayed or cell.changed == True:
			cell.changed = True
		else:
			cell.changed = False

		cell.lastColourDisplayed = colour

		return colour

	# Place the various tiles at the given location.
	# Makes things far cleaner elsewhere to have a bunch of these methods here.
	def placeGrasslandCell(self, (x, y)):
		self.replaceCell((x, y), Cell.GrasslandCell(self.configManager))

	def placeDesertCell(self, (x, y)):
		self.replaceCell((x, y), Cell.DesertCell(self.configManager))

	def placeMountainCell(self, (x, y)):
		self.replaceCell((x, y), Cell.MountainCell(self.configManager))

	def placeRiverCell(self, (x, y)):
		self.replaceCell((x, y), Cell.RiverCell(self.configManager))

	def placeLakeCell(self, (x, y)):
		self.replaceCell((x, y), Cell.LakeCell(self.configManager))

	def placeForestCell(self, (x, y)):
		self.replaceCell((x, y), Cell.ForestCell(self.configManager))

	def placeFarmCell(self, (x, y)):
		self.replaceCell((x, y), Cell.FarmCell(self.configManager))

	def placeVillageCell(self, (x, y)):
		self.replaceCell((x, y), Cell.VillageCell(self.configManager))

	def placePastureCell(self, (x, y)):
		self.replaceCell((x, y), Cell.PastureCell(self.configManager))

	def placeInitialVillage(self):
		self.placeVillageCell(self.focusCell)

	# Move forward a year.
	# Not much happens in the Moment of Interaction world.
	def advanceYear(self):
		for x in xrange(0, self.worldCellWidth):
			for y in xrange(0, self.worldCellHeight):
				cell = self.getCell((x, y))

				cell.regenResources()

		self.year += 1