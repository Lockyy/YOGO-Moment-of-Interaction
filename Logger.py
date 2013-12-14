import datetime
import sys

class Logger(object):
	def __init__(self):
		self.terminal = sys.stdout
		self.logFile = "log.txt"

	def write(self, message):
		dateTime = self.getDateTimeString() 

		if message == '\n':
			dateTime = ""

		self.terminal.write(message)

		with open(self.logFile, "a") as output:
			output.write(dateTime + message)

	def getDateTimeString(self, leadingZeroes = True, dateSeperator = None, timeSeperator = None, dateTimeSeperator = None):
		leading = "0" if leadingZeroes else ""
		if dateSeperator == None:
			dateSeperator = "/"
		if timeSeperator == None:
			timeSeperator = ":"
		if dateTimeSeperator == None:
			dateTimeSeperator = " "

		dateTime = datetime.datetime.utcnow()
		output = "["
		output += str(dateTime.year) + dateSeperator
		if dateTime.month < 10:
			output += leading
		output += str(dateTime.month) + dateSeperator
		if dateTime.day < 10:
			output += leading
		output += str(dateTime.day) + dateTimeSeperator
		# I wish osx would just let me use :s in filepaths
		if dateTime.hour < 10:
			output += leading
		output += str(dateTime.hour) + timeSeperator
		if dateTime.minute < 10:
			output += leading
		output += str(dateTime.minute)
		output += "] "

		return output