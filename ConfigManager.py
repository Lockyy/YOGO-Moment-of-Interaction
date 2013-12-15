import time
from ConfigParser import SafeConfigParser

class ConfigManager(object):

	SIDEBARWIDTH 	= 250
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

		print self.LANDPERCENTAGE

		self.MOUNTAINDIRECTIONCHANGECHANCE = int(self.configParser.get('World_Generation', 'mountain_direction_change_chance'))
		self.MOUNTAINLENGTHMAX = int(self.configParser.get('World_Generation', 'mountain_length_max'))
		self.MOUNTAINRANGECOUNT = int(self.configParser.get('World_Generation', 'mountain_range_count'))

		self.RIVERCOUNT = int(self.configParser.get('World_Generation', 'river_count'))

	def regenSeed(self):
		self.WORLDGENSEED = time.time()