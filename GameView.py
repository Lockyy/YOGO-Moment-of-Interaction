import View
import pygame
import Colours

class GameView(View.View):

	def __init__(self, configParser, MAINDISPLAYSURF, drawer, SIDEBARWIDTH):
		super(GameView, self).__init__(configParser, MAINDISPLAYSURF, drawer, SIDEBARWIDTH)

		self.TOPLEFT = (0,0)

		self.HEIGHT = int(self.configParser.get('UI', 'resolution_height'))
		self.WIDTH = int(self.configParser.get('UI', 'resolution_width'))

		self.DISPLAYSURF = pygame.Surface((self.WIDTH - 200, self.HEIGHT))

	def update(self, model):
		colour = Colours.GAMEBACKGROUND
		self.drawer.fill(self.DISPLAYSURF, colour)

		self.drawToMainDisplay()