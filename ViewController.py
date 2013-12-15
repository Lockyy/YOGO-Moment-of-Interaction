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

	def updateView(self, model, updateUI):
		# Draw in the sidebar
		if updateUI:
			# Fill in the background
			self.drawer.fill(self.DISPLAYSURF)
			self.sideBarView.update(model)

		# Draw the game world
		self.gameView.update(model)

		# Update the display
		pygame.display.update()

	def getGameViewRect(self):
		gameViewLocation = self.gameView.TOPLEFT
		gameViewRect = pygame.Rect(	gameViewLocation[0],\
									gameViewLocation[1],\
									self.configManager.WORLDDISPLAYWIDTH,\
									self.configManager.WORLDDISPLAYHEIGHT)

		return gameViewRect

	def getClickedCell(self, (mousex, mousey)):
		if not self.getGameViewRect().collidepoint((mousex, mousey)):
			return False

		mousex -= self.configManager.BORDERSIZE
		mousey -= self.configManager.BORDERSIZE

		cellx = mousex / self.configManager.CELLSIZE
		celly = mousey / self.configManager.CELLSIZE

		return (cellx, celly)
