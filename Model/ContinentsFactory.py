import random
import math
import Cell
from random import randint
from ConfigParser import SafeConfigParser

class ContinentsFactory(object):
	
	def __init__(self, world, configManager):
		self.world = world
		self.configManager = configManager

		random.seed(self.configManager.WORLDGENSEED)

	# Creates continents.
	# Uses modified sparks algorithm found at http://www.cartania.com/alexander/generation.html
	def createContinents(self):
		sparkConstant = self.configManager.SPARKSCONSTANT

		# Generate list of sparks to be used for generation.
		sparksList = []

		# Generate sparks. Makes area of world / sparkConstant sparks. A higher spark constant creates chunkier
		# landmasses.
		for x in xrange(self.world.area / sparkConstant):
			# Create random co-ordinates for spark.
			y = randint(0, self.world.worldCellHeight - 1)
			x = randint(0, self.world.worldCellWidth - 1)

			# Set the tile to grassland.
			self.world.placeGrasslandCell((x, y))
			# Put this on the sparkslist.
			sparksList.append((x,y))
			# Increment the land area.
			self.world.landArea += 1

		# While there are still sparks in the list 
		# and land area hasn't exceeded it's max size as dictated by the config.ini
		while len(sparksList) > 0 and self.world.landArea < self.world.area * self.configManager.LANDPERCENTAGE:
			# Get a random spark from the spark list.
			sparkCoordinates = random.choice(sparksList)
			sparkTile = self.world.getCell(sparkCoordinates)
			
			# The repeatList stores which offsets have been used so far in the
			# spread of the spark.
			# This must be done because x and y are now generated randomly 
			# between -1 and 1 each. Previously it just iterated each from -1 to 1.
			# But this lead to the bottom and left of continents being very flat.
			# 0,0 shouldn't be checked because it's not an offset.
			repeatList = [(0,0)]
			# Surrounding tiles checked for spreading availability.
			tilesDone = 0
			# Check 8 tiles.
			while(tilesDone < 8):
				# Generate the random offsets.
				x = randint(-1,1)
				y = randint(-1,1)
				# If these offsets have already been used then try again.
				if (x,y) in repeatList:
					continue
				# Append the offsets to the repeatList for checking next loop.
				repeatList.append((x, y))
				# Increment the amount of tiles checked.
				tilesDone += 1
				# Set co-ordinates of new tile.
				newTileCoordinates = (sparkCoordinates[0] + x, sparkCoordinates[1] + y)

				# Ensure we aren't out of bounds
				if self.world.outOfBounds(newTileCoordinates):
					continue

				# Get the tile.
				newTile = self.world.getCell(newTileCoordinates)
				# Ensure the tile is inside the world.
				if newTileCoordinates[0] < 0 or newTileCoordinates[1] < 0 \
					or newTileCoordinates[0] > self.world.worldCellWidth or newTileCoordinates[1] > self.world.worldCellHeight:
					pass
				# If the tile is currently unassigned then spread sparkType to it,
				# along with the sparkTile's name.
				if newTile.name == "Empty":
					self.world.placeGrasslandCell(newTileCoordinates)
					# Add the new tile to the sparkslist.
					sparksList.append(newTileCoordinates)
					
					self.world.landArea += 1

			# Remove the spark from the sparksList.
			while sparkCoordinates in sparksList:
				sparksList.remove(sparkCoordinates)

		self.fillOceans()

		self.cleanOceans()

	def fillOceans(self):
		# Once we've gone through the land creation turn everything that isn't land into ocean.
		for x in xrange(0, self.world.worldCellWidth):
			for y in xrange(0, self.world.worldCellHeight):
				if self.world.getCell((x,y)).name == "Empty":
					self.world.placeLakeCell((x, y))

	# Remove the little bits of land dotted around in the ocean.
	def cleanOceans(self):
		for x in xrange(0, self.world.worldCellWidth):
			for y in xrange(0, self.world.worldCellHeight):
				if self.surroundedByOcean((x, y)):
					self.world.placeLakeCell((x, y))

	def surroundedByOcean(self, (x, y)):
		for x in xrange(-1, 2):
			for y in xrange(-1, 2):
				if not self.world.getCell((x, y)).water:
					return False

		return True
