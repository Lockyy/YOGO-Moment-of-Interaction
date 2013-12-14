import profile
import sys
from Logger import Logger
from GameController import GameController

if __name__ == '__main__':
	sys.stdout = Logger()
	gameController = GameController()
	#profile.run('game.main()')
	gameController.main()