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

		self.fpsClock = pygame.time.Clock()

	def main(self):
		clicked = True
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == MOUSEBUTTONUP:
					# Pixel co-ordinates of click.
					mousex, mousey = event.pos
					
					clickedCell = self.viewController.getClickedCell((mousex, mousey))

					if clickedCell:
						self.model.setFocusCell(clickedCell)
					else:
						print "Clicked outside game view"

					clicked = True
				elif event.type == KEYDOWN and event.key == K_n:
					self.newGame()

			self.viewController.updateView(self.model, updateUI = clicked)
			clicked = False

        	self.fpsClock.tick(self.configManager.FPS)

	def newGame(self):
		self.configManager.regenSeed()
		self.model = Model(self.configManager)