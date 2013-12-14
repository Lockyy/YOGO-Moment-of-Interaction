import pygame
import sys
from ConfigManager import ConfigManager
from ViewController import ViewController
from Model import Model
from pygame.locals import *

class GameController(object):
	
	def __init__(self):
		self.configManager = ConfigManager()

		self.viewController 	=	ViewController(self.configManager)
		self.model 				=	Model(self.configManager)

	def main(self):
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

			self.viewController.updateView(self.model)



