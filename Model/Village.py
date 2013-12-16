import Villager
import math
import random

class Village(object):

	def __init__(self, configManager, world):
		self.configManager = configManager
		self.world = world

		self.villageLevel = 1

		self.population = 0

		self.villagers = []
		self.dead = {}
		self.log = []

		self.villageCells = [self.world.focusCell]
		self.farms = []
		self.pastures = []

		self.villageCellCount = 1
		self.farmCount = 0
		self.pastureCount = 1

		self.peoplePerFarm = 10
		self.peoplePerPasture = 10
		self.peoplePerVillageCell = 30

		self.wood = 1
		self.stone = 0
		self.grain = 31
		self.fish = 20
		self.meat = 1

		self.createVillagers(self.configManager.VILLAGEINITIALPOPULATION)

		# This consumption is per 10 population
		self.proteinConsumption = self.configManager.VILLAGECONSUMPTIONPROTEIN
		self.grainConsumption = self.configManager.VILLAGECONSUMPTIONGRAIN
		self.buildingMaterialConsumption = self.configManager.VILLAGECONSUMPTIONBUILDINGMATERIAL

		self.materialShortage = 0
		self.grainShortage = 0
		self.proteinShortage = 0

		self.villageStatus = True

	def createVillagers(self, count):
		for x in xrange(count):
			newVillager = Villager.Villager()
			self.villagers.append(newVillager)
			self.addToVillageLog(newVillager.name + "was born")
			self.consumeGrain(2)
			self.consumeProtein(3)
			self.population += 1

	def advanceYear(self):
		self.gatherResources()
		self.expandVillage()
		self.consumeResources()
		self.adjustPopulation()

		self.villageStatus = self.checkVillageStatus()

	def gatherResources(self):
		# A tenth of the village stays at the village
		villagersForGathering = random.sample(self.villagers, self.population - (self.population % 9))

		split = len(villagersForGathering) / 3

		proteinGatherers = villagersForGathering[0:split]
		grainGatherers = villagersForGathering[split:split*2]
		materialGatherers = villagersForGathering[split*2:split*3]

		for gatherer in proteinGatherers:
			self.gatherProtein(gatherer)

		for gatherer in grainGatherers:
			self.gatherGrain(gatherer)

		for gatherer in materialGatherers:
			self.gatherMaterials(gatherer)

	def gatherProtein(self, gatherer):
		best = 0
		bestCell = False
		fish = False
		meat = False
		
		for villageX in xrange(self.world.worldCellWidth):
			for villageY in xrange(self.world.worldCellHeight):
				if self.world.getCell((villageX, villageY)).name == "Village":
					for x in xrange(-10, 10):
						for y in xrange(-10, 10):
							cellX = villageX + x
							cellY = villageY + y

							if self.world.outOfBounds((cellX, cellY)):
								continue

							cellToCheck = self.world.getCell((cellX, cellY))

							if cellToCheck.meat > best:
								best = cellToCheck.meat
								bestCell = (cellX, cellY)
								meat = True
								fish = False

							if cellToCheck.fish > best:
								best = cellToCheck.fish
								bestCell = (cellX, cellY)
								fish = True
								meat = False

		if best == 0:
			self.addToVillageLog(gatherer.name + " didn't get meat or fish")
		else:
			if fish:
				self.world.getCell(bestCell).fish -= 1
				self.fish += 1
				self.addToVillageLog(gatherer.name + " caught fish")# at " + str(bestCell[0]) + "," + str(bestCell[1]))
			if meat:
				self.world.getCell(bestCell).meat -= 1
				self.meat += 1
				self.addToVillageLog(gatherer.name + " butchered meat")# at " + str(bestCell[0]) + "," + str(bestCell[1]))

	def gatherGrain(self, gatherer):
		best = 0
		bestCell = False

		for villageX in xrange(self.world.worldCellWidth):
			for villageY in xrange(self.world.worldCellHeight):
				if self.world.getCell((villageX, villageY)).name == "Village":
					for x in xrange(-10, 10):
						for y in xrange(-10, 10):
							cellX = villageX + x
							cellY = villageY + y
							
							if self.world.outOfBounds((cellX, cellY)):
								continue

							cellToCheck = self.world.getCell((cellX, cellY))

							if cellToCheck.grain > best:
								best = cellToCheck.grain
								bestCell = (cellX, cellY)

		if best == 0:
			self.addToVillageLog(gatherer.name + " didn't get grain")
		else:
			self.world.getCell(bestCell).grain -= 1
			self.grain += 1
			self.addToVillageLog(gatherer.name + " harvested grain")# at " + str(bestCell[0]) + "," + str(bestCell[1]))

	def gatherMaterials(self, gatherer):
		best = 0
		bestCell = False
		stone = False
		wood = False
		
		for villageX in xrange(self.world.worldCellWidth):
			for villageY in xrange(self.world.worldCellHeight):
				if self.world.getCell((villageX, villageY)).name == "Village":
					for x in xrange(-10, 10):
						for y in xrange(-10, 10):
							cellX = villageX + x
							cellY = villageY + y
							
							if self.world.outOfBounds((cellX, cellY)):
								continue

							cellToCheck = self.world.getCell((cellX, cellY))

							if cellToCheck.stone > best:
								best = cellToCheck.stone
								bestCell = (cellX, cellY)
								stone = True
								wood = False

							if cellToCheck.wood > best:
								best = cellToCheck.wood
								bestCell = (cellX, cellY)
								wood = True
								stone = False

		if best == 0:
			self.addToVillageLog(gatherer.name + " didn't get wood or stone")
		else:
			if stone:
				self.world.getCell(bestCell).stone -= 1
				self.stone += 1
				self.addToVillageLog(gatherer.name + " mined stone")# at " + str(bestCell[0]) + "," + str(bestCell[1]))
			if wood:
				self.world.getCell(bestCell).wood -= 1
				self.wood += 1
				self.addToVillageLog(gatherer.name + " gathered wood")# at " + str(bestCell[0]) + "," + str(bestCell[1]))


	def consumeResources(self):
		consumptionLevel = int(math.ceil(float(self.population) / 10))

		self.consumeProtein(self.grainConsumption * consumptionLevel)
		self.consumeBuildingMaterials(self.buildingMaterialConsumption * consumptionLevel)
		self.consumeGrain(self.grainConsumption * consumptionLevel)

	def adjustPopulation(self):
		if self.materialShortage > 0:
			for x in xrange(self.materialShortage):
				self.killVillager(0)

		if self.grainShortage > 0:
			for x in xrange(self.grainShortage):
				self.killVillager(1)

		if self.proteinShortage > 0:
			for x in xrange(self.proteinShortage):
				self.killVillager(2)

		while self.materialsForBaby():
			self.createVillagers(1)

	def expandVillage(self):
		if self.population > self.farmCount * self.peoplePerFarm and self.materialsForFarm():
			self.buildFarm()
			return
		if self.population > self.pastureCount * self.peoplePerPasture and self.materialsForPasture():
			self.buildPasture()
			return
		if self.population > self.villageCellCount * self.peoplePerVillageCell and self.materialsForVillageCell():
			self.buildVillage()
			return

	def materialsForFarm(self):
		return self.buildingMaterials() >= 1 and self.grain >= 1

	def materialsForPasture(self):
		return self.buildingMaterials() >= 10 and self.grain >= 5

	def materialsForVillageCell(self):
		return self.buildingMaterials() >= 20 and self.grain >= 10

	def materialsForBaby(self):
		return self.grain >= 10 and self.protein() >= 15

	def buildFarm(self):
		validLocations = []

		for x in range(-1, 1):
			for y in range(-1, 1):
				for village in self.villageCells:
					cellX = village[0] + x
					cellY = village[1] + y
					if self.world.getCell((cellX, cellY)).farmable:
						validLocations.append((cellX, cellY))
				else:
					for farm in self.farms:
						cellX = farm[0] + x
						cellY = farm[1] + y
						if self.world.getCell((cellX, cellY)).farmable:
							validLocations.append((cellX, cellY))
					else:
						for pasture in self.pastures:
							cellX = pasture[0] + x
							cellY = pasture[1] + y
							if self.world.getCell((cellX, cellY)).farmable:
								validLocations.append((cellX, cellY))

		location = random.choice(validLocations)

		self.world.placeFarmCell(location)
		self.farms.append(location)
		self.farmCount += 1

		self.consumeGrain(1)
		self.consumeBuildingMaterials(1)
		self.addToVillageLog("Farm built.")

	def buildPasture(self):
		validLocations = []
		for x in range(-1, 1):
			for y in range(-1, 1):
				for village in self.villageCells:
					cellX = village[0] + x
					cellY = village[1] + y
					if self.world.getCell((cellX, cellY)).farmable:
						validLocations.append((cellX, cellY))
				else:
					for farm in self.farms:
						cellX = farm[0] + x
						cellY = farm[1] + y
						if self.world.getCell((cellX, cellY)).farmable:
							validLocations.append((cellX, cellY))
					else:
						for pasture in self.pastures:
							cellX = pasture[0] + x
							cellY = pasture[1] + y
							if self.world.getCell((cellX, cellY)).farmable:
								validLocations.append((cellX, cellY))

		location = random.choice(validLocations)
		
		self.world.placePastureCell(location)
		self.pastures.append(location)
		self.pastureCount += 1

		self.consumeGrain(5)
		self.consumeBuildingMaterials(10)
		self.addToVillageLog("Pasture built.")

	def buildVillage(self):
		validLocations = []

		for x in range(-1, 1):
			for y in range(-1, 1):
				for village in self.villageCells:
					cellX = village[0] + x
					cellY = village[1] + y
					if self.world.getCell((cellX, cellY)).passable:
						validLocations.append((cellX, cellY))
				else:
					for farm in self.farms:
						cellX = farm[0] + x
						cellY = farm[1] + y
						if self.world.getCell((cellX, cellY)).passable:
							validLocations.append((cellX, cellY))
					else:
						for pasture in self.pastures:
							cellX = pasture[0] + x
							cellY = pasture[1] + y
							if self.world.getCell((cellX, cellY)).farmable:
								validLocations.append((cellX, cellY))

		self.world.placeVillageCell(location)
		self.villageCells.append(location)
		self.villageCellCount += 1

		self.consumeGrain(10)
		self.consumeBuildingMaterials(20)
		self.addToVillageLog("Village hub built.")

	def buildingMaterials(self):
		return self.wood + self.stone

	def protein(self):
		return self.fish + self.meat

	def consumeProtein(self, requiredProtein):

		leftOver = requiredProtein - self.fish
		if leftOver > 0:
			self.fish = 0
			self.proteinShortage = requiredProtein - self.fish
		else:
			self.fish -= requiredProtein
			self.proteinShortage = 0

		requiredProtein = leftOver

		if requiredProtein > 0:
			leftOver = requiredProtein - self.meat
			if leftOver > 0:
				self.meat = 0
				self.proteinShortage = requiredProtein - self.meat
			else:
				self.meat -= requiredProtein
				self.proteinShortage = 0

	def consumeBuildingMaterials(self, requiredBuildingMaterials):

		leftOver = requiredBuildingMaterials - self.stone
		if leftOver > 0:
			self.stone = 0
			self.materialShortage = requiredBuildingMaterials - self.stone
		else:
			self.stone -= requiredBuildingMaterials
			self.materialShortage = 0

		requiredBuildingMaterials = leftOver

		if requiredBuildingMaterials > 0:
			leftOver = requiredBuildingMaterials - self.wood
			if leftOver > 0:
				self.wood = 0
				self.materialShortage = requiredBuildingMaterials - self.wood
			else:
				self.wood -= requiredBuildingMaterials
				self.materialShortage = 0

	def consumeGrain(self, requiredGrain):

		leftOver = requiredGrain - self.grain
		if leftOver > 0:
			self.grain = 0
			self.grainShortage = requiredGrain - self.grain
		else:
			self.grain -= requiredGrain
			self.grainShortage = 0

	def killVillager(self, causeOfDeath):
		if self.population == 0:
			return

		villager = random.choice(self.villagers)

		if causeOfDeath == 0:
			deathString = " died in the streets."
		elif causeOfDeath == 1:
			deathString = " starved to death."
		elif causeOfDeath == 2:
			deathString = " wasted away."

		self.dead[villager] = deathString

		del self.villagers[self.villagers.index(villager)]

		self.population -= 1

		self.addToVillageLog(villager.name + deathString)

	def checkVillageStatus(self):
		if self.population <= 0:
			return False
		else:
			return True

	def addToVillageLog(self, message):
		self.log.append(message)

	def getLastXMessages(self, X):
		return self.log[-X:]