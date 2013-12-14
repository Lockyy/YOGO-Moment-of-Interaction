import Colours
import pygame

class Drawer(object):

	def __init__(self, configParser):
		self.configParser = configParser

	def fill(self, DISPLAYSURF, colour = False):
		if colour == False:
			colour = Colours.BACKGROUND

		DISPLAYSURF.fill(colour)

