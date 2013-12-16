import pygame
from View.Drawer import Drawer
from View.GameView import GameView
from View.SidebarView import SidebarView

class ViewController(object):

	def __init__(self, configManager):
		self.configManager = configManager

		pygame.init()

		self.setupWindow()

		self.drawer = Drawer(self.configManager)

		self.drawer.fill(self.DISPLAYSURF)

		self.gameView = GameView(self.configManager, self.DISPLAYSURF, self.drawer)

		self.sideBarView = SidebarView(self.configManager, self.DISPLAYSURF, self.drawer)

		pygame.display.update()

	def setupWindow(self):
		windowTitle = self.configManager.WINDOWTITLE

		pygame.display.set_caption(windowTitle)

		self.DISPLAYSURF = pygame.display.set_mode(self.configManager.RESOLUTION)

	def updateView(self, model):
		# Draw in the sidebar
		self.sideBarView.update(model)

		# Draw the game world
		self.gameView.update(model)

		# Update the display
		pygame.display.update()

	# Get which cell has been clicked. For use with selecting cells.
	def getClickedCell(self, (mousex, mousey)):
		if not self.getGameViewRect().collidepoint((mousex, mousey)):
			return False

		mousex -= self.configManager.BORDERSIZE
		mousey -= self.configManager.BORDERSIZE

		cellx = mousex / self.configManager.CELLSIZE
		celly = mousey / self.configManager.CELLSIZE

		return (cellx, celly)

	def getGameViewRect(self):
		gameViewLocation = self.gameView.TOPLEFT
		gameViewRect = pygame.Rect(	gameViewLocation[0],\
									gameViewLocation[1],\
									self.configManager.WORLDDISPLAYWIDTH,\
									self.configManager.WORLDDISPLAYHEIGHT)

		return gameViewRect
