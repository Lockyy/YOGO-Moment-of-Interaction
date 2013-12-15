import Colours

class Cell(object):
	
	def __init__(self):
		self.name 			= "Empty"
		self.colour 		= Colours.EMPTY
		self.passable 		= False
		self.farmable 		= False
		self.land			= True
		self.mountain 		= False
		self.water			= False
		self.riverPassable	= True
		self.fishable		= False

		self.lastColourDisplayed = False
		self.changed = True

	def compareType(self, name):
		if name == self.name:
			return True
		else:
			return False

class GrasslandCell(Cell):
	
	def __init__(self):
		Cell.__init__(self)

		self.name 		= "Grasslands"
		self.colour 	= Colours.GRASSLAND
		self.passable 	= True
		self.farmable 	= True

class DesertCell(Cell):
	
	def __init__(self):
		Cell.__init__(self)

		self.name 			= "Desert"
		self.colour 		= Colours.DESERT
		self.passable 		= True
		self.riverPassable	= False

class MountainCell(Cell):
	
	def __init__(self):
		Cell.__init__(self)

		self.name 		= "Mountain"
		self.colour 	= Colours.MOUNTAIN
		self.mountain 	= True

class RiverCell(Cell):

	def __init__(self):
		Cell.__init__(self)

		self.name 		= "River"
		self.colour 	= Colours.RIVER
		self.water 		= True
		self.land		= False
		self.fishable	= True

class LakeCell(Cell):

	def __init__(self):
		Cell.__init__(self)

		self.name 		= "Lake"
		self.colour 	= Colours.RIVER
		self.water 		= True
		self.land		= False
		self.fishable	= True

class OOBCell(Cell):

	def __init__(self):
		Cell.__init__(self)

		self.name 		= "OOB"
		self.colour 	= Colours.RIVER
		self.water 		= True
		self.land		= False