import random

class Villager(object):

	def __init__(self):
		self.gender = self.getGender()
		self.name = self.getNewName(self.gender)

	def getGender(self):
		return random.randint(1, 2)

	# Creates a new name using the clauses specified in the prefixes and suffixes
	# in the data/names folder.
	def getNewName(self, gender):
		if gender == 1:
			genderString = "female"
		else:
			genderString = "male"

		# Get a random prefix and suffix.
		with open("data/names/" + genderString + ".txt", "r") as prefixFile:
			firstName = random.choice(prefixFile.readlines()).rstrip()

		with open("data/names/surnames.txt", "r") as suffixFile:
			surname = random.choice(suffixFile.readlines()).rstrip()

		# Return the new name.
		return firstName + " " + surname