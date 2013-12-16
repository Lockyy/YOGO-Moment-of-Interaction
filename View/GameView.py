import pygame
import Colours
import View

class GameView(View.View):

	def __init__(self, configManager, MAINDISPLAYSURF, drawer):
		super(GameView, self).__init__(configManager, MAINDISPLAYSURF, drawer)

		self.TOPLEFT = (self.configManager.BORDERSIZE, self.configManager.BORDERSIZE)

		self.DISPLAYSURF = pygame.Surface((self.configManager.WORLDDISPLAYWIDTH, self.configManager.WORLDDISPLAYHEIGHT))

	def update(self, model):
		colour = Colours.GAMEBACKGROUND
		# self.drawer.fill(self.DISPLAYSURF, colour)

		self.drawWorld(model)	

		if model.world.worldGenDone:
			self.drawFocusCellBox(model)

		self.drawToMainDisplay()

	def drawWorld(self, model):
		BORDER = self.configManager.BORDERSIZE
		CELLSIZE = self.configManager.CELLSIZE

		for x in xrange(model.world.worldCellWidth):
			for y in xrange(model.world.worldCellHeight):
				colour = model.world.getCellColour((x, y))

				location = ((CELLSIZE * x), (CELLSIZE * y))

				if model.world.cellChanged((x, y)):
					self.drawer.drawCell(self.DISPLAYSURF, colour, location)

				model.world.setCellChanged((x, y), False)

	def drawFocusCellBox(self, model):
		focusCell = model.world.focusCell

		cellsize = self.configManager.CELLSIZE

		rect = (focusCell[0] * cellsize, focusCell[1] * cellsize, cellsize - 1, cellsize - 1)

		pygame.draw.rect(self.DISPLAYSURF, Colours.FOCUSCELL, rect, 2)