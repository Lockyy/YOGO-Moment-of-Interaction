import View
import pygame
import Colours

class GameView(View.View):

	def __init__(self, configManager, MAINDISPLAYSURF, drawer):
		super(GameView, self).__init__(configManager, MAINDISPLAYSURF, drawer)

		self.TOPLEFT = (0,0)

		self.HEIGHT = self.configManager.WINDOWHEIGHT
		self.WIDTH = self.configManager.WINDOWWIDTH - self.configManager.SIDEBARWIDTH

		self.DISPLAYSURF = pygame.Surface((self.WIDTH, self.HEIGHT))

	def update(self, model):
		colour = Colours.GAMEBACKGROUND
		self.drawer.fill(self.DISPLAYSURF, colour)

		self.drawToMainDisplay()