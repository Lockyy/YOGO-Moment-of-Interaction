from ConfigParser import SafeConfigParser

class ConfigManager(object):

	SIDEBARWIDTH 	= 300
	MINIMUMWIDTH 	= 1280
	MINIMUMHEIGHT 	= 800

	def __init__(self):
		# Get the config file. This stores any non-world generation settings.
		# Including filepath for default world gen settings.
		self.configParser = SafeConfigParser()
		self.configParser.read('data/settings/config.ini')

		self.WINDOWHEIGHT 	= int(self.configParser.get('UI', 'resolution_height'))
		self.WINDOWWIDTH	= int(self.configParser.get('UI', 'resolution_width'))

		if self.WINDOWHEIGHT < self.MINIMUMHEIGHT:
			self.WINDOWHEIGHT = self.MINIMUMHEIGHT

		if self.WINDOWWIDTH < self.MINIMUMWIDTH:
			self.WINDOWWIDTH = self.MINIMUMWIDTH

		self.RESOLUTION = (self.WINDOWWIDTH, self.WINDOWHEIGHT)

		self.WINDOWTITLE = self.configParser.get('Text', 'window_title')
