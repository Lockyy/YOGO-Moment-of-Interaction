import pygame
from Drawer import Drawer

class View(object):

	def __init__(self, configParser):
		self.configParser = configParser

		pygame.init()

		self.setupWindow()

		self.drawer = Drawer(self.DISPLAYSURF, self.configParser)

	def setupWindow(self):
		windowHeight 		= int(self.configParser.get('UI', 'resolution_height'))
		windowWidth			= int(self.configParser.get('UI', 'resolution_width'))

		self.DISPLAYSURF	= pygame.display.set_mode((windowWidth, windowHeight))

		windowTitle			= self.configParser.get('Text', 'window_title')

		pygame.display.set_caption(windowTitle)

	def drawWindow(self, model):
		self.drawer.fill()
		pygame.display.update()
