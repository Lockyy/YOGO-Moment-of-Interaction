import Colours
import pygame

class Drawer(object):

	def __init__(self, DISPLAYSURF, configParser):
		self.DISPLAYSURF = DISPLAYSURF

	def fill(self, colour = False):
		if colour == False:
			colour = Colours.BACKGROUND

		self.DISPLAYSURF.fill(colour)

