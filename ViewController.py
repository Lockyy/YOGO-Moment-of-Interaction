import pygame
from Drawer import Drawer
from GameView import GameView
from SidebarView import SidebarView

class ViewController(object):

	SIDEBARWIDTH 	= 300
	MINIMUMWIDTH 	= 1280
	MINIMUMHEIGHT 	= 800

	def __init__(self, configParser):
		self.configParser = configParser

		pygame.init()

		self.setupWindow()

		self.drawer = Drawer(self.configParser)

		self.gameView = GameView(self.configParser, self.DISPLAYSURF, self.drawer, self.SIDEBARWIDTH)

		windowWidth	= int(self.configParser.get('UI', 'resolution_width'))

		TOPLEFT = (windowWidth - self.SIDEBARWIDTH, 0)

		self.sideBarView = SidebarView(self.configParser, self.DISPLAYSURF, self.drawer, self.SIDEBARWIDTH, TOPLEFT)

	def setupWindow(self):
		windowHeight 		= int(self.configParser.get('UI', 'resolution_height'))
		windowWidth			= int(self.configParser.get('UI', 'resolution_width'))

		if windowHeight < self.MINIMUMHEIGHT:
			windowHeight = self.MINIMUMHEIGHT

		if windowWidth < self.MINIMUMWIDTH:
			windowWidth = self.MINIMUMWIDTH

		self.DISPLAYSURF	= pygame.display.set_mode((windowWidth, windowHeight))

		windowTitle			= self.configParser.get('Text', 'window_title')

		pygame.display.set_caption(windowTitle)

	def updateView(self, model):
		# Fill in the background
		#self.drawer.fill(self.DISPLAYSURF)

		# Draw the game world
		self.gameView.update(model)

		# Draw in the sidebar
		self.sideBarView.update(model)

		# Update the display
		pygame.display.update()

