import profile
import sys
from Controller.Logger import Logger
from Controller.GameController import GameController

if __name__ == '__main__':
	sys.stdout = Logger()
	gameController = GameController()
	#profile.run('game.main()')
	gameController.main()