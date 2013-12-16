import random
import math
import pygame
import Cell
from random import randint
from ConfigParser import SafeConfigParser

class ForestFactory(object):

	def __init__(self, model, configManager):
		self.model = model
		self.configManager = configManager

	# Creates a forest.
	def createForest(self):
		# Place the first tile.
		spark = self.createInitialSpark()

		self.spreadForest(spark)

	# Works out the size of the forest to be created.
	def getForestSize(self):
		minSize = self.configManager.FORESTSIZEMIN
		maxSize = self.configManager.FORESTSIZEMAX

		if minSize < 0:
			minSize = 0
		if maxSize < minSize:
			maxSize = minSize

		return randint(minSize, maxSize)

	# Places the initial spark of the new biome.
	def createInitialSpark(self):
		spark = self.getValidInitialSpark()
		newSparkTile = self.model.getCell(spark)

		self.model.placeForestCell(spark)

		# Store the co-ordinates of the initial spark.
		initialSpark = spark

		return initialSpark

	# Gets a "valid" location for the initial spark of the new forest.
	def getValidInitialSpark(self):
		# Get a random co-ordinate on the map.
		spark = self.model.getRandomCell()

		# Keep looking for a sparks tile until we find one that is compatible with this forest.
		while not self.checkCompatibility(spark):
			spark = self.model.getRandomCell()

		return spark

	# Spreads the forest around to create a nice sizeable forest.
	def spreadForest(self, spark):
		# Get the exact size of the new forest.
		actualSize = self.getForestSize()

		openList = closedList = [spark]

		loops = 0
		while len(openList) < actualSize and loops < actualSize * 5:
			openList = openList + self.getAdjacentTiles(spark, openList)
			spark = random.choice(openList)
			loops += 1

		for tile in openList:
			self.model.placeForestCell(tile)

	def getAdjacentTiles(self, spark, openList):
		output = []
		for x in xrange(-1,2):
			for y in xrange(-1,2):
				adjacentTile = (spark[0] + x, spark[1] + y)
				# Whether the adjacent tile is compatible with the new forest.
				if not adjacentTile in openList and self.checkCompatibility(adjacentTile):
					output.append(adjacentTile)
		return output

	# Gives a random tile adjacent to the current one.
	# Does not check if the tile is out of bounds or not.
	def randomAdjacentTile(self, spark):
		# Whether neighbour will be horizontally or vertically adjacent to spark.
		# 1 == horizontal, 0 == vertical
		horizontalOrVertical = randint(0,1)
		# Whether co-ordinates will be adjusted up or down.
		positiveOrNegative = randint(-1,1)

		# If horizontalOrVertical is 1 then return spark with positiveOrNegative added to the x co-ord else add it to the y co-ord.
		return [spark[0] + positiveOrNegative, spark[1]] if horizontalOrVertical == 1 else [spark[0], spark[1] + positiveOrNegative]

	def checkCompatibility(self, (x, y)):
		if not self.model.outOfBounds((x, y)) and self.model.getCell((x, y)).forestable:
			return True
		else:
			return False