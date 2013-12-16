import World
import Village

class Model(object):

	def __init__(self, configManager):
		self.configManager = configManager

		self.gamePaused = False
		self.villagePlaced = False

		self.world = World.World(self.configManager)

	def updateWorld(self):
		if not self.gamePaused and self.villagePlaced and self.village.villageStatus:
			self.village.advanceYear()
			self.world.advanceYear()

	def placeVillage(self):
		self.village = Village.Village(self.configManager, self.world)
		self.world.placeInitialVillage()