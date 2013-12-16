import pygame
import sys
import time
from Model.ConfigManager import ConfigManager
from ViewController import ViewController
from Model.Model import Model
from collections import defaultdict
from pygame.locals import *

class GameController(object):
	
	def __init__(self):
		self.configManager = ConfigManager()
		self.fpsClock = pygame.time.Clock()

		self.viewController = ViewController(self.configManager)

		self.newGame()

		# Amount of logic frames per second.
		LOGIC_UPDATES_PER_SECOND = 1
		self.SKIP_TICKS = 1000 / LOGIC_UPDATES_PER_SECOND
		self.MAX_FRAMESKIP = 10

	def main(self):
		self.buttonsPressed = defaultdict(lambda: False)

		# How long since pygame was inited
		# Used to keep track of how long it has been since the last draw.
		nextGameTick = pygame.time.get_ticks()

		while True:
			# Logic loop parameter.
			loops = 0
			# While enough past time has passed since the last logic update and while total consecutive logic loops
			# is below MAX_FRAMESKIP.
			while pygame.time.get_ticks() > nextGameTick and loops < self.MAX_FRAMESKIP:
				self.updateModel()

				nextGameTick += self.SKIP_TICKS
				loops += 1

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == MOUSEBUTTONUP:
					# Pixel co-ordinates of click.
					mousex, mousey = event.pos
					
					clickedCell = self.viewController.getClickedCell((mousex, mousey))

					if clickedCell:
						self.model.world.setFocusCell(clickedCell)
					else:
						print "Clicked outside game view"
				elif event.type == KEYDOWN and event.key == K_n:
					self.buttonsPressed['regenWorld'] = True
				elif event.type == KEYDOWN and event.key == K_y:
					self.buttonsPressed['confirmKey'] = True
				elif event.type == KEYDOWN and event.key == K_p:
					self.buttonsPressed['pauseKey'] = True

			self.handleInput()

			self.updateView(self.model)


	def newGame(self):
		self.model = Model(self.configManager)
		self.updateView(self.model)
		self.fpsClock.tick(self.configManager.FPS)

		while not self.model.world.worldGenDone:
			self.model.world.createWorldStep()
			self.updateView(self.model)
        	self.fpsClock.tick(self.configManager.FPS)

	def updateView(self, model, updateUI = False):
		self.configManager.currentFPS = str(int(self.fpsClock.get_fps()))

		self.viewController.updateView(model)
		self.fpsClock.tick(self.configManager.FPS)

	def updateModel(self):
		self.model.updateWorld()

	def handleInput(self):
		if self.buttonsPressed['regenWorld']:
			self.regenWorld()
			self.buttonsPressed['regenWorld'] = False
		
		if self.buttonsPressed['confirmKey'] and not self.model.villagePlaced:
			self.placeVillage()
			self.buttonsPressed['confirmKey'] = False

		if self.buttonsPressed['pauseKey'] and self.model.villagePlaced:
			self.model.gamePaused = not self.model.gamePaused
			self.buttonsPressed['pauseKey'] = False

	def regenWorld(self):
		self.configManager.regenSeed()
		self.newGame()

	def placeVillage(self):
		self.model.placeVillage()
		self.model.villagePlaced = True

