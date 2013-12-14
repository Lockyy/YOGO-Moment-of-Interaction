import pygame
from Drawer import Drawer

class View(object):
	
	def __init__(self, configParser, MAINDISPLAYSURF, drawer, SIDEBARWIDTH):
		self.configParser = configParser
		self.MAINDISPLAYSURF = MAINDISPLAYSURF
		self.drawer = drawer
		self.SIDEBARWIDTH = SIDEBARWIDTH

	def update(self, model):
		self.drawer.fill(self.MAINDISPLAYSURF)

	def drawToMainDisplay(self):
		self.MAINDISPLAYSURF.blit(self.DISPLAYSURF, self.TOPLEFT)