import Colours
import pygame

class Drawer(object):

	def __init__(self, configManager):
		self.configManager = configManager
		self.fontObjects = {}

	# Fill the given DISPLAYSURFACE
	def fill(self, DISPLAYSURF, colour = False):
		if colour == False:
			colour = Colours.GAMEBACKGROUND

		DISPLAYSURF.fill(colour)

	# Draw a cell at position (x, y) on the grid.
	def drawCell(self, DISPLAYSURF, colour, (x, y)):
		cellSize = self.configManager.CELLSIZE
		
		cellRect = (x, y, cellSize, cellSize)

		pygame.draw.rect(DISPLAYSURF, colour, cellRect)

	# Print message to co-ordinates xPixel, yPixel.
	def drawText(self, message, DISPLAYSURF, (xPixel, yPixel), colour = False, background = False, fontSize = 32):
		if colour == False:
			colour = Colours.TEXT
		if background == False:
			background = Colours.SIDEBARBACKGROUND
		if fontSize == False:
			fontSize = 32

		# Hold onto the font objects being created. Saves us time later.s
		if fontSize in self.fontObjects:
			fontObj = self.fontObjects[fontSize]
		else:
			fontObj = pygame.font.Font('freesansbold.ttf', fontSize)
			self.fontObjects[fontSize] = fontObj

		textSurfaceObj = fontObj.render(message, True, colour, background)
		textRectObj = textSurfaceObj.get_rect()
		textRectObj.topleft = (xPixel, yPixel)
		DISPLAYSURF.blit(textSurfaceObj, textRectObj)