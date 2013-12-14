import pygame
import sys
from View import View
from Model import Model
from pygame.locals import *
from ConfigParser import SafeConfigParser

class Controller(object):

	def __init__(self):
		# Get the config file. This stores any non-world generation settings.
		# Including filepath for default world gen settings.
		self.configParser = SafeConfigParser()
		self.configParser.read('data/settings/config.ini')

		self.view 	=	View(self.configParser)
		self.model 	=	Model(self.configParser)

	def main(self):
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

			self.view.drawWindow(self.model)



