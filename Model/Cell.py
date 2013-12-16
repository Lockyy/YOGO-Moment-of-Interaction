from View import Colours
from random import randint

class Cell(object):
	
	def __init__(self, configManager):
		self.configManager = configManager

		self.name 			= "Empty"
		self.colour 		= Colours.RIVER

		self.revertsTo		= self

		self.passable 		= False
		self.farmable 		= False
		self.land			= True
		self.mountain 		= False
		self.water			= False
		self.riverPassable	= True
		self.fishable		= False
		self.forestable		= False

		self.lastColourDisplayed = False
		self.changed = True

		self.meat = 0
		self.grain = 0
		self.fish = 0
		self.wood = 0
		self.stone = 0

		self.minMeatRegen = 0
		self.minGrainRegen = 0
		self.minFishRegen = 0
		self.minWoodRegen = 0
		self.minStoneRegen = 0
		self.maxMeatRegen = 0
		self.maxGrainRegen = 0
		self.maxFishRegen = 0
		self.maxWoodRegen = 0
		self.maxStoneRegen = 0

		self.meatLimit = 0
		self.grainLimit = 0
		self.fishLimit = 0
		self.woodLimit = 0
		self.stoneLimit = 0

	def compareType(self, name):
		if name == self.name:
			return True
		else:
			return False

	def regenResources(self):
		if self.meat < self.meatLimit:
			meat = randint(self.minMeatRegen, self.maxMeatRegen)
			self.meat += meat
		if self.grain < self.grainLimit:
			grain = randint(self.minGrainRegen, self.maxGrainRegen)
			self.grain += grain
		if self.fish < self.fishLimit:
			fish = randint(self.minFishRegen, self.maxFishRegen)
			self.fish += fish
		if self.wood < self.woodLimit:
			wood = randint(self.minWoodRegen, self.maxWoodRegen)
			self.wood += wood
		if self.stone < self.stoneLimit:
			stone = randint(self.minStoneRegen, self.maxStoneRegen)
			self.stone += stone

class GrasslandCell(Cell):
	
	def __init__(self, configManager):
		Cell.__init__(self, configManager)

		self.name 		= "Grasslands"
		self.colour 	= Colours.GRASSLAND
		self.passable 	= True
		self.farmable 	= True
		self.forestable = True

		minMeat = self.configManager.GRASSLANDMEATMIN
		maxMeat = self.configManager.GRASSLANDMEATMAX

		self.meat = self.meatLimit = randint(minMeat, maxMeat)

		self.minMeatRegen = self.configManager.GRASSLANDMEATREGENMIN
		self.maxMeatRegen = self.configManager.GRASSLANDMEATREGENMAX

class DesertCell(Cell):
	
	def __init__(self, configManager):
		Cell.__init__(self, configManager)

		self.name 			= "Desert"
		self.colour 		= Colours.DESERT
		self.passable 		= True
		self.riverPassable	= False

class MountainCell(Cell):
	
	def __init__(self, configManager):
		Cell.__init__(self, configManager)

		self.name 		= "Mountain"
		self.colour 	= Colours.MOUNTAIN
		self.mountain 	= True

		minStone = self.configManager.MOUNTAINSTONEMIN
		maxStone = self.configManager.MOUNTAINSTONEMAX

		self.stone = self.stoneLimit = randint(minStone, maxStone)

		self.minStoneRegen = self.configManager.MOUNTAINSTONEREGENMIN
		self.maxStoneRegen = self.configManager.MOUNTAINSTONEREGENMAX

class RiverCell(Cell):

	def __init__(self, configManager):
		Cell.__init__(self, configManager)

		self.name 		= "River"
		self.colour 	= Colours.RIVER
		self.water 		= True
		self.land		= False
		self.fishable	= True

		minFish = self.configManager.RIVERFISHMIN
		maxFish = self.configManager.RIVERFISHMAX

		self.fish = self.fishLimit = randint(minFish, maxFish)

		self.minFishRegen = self.configManager.RIVERFISHREGENMIN
		self.maxFishRegen = self.configManager.RIVERFISHREGENMAX

class LakeCell(Cell):

	def __init__(self, configManager):
		Cell.__init__(self, configManager)

		self.name 		= "Lake"
		self.colour 	= Colours.RIVER
		self.water 		= True
		self.land		= False
		self.fishable	= True

		minFish = self.configManager.LAKEFISHMIN
		maxFish = self.configManager.LAKEFISHMAX

		self.fish = self.fishLimit = randint(minFish, maxFish)

		self.minFishRegen = self.configManager.LAKEFISHREGENMIN
		self.maxFishRegen = self.configManager.LAKEFISHREGENMAX

class OOBCell(Cell):

	def __init__(self, configManager):
		Cell.__init__(self, configManager)

		self.name 		= "OOB"
		self.colour 	= Colours.RIVER
		self.water 		= False
		self.land		= False

class ForestCell(Cell):
	
	def __init__(self, configManager):
		Cell.__init__(self, configManager)

		self.name 		= "Forest"
		self.colour 	= Colours.FOREST
		self.passable 	= True
		self.farmable 	= True

		minWood = self.configManager.FORESTWOODMIN
		maxWood = self.configManager.FORESTWOODMAX

		self.wood = self.woodLimit = randint(minWood, maxWood)

		self.minWoodRegen = self.configManager.FORESTWOODREGENMIN
		self.maxWoodRegen = self.configManager.FORESTWOODREGENMAX

class FarmCell(Cell):

	def __init__(self, configManager):
		Cell.__init__(self, configManager)

		self.name		= "Farm"
		self.colour 	= Colours.FARM

		minGrain = self.configManager.FARMGRAINMIN
		maxGrain = self.configManager.FARMGRAINMAX

		self.grain = self.grainLimit = randint(minGrain, maxGrain)

		self.minGrainRegen = self.configManager.FARMGRAINREGENMIN
		self.maxGrainRegen = self.configManager.FARMGRAINREGENMAX

class PastureCell(Cell):

	def __init__(self, configManager):
		Cell.__init__(self, configManager)

		self.name		= "Pasture"
		self.colour 	= Colours.PASTURE

		minMeat = self.configManager.PASTUREMEATMIN
		maxMeat = self.configManager.PASTUREMEATMAX

		self.meat = self.meatLimit = randint(minMeat, maxMeat)

		self.minMeatRegen = self.configManager.PASTUREMEATREGENMIN
		self.maxMeatRegen = self.configManager.PASTUREMEATREGENMAX	

class VillageCell(Cell):

	def __init__(self, configManager):
		Cell.__init__(self, configManager)

		self.name		= "Village"
		self.colour 	= Colours.VILLAGE
		self.passable 	= True