import View
import pygame
import Colours

class SidebarView(View.View):

	def __init__(self, configParser, MAINDISPLAYSURF, drawer, SIDEBARWIDTH, TOPLEFT):
		super(SidebarView, self).__init__(configParser, MAINDISPLAYSURF, drawer, SIDEBARWIDTH)

		self.TOPLEFT = TOPLEFT

		self.HEIGHT = int(self.configParser.get('UI', 'resolution_height'))

		self.DISPLAYSURF = pygame.Surface((self.SIDEBARWIDTH, self.HEIGHT))

	def update(self, model):
		colour = Colours.SIDEBARBACKGROUND
		self.drawer.fill(self.DISPLAYSURF, colour)

		self.drawToMainDisplay()