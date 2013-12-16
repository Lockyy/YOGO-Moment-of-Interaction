import pygame
from Drawer import Drawer

class View(object):
	
	def __init__(self, configManager, MAINDISPLAYSURF, drawer):
		self.configManager = configManager
		self.MAINDISPLAYSURF = MAINDISPLAYSURF
		self.drawer = drawer

	def update(self, model):
		self.drawer.fill(self.MAINDISPLAYSURF)

	def drawToMainDisplay(self):
		self.MAINDISPLAYSURF.blit(self.DISPLAYSURF, self.TOPLEFT)