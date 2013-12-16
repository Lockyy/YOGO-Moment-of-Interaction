import View
import pygame
import Colours

class SidebarView(View.View):

	def __init__(self, configManager, MAINDISPLAYSURF, drawer):
		super(SidebarView, self).__init__(configManager, MAINDISPLAYSURF, drawer)

		self.TOPLEFT = (self.configManager.WINDOWWIDTH - self.configManager.SIDEBARWIDTH, 0)

		self.HEIGHT = self.configManager.WINDOWHEIGHT

		self.DISPLAYSURF = pygame.Surface((self.configManager.SIDEBARWIDTH, self.configManager.WINDOWHEIGHT))

		self.FPSFONTSIZE = 10
		self.SIDEBARFONTSIZE = 15
		self.BORDER = 10
		self.ROWHEIGHT = self.SIDEBARFONTSIZE + 5

	def update(self, model):
		colour = Colours.SIDEBARBACKGROUND
		self.drawer.fill(self.DISPLAYSURF, colour)

		self.drawMessages(model)

		self.drawToMainDisplay()

	def drawMessages(self, model):
		self.drawer.drawText(self.configManager.currentFPS, self.DISPLAYSURF, (0,0), fontSize = self.FPSFONTSIZE)

		messages = {}

		if not model.world.worldGenDone:
			messages[1] = "Generating"
			messages[2] = model.world.worldGenStageMessage
		else:
			focusCell = model.world.getFocusCell()

			yearString = "Year " + str(model.world.year)

			if model.gamePaused:
				yearString += " (Paused)"

			messages[1] = yearString
			messages[2] = str(model.world.focusCell[0]) + ", " + str(model.world.focusCell[1])
			messages[3] = "Terrain:"
			messages[4] = focusCell.name

			if focusCell.name == "Village":
				del messages[3]
				messages[6] = "Level: " + str(model.village.villageLevel)
				messages[7] = "Population: " + str(model.village.population)
				messages[9] = "Building Materials: " + str(model.village.buildingMaterials())
				messages[10] = "Grain: " + str(model.village.grain)
				messages[11] = "Food: " + str(model.village.protein())

				logMessagesToDisplay = 20
				villageLog = model.village.getLastXMessages(logMessagesToDisplay)

				for x in xrange(0, logMessagesToDisplay):
					try:
						messages[x + 15] = villageLog[x]
					except:
						pass
			else:
				messages[9] = "Wood: " + str(focusCell.wood)
				messages[10] = "Stone: " + str(focusCell.stone)
				messages[11] = "Grain: " + str(focusCell.grain)
				messages[12] = "Meat: " + str(focusCell.meat)
				messages[13] = "Fish: " + str(focusCell.fish)

		self.drawMessageDictionary(messages)

	def drawMessageDictionary(self, messages):
		for key in messages:
			self.drawer.drawText(messages[key], self.DISPLAYSURF, (self.BORDER, self.ROWHEIGHT * key), fontSize = self.SIDEBARFONTSIZE)