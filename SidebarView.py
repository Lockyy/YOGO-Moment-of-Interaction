import View
import pygame
import Colours

class SidebarView(View.View):

	def __init__(self, configManager, MAINDISPLAYSURF, drawer):
		super(SidebarView, self).__init__(configManager, MAINDISPLAYSURF, drawer)

		self.TOPLEFT = (self.configManager.WINDOWWIDTH - self.configManager.SIDEBARWIDTH, 0)

		self.HEIGHT = self.configManager.WINDOWHEIGHT

		self.DISPLAYSURF = pygame.Surface((self.configManager.SIDEBARWIDTH, self.configManager.WINDOWHEIGHT))

	def update(self, model):
		colour = Colours.SIDEBARBACKGROUND
		self.drawer.fill(self.DISPLAYSURF, colour)

		self.drawMessages(model)

		self.drawToMainDisplay()

	def drawMessages(self, model):
		focusCell = model.getFocusCell()

		message = focusCell.name
		self.drawer.drawText("Terrain:", self.DISPLAYSURF, (10, 10))
		self.drawer.drawText(message, self.DISPLAYSURF, (10, 42))