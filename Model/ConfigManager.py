import time
from ConfigParser import SafeConfigParser

class ConfigManager(object):

	SIDEBARWIDTH 	= 300
	MINIMUMWIDTH 	= 1280
	MINIMUMHEIGHT 	= 800

	def __init__(self):
		# Get the config file. This stores any non-world generation settings.
		# Including filepath for default world gen settings.
		self.configParser = SafeConfigParser()
		self.configParser.read('data/settings/config.ini')

		# Get the window's height and ensure it's at least the MINIMUMHEIGHT
		self.WINDOWHEIGHT 	= int(self.configParser.get('UI', 'resolution_height'))

		if self.WINDOWHEIGHT < self.MINIMUMHEIGHT:
			self.WINDOWHEIGHT = self.MINIMUMHEIGHT

		# Get the window's width and ensure it's at least the MINIMUMWIDTH
		self.WINDOWWIDTH	= int(self.configParser.get('UI', 'resolution_width'))
		if self.WINDOWWIDTH < self.MINIMUMWIDTH:
			self.WINDOWWIDTH = self.MINIMUMWIDTH 

		# Size of the cells representing the game world's cells.
		self.CELLSIZE 		= int(self.configParser.get('UI', 'cell_size'))

		# Adjust the window size to conform the the size of cells so things fit in neatly.
		widthRemainder = (self.WINDOWWIDTH - self.SIDEBARWIDTH) % self.CELLSIZE
		self.WINDOWWIDTH -= widthRemainder

		heightRemainder = self.WINDOWHEIGHT % self.CELLSIZE
		self.WINDOWHEIGHT -= heightRemainder

		# Tuple of the windows resolution
		self.RESOLUTION 	= (self.WINDOWWIDTH, self.WINDOWHEIGHT)

		self.BORDERSIZE		= int(self.configParser.get('UI', 'border_size'))

		self.WORLDDISPLAYHEIGHT = self.WINDOWHEIGHT - self.BORDERSIZE * 2
		self.WORLDDISPLAYWIDTH 	= self.WINDOWWIDTH - self.SIDEBARWIDTH - self.BORDERSIZE * 2

		self.WINDOWTITLE 	= self.configParser.get('Text', 'window_title')

		# Seed the random number generator.
		seed = self.configParser.get('World_Generation', 'seed')
		
		if seed == "None": 
			self.WORLDGENSEED = time.time()
		else:
			self.WORLDGENSEED = int(seed)

		self.FPS = int(self.configParser.get('Game', 'fps'))

		self.SPARKSCONSTANT = int(self.configParser.get('World_Generation', 'spark_constant'))
		self.LANDPERCENTAGE = float(self.configParser.get('World_Generation', 'land_percentage')) / 100

		self.FARMGRAINMIN = int(self.configParser.get('World_Generation', 'farm_grain_min'))
		self.FARMGRAINMAX = int(self.configParser.get('World_Generation', 'farm_grain_max'))
		self.FARMGRAINREGENMIN = int(self.configParser.get('World_Generation', 'farm_grain_regen_min'))
		self.FARMGRAINREGENMAX = int(self.configParser.get('World_Generation', 'farm_grain_regen_max'))

		self.PASTUREMEATMIN = int(self.configParser.get('World_Generation', 'pasture_meat_min'))
		self.PASTUREMEATMAX = int(self.configParser.get('World_Generation', 'pasture_meat_max'))
		self.PASTUREMEATREGENMIN = int(self.configParser.get('World_Generation', 'pasture_meat_regen_min'))
		self.PASTUREMEATREGENMAX = int(self.configParser.get('World_Generation', 'pasture_meat_regen_max'))

		self.GRASSLANDMEATMIN = int(self.configParser.get('World_Generation', 'grassland_meat_min'))
		self.GRASSLANDMEATMAX = int(self.configParser.get('World_Generation', 'grassland_meat_max'))
		self.GRASSLANDMEATREGENMIN = int(self.configParser.get('World_Generation', 'grassland_meat_regen_min'))
		self.GRASSLANDMEATREGENMAX = int(self.configParser.get('World_Generation', 'grassland_meat_regen_max'))

		self.MOUNTAINDIRECTIONCHANGECHANCE = int(self.configParser.get('World_Generation', 'mountain_direction_change_chance'))
		self.MOUNTAINLENGTHMIN = int(self.configParser.get('World_Generation', 'mountain_length_min'))
		self.MOUNTAINLENGTHMAX = int(self.configParser.get('World_Generation', 'mountain_length_max'))
		self.MOUNTAINRANGECOUNT = int(self.configParser.get('World_Generation', 'mountain_range_count'))
		self.MOUNTAINSTONEMIN = int(self.configParser.get('World_Generation', 'mountain_stone_min'))
		self.MOUNTAINSTONEMAX = int(self.configParser.get('World_Generation', 'mountain_stone_max'))
		self.MOUNTAINSTONEREGENMIN = int(self.configParser.get('World_Generation', 'mountain_stone_regen_min'))
		self.MOUNTAINSTONEREGENMAX = int(self.configParser.get('World_Generation', 'mountain_stone_regen_max'))

		self.RIVERCOUNT = int(self.configParser.get('World_Generation', 'river_count'))
		self.RIVERFISHMIN = int(self.configParser.get('World_Generation', 'river_fish_min'))
		self.RIVERFISHMAX = int(self.configParser.get('World_Generation', 'river_fish_max'))
		self.RIVERFISHREGENMIN = int(self.configParser.get('World_Generation', 'river_fish_regen_min'))
		self.RIVERFISHREGENMAX = int(self.configParser.get('World_Generation', 'river_fish_regen_max'))

		self.LAKEFISHMIN = int(self.configParser.get('World_Generation', 'lake_fish_min'))
		self.LAKEFISHMAX = int(self.configParser.get('World_Generation', 'lake_fish_max'))
		self.LAKEFISHREGENMIN = int(self.configParser.get('World_Generation', 'lake_fish_regen_min'))
		self.LAKEFISHREGENMAX = int(self.configParser.get('World_Generation', 'lake_fish_regen_max'))

		self.FORESTCOUNT = int(self.configParser.get('World_Generation', 'forest_count'))
		self.FORESTSIZEMIN = int(self.configParser.get('World_Generation', 'forest_size_min'))
		self.FORESTSIZEMAX = int(self.configParser.get('World_Generation', 'forest_size_max'))
		self.FORESTWOODMIN = int(self.configParser.get('World_Generation', 'forest_wood_min'))
		self.FORESTWOODMAX = int(self.configParser.get('World_Generation', 'forest_wood_max'))
		self.FORESTWOODREGENMIN = int(self.configParser.get('World_Generation', 'forest_wood_regen_min'))
		self.FORESTWOODREGENMAX = int(self.configParser.get('World_Generation', 'forest_wood_regen_max'))

		self.VILLAGEINITIALPOPULATION = int(self.configParser.get('World_Generation', 'village_initial_population'))
		self.VILLAGECONSUMPTIONGRAIN = int(self.configParser.get('World_Generation', 'village_consumption_grain'))
		self.VILLAGECONSUMPTIONPROTEIN = int(self.configParser.get('World_Generation', 'village_consumption_protein'))
		self.VILLAGECONSUMPTIONBUILDINGMATERIAL = int(self.configParser.get('World_Generation', 'village_consumption_buildingMaterial'))

	def regenSeed(self):
		self.WORLDGENSEED = time.time()