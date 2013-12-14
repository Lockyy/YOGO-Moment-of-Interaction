import pygame
from Drawer import Drawer
from GameView import GameView
from SidebarView import SidebarView

class ViewController(object):

	def __init__(self, configManager):
		self.configManager = configManager

		pygame.init()

		self.setupWindow()

		self.drawer = Drawer(self.configManager)

		self.gameView = GameView(self.configManager, self.DISPLAYSURF, self.drawer)

		self.sideBarView = SidebarView(self.configManager, self.DISPLAYSURF, self.drawer)

	def setupWindow(self):
		self.DISPLAYSURF	= pygame.display.set_mode(self.configManager.RESOLUTION)

		windowTitle			= self.configManager.WINDOWTITLE

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

