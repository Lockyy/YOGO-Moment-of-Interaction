import Villager
import math
import random

class Village(object):

	def __init__(self, configManager, world):
		self.configManager = configManager
		self.world = world

		# Level of the village, will be used to determine how fast the village can grow.
		self.villageLevel = 1

		# Current population of the village.
		self.population = 0

		# Keep track of the live and dead villagers.
		self.villagers = []
		self.dead = {}

		# The village news log. Used for displaying the log in the sidebar.
		# Will also be output to a file at some point in the future.
		self.log = []

		# Keep track of which cells are owned by the village and what they are.
		self.villageCells = [self.world.focusCell]
		self.farms = []
		self.pastures = []

		self.villageCellCount = 1
		self.farmCount = 0
		self.pastureCount = 1

		# How many people each building should be able to support. Used for prioritising building.
		self.peoplePerFarm = 10
		self.peoplePerPasture = 10
		self.peoplePerVillageCell = 30

		# Initial village resources.
		# Lots of grain and fish for creating the initial villagers.
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

		# Keeps track of how "overdrawn" the village went the previous year.
		# Kills a villager for each overdrawn resource.
		self.materialShortage = 0
		self.grainShortage = 0
		self.proteinShortage = 0

		# Whether the village is dead or not.
		self.villageStatus = True

	# Creates 'count' villagers.
	# Consumes 2 grand and 3 protein per villager.
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

		# Split the remaining population into three sections.
		proteinGatherers = villagersForGathering[0:split]
		grainGatherers = villagersForGathering[split:split*2]
		materialGatherers = villagersForGathering[split*2:split*3]

		# Send them all off to gather resources.
		for gatherer in proteinGatherers:
			self.gatherProtein(gatherer)

		for gatherer in grainGatherers:
			self.gatherGrain(gatherer)

		for gatherer in materialGatherers:
			self.gatherMaterials(gatherer)

	def gatherProtein(self, gatherer):
		# Check around the villages buildings for a meat/fish gathering spot.
		best = 0
		bestCell = False
		fish = False
		meat = False
		
		buildings = self.villageCells + self.farms + self.pastures
		checkedCells = []

		# Check a 20x20 square around each building for resources.
		for building in buildings:
			for x in xrange(-10, 10):
				for y in xrange(-10, 10):
					cellX = building[0] + x
					cellY = building[1] + y

					cell = (cellX, cellY)

					# Make sure we only check each cell once.
					# Also pass on out of bounds cells
					if cell in checkedCells or self.world.outOfBounds(cell):
						continue
					else:
						checkedCells.append(cell)

					cellToCheck = self.world.getCell(cell)

					# Check if the cell has more meat/fish than the best cell found so far.
					# If so, record it's location and whether it was fish or meat it has.

					if cellToCheck.meat > best:
						best = cellToCheck.meat
						bestCell = cell
						meat = True
						fish = False

					if cellToCheck.fish > best:
						best = cellToCheck.fish
						bestCell = cell
						fish = True
						meat = False

		# Record the villagers shame in the village log.
		if best == 0:
			self.addToVillageLog(gatherer.name + " didn't get meat or fish")
		else:
			# Take the fish/meat from the best available cell and put it in the stores.
			# Record the gathering in the log.
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

		# Check every farm for which has the most grain. Gather from that farm.
		buildings = self.farms

		for building in buildings:
			cellX = building[0]
			cellY = building[1]
			
			if self.world.outOfBounds(building):
				continue

			cellToCheck = self.world.getCell(building)

			if cellToCheck.grain > best:
				best = cellToCheck.grain
				bestCell = building

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

	# Consumes resources to support village population.
	def consumeResources(self):
		consumptionLevel = int(math.ceil(float(self.population) / 10))

		self.consumeProtein(self.grainConsumption * consumptionLevel)
		self.consumeBuildingMaterials(self.buildingMaterialConsumption * consumptionLevel)
		self.consumeGrain(self.grainConsumption * consumptionLevel)

	# Births and deaths.
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

	# Build new buildings.
	# One building per year.
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

	# These functions return whether we can afford the various buildings, or a baby.

	def materialsForFarm(self):
		return self.buildingMaterials() >= 1 and self.grain >= 1

	def materialsForPasture(self):
		return self.buildingMaterials() >= 10 and self.grain >= 5

	def materialsForVillageCell(self):
		return self.buildingMaterials() >= 20 and self.grain >= 10

	def materialsForBaby(self):
		return self.grain >= 10 and self.protein() >= 15

	# Build a farm. Check around every existing structure for an open slot.
	def buildFarm(self):
		validLocations = []

		for x in range(-1, 1):
			for y in range(-1, 1):
				# Check around the villages.
				for village in self.villageCells:
					cellX = village[0] + x
					cellY = village[1] + y
					if self.world.getCell((cellX, cellY)).farmable:
						validLocations.append((cellX, cellY))
				else:
					# Around the farms.
					for farm in self.farms:
						cellX = farm[0] + x
						cellY = farm[1] + y
						if self.world.getCell((cellX, cellY)).farmable:
							validLocations.append((cellX, cellY))
					else:
						# And finally around the pastures.
						for pasture in self.pastures:
							cellX = pasture[0] + x
							cellY = pasture[1] + y
							if self.world.getCell((cellX, cellY)).farmable:
								validLocations.append((cellX, cellY))

		# Take a random valid location and place the farm there.
		try:						
			location = random.choice(validLocations)

			self.world.placeFarmCell(location)
			self.farms.append(location)
			self.farmCount += 1

			self.consumeGrain(1)
			self.consumeBuildingMaterials(1)
			self.addToVillageLog("Farm built.")
		except:
			return

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
		try:
			location = random.choice(validLocations)
			
			self.world.placePastureCell(location)
			self.pastures.append(location)
			self.pastureCount += 1

			self.consumeGrain(5)
			self.consumeBuildingMaterials(10)
			self.addToVillageLog("Pasture built.")
		except:
			return

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
		try:
			location = random.choice(validLocations)

			self.world.placeVillageCell(location)
			self.villageCells.append(location)
			self.villageCellCount += 1

			self.consumeGrain(10)
			self.consumeBuildingMaterials(20)
			self.addToVillageLog("Village hub built.")
		except: 
			return

	def buildingMaterials(self):
		return self.wood + self.stone

	def protein(self):
		return self.fish + self.meat

	def consumeProtein(self, requiredProtein):
		# Subtract the current level of fish from the required protein.
		leftOver = requiredProtein - self.fish

		# If we still need more protein then we have no fish left.
		if leftOver > 0:
			self.fish = 0
			# The shortage of protein we have is therefore the leftover.
			self.proteinShortage = leftOver
		# However if we have no leftover than we can fulfill our needs just from fish.
		else:
			# Subtract the required protein from fish and set our protein shortage to 0.
			self.fish -= requiredProtein
			self.proteinShortage = 0
			return

		# Now we do that again except with the meat.
		# If we still have a leftover after that then we actually have a protein shortage.
		requiredProtein = leftOver

		leftOver = requiredProtein - self.meat
		if leftOver > 0:
			self.meat = 0
			self.proteinShortage = requiredProtein - self.meat
		else:
			self.meat -= requiredProtein
			self.proteinShortage = 0

	# Same as above but with building materials.
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

	# Same as above but with grain.
	def consumeGrain(self, requiredGrain):

		leftOver = requiredGrain - self.grain
		if leftOver > 0:
			self.grain = 0
			self.grainShortage = requiredGrain - self.grain
		else:
			self.grain -= requiredGrain
			self.grainShortage = 0

	# Kill a random villager.
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

		# Bury their corpse in the dead dictionary.
		self.dead[villager] = deathString

		del self.villagers[self.villagers.index(villager)]

		self.population -= 1

		# Record their cause of death in the town log.
		self.addToVillageLog(villager.name + deathString)

	# Checks whether the village is dead or not.
	def checkVillageStatus(self):
		if self.population <= 0:
			return False
		else:
			return True

	# Put the message in the log.
	def addToVillageLog(self, message):
		self.log.append(message)

	# Get the last x messages from the log.
	def getLastXMessages(self, X):
		return self.log[-X:]