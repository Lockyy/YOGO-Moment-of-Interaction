from random import randint

class PathfindingNode:

	def __init__(self, coords, parent = None, end = None):
		self.parent = parent
		self.coords = coords

		self.g = None

		if end == None:
			self.f = 0
		else:
			self.f = abs(self.coords[0] - end[0]) * self.g + abs(self.coords[1] - end[1]) * self.g 

	def getG(self):
		if self.g == None:
			g = self.generateG()
			if self.parent == None:
				self.g = g
			else:
				self.g = self.parent.getG() + g

		return self.g

	def getF(self):
		return self.getG() + self.f

	def generateG(self):
		return randint(0, 10)