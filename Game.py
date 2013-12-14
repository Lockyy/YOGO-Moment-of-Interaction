import profile
import sys
from Logger import Logger
from Controller import Controller

if __name__ == '__main__':
	sys.stdout = Logger()
	controller = Controller()
	#profile.run('game.main()')
	controller.main()