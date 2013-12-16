import random
import math
import pygame
import Cell
from random import randint
from ConfigParser import SafeConfigParser

class MountainFactory(object):

	def __init__(self, model, configManager):
		self.model = model
		self.configManager = configManager

		random.seed(configManager.WORLDGENSEED)

	# Add a single mountain range.
	def createMountainRange(self):
		# Get length of range.
		actualRangeLength = self.getActualRangeLength()

		# Place the first mountain of the range.
		lastMountainPlaced = initialMountain = self.placeInitialMountain()

		# Record that one mountain has been placed.
		mountainsPlaced = 1

		# Get direction mountain range will move in.
		horizontalOffset, verticalOffset = self.getNewDirection(0,0)

		# Ensures we don't get stuck in this loop forever.
		acceptableTries = actualRangeLength * 20
		loops = 0

		# Whilst we still have mountains to place.
		while mountainsPlaced < actualRangeLength and loops < acceptableTries:
			# Get new mountain co-ordinates.
			newMountainCoords = [lastMountainPlaced[0] + horizontalOffset, lastMountainPlaced[1] + verticalOffset]

			if not self.model.outOfBounds(newMountainCoords):

				# Get tile at new mountain co-ordinates.
				newMountainTile = self.model.getCell(newMountainCoords)
				# Try to add the mountain, if it's successful then set last mountain placed, the alignment of it's new tile
				# and the amount of mountains placed.
				
				if newMountainTile.land and not newMountainTile.mountain:
					self.model.placeMountainCell(newMountainCoords)
					lastMountainPlaced = newMountainCoords
					mountainsPlaced += 1

				# Get new direction, if randint(0,100) isn't within correct range, will just return existing direction.
				horizontalOffset, verticalOffset = self.getNewDirection(0,0, randint(0,100))

			# Increase loop counter.
			loops += 1


	def getActualRangeLength(self):
		# Max size of mountain ranges.
		minRangeLength = int(self.configManager.MOUNTAINLENGTHMIN)
		maxRangeLength = int(self.configManager.MOUNTAINLENGTHMAX)

		if minRangeLength >= maxRangeLength:
			actualRangeLength = minRangeLength
		else:
			actualRangeLength = randint(minRangeLength, maxRangeLength)

		return actualRangeLength

	def placeInitialMountain(self):
		firstMountain = [randint(0, self.model.worldCellWidth - 1), randint(0, self.model.worldCellHeight - 1)]
		firstMountainTile = self.model.getCell(firstMountain)
		while self.model.outOfBounds(firstMountain) and firstMountainTile.land:
			firstMountain = [randint(0, self.model.worldCellWidth - 1), randint(0, self.model.worldCellHeight - 1)]
			firstMountainTile = self.model.getCell(firstMountain)

		self.model.placeMountainCell(firstMountain)

		return firstMountain

	def getNewDirection(self, horizontal, vertical, diceRoll = False):
		directionChangeChance = self.configManager.MOUNTAINDIRECTIONCHANGECHANCE

		if diceRoll == False:
			diceRoll = directionChangeChance + 1
		if diceRoll <= directionChangeChance:
			return horizontal, vertical

		newHorizontal = newVertical = 0

		while newHorizontal == horizontal and newVertical == vertical or (newHorizontal == 0 and newVertical == 0):
			newHorizontal = randint(-1,1)
			newVertical = randint(-1,1)

		return newHorizontal, newVertical