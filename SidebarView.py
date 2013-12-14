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

		self.drawToMainDisplay()