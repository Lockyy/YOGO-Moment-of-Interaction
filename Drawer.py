import Colours
import pygame

class Drawer(object):

	def __init__(self, configManager):
		self.configManager = configManager

	def fill(self, DISPLAYSURF, colour = False):
		if colour == False:
			colour = Colours.BACKGROUND

		DISPLAYSURF.fill(colour)

