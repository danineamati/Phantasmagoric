from . import maze
import random
import sys
import csv

from ast import literal_eval

Direction = ["North", "East", "South", "West"]

class playerMaze():
	"""Stores the maze, player location, and what the player can view."""
	def __init__(self, maze = maze.Maze(0, 0), startLoc = (-1, -1)):
		self.maze = maze
		self.currLoc = startLoc # in the form (row, col)
		self.visited = [startLoc] # Stores visited locations

		self.otherPlayerUsernames = []

		self.viewedCoins = []
		self.score = 0

		sr, sc = startLoc
		if sr <= 0 or sc <= 0:
			self.canViewEnd = False
			
		else:
			self.canViewEnd = self.checkViewEnd()
			self.checkViewCoin()
			
		

	def savePlayerMaze(self, playerFileName, saveThisMaze = True):
		'''Will save the crucial data of the maze so that it can be loaded
		after the program has ended.

		Filename is assumed to be a csv file. '''

		with open(playerFileName, 'w', newline = '') as saveFile:
			saveWriter = csv.writer(saveFile)
			saveWriter.writerow(["Current Location", self.currLoc])
			saveWriter.writerow(["Visited Locations", self.visited])
			saveWriter.writerow(["Other Usernames:", self.otherPlayerUsernames])
			saveWriter.writerow(["Can view end", int(self.canViewEnd)])	
			saveWriter.writerow(["Viewed Coins", self.viewedCoins])
			saveWriter.writerow(["Score", self.score])

		# Now save the maze
		if saveThisMaze:
			mazeFilename = playerFileName.split('_')[0] + '_' +\
								playerFileName.split('_')[1] + '.csv'
			self.maze.saveMaze(mazeFilename)

	def loadPlayerMaze(self, playerFileName):
		'''Loads back saved data to recreate a maze.

		Filename is assumed to be a csv file.'''
		
		with open(playerFileName) as saveFile:
			saveReader = csv.reader(saveFile)

			for index, row in enumerate(saveReader):
				if index == 0:
					self.currLoc = literal_eval(row[1])
				elif index == 1:
					self.visited = literal_eval(row[1])
				elif index == 2:
					self.otherPlayerUsernames = literal_eval(row[1])
				elif index == 3:
					try:
						self.canViewEnd = bool(literal_eval(row[1]))
					except ValueError as e:
						print(e)
						self.canViewEnd = True
					
				elif index == 4:
					self.viewedCoins = literal_eval(row[1])
				elif index == 5:
					self.score = int(row[1])
					# print("Loading Score: ", int(row[1]), self.score)

		mazeFilename = playerFileName.split('_')[0] + '_' +\
								playerFileName.split('_')[1] + '.csv'

		newmaze = maze.Maze(0, 0)
		newmaze.loadMaze(mazeFilename)

		self.maze = newmaze
		self.checkViewCoin()

	def setOtherUsernamer(self, Usernames):
		'''Loads other player usernames so that the mazes update in unison. '''
		self.otherPlayerUsernames = Usernames

	def getCurrentLocation(self):
		'''Returns current location.'''
		return self.currLoc

	def addNewLocation(self, loc):
		'''Sets new location for the player and adds it to the list of visited
		locations.'''
		self.visited.append(loc)
		self.currLoc = loc
		if self.canViewEnd == False:
			self.canViewEnd = self.checkViewEnd()
		self.checkViewCoin(False)

		if (loc[0], loc[1]) in self.maze.coin:
			self.maze.coin.remove(loc)
			self.viewedCoins.remove(loc)

			self.score += 1

	def moveLocation(self, direction):
		'''Moves to new location given ['North', 'East', 'South', 'West'] 

		The Direction list is specified in maze.py'''
		current_row, current_col = self.currLoc
		assert(not self.maze.hasWall(current_row, current_col, direction))
		new_row, new_col = self.maze.getNeighborCell(\
			current_row, current_col, direction)
		self.addNewLocation((new_row, new_col))

	def checkMove(self, direction):
		'''Checks if player can move in given direction.'''
		current_row, current_col = self.currLoc
		return not self.maze.hasWall(current_row, current_col, direction)

	def checkViewEnd(self):
		'''Checks if the player can see or has seen the end. '''
		# Check the adjacent locations to the end.
		for direction in Direction:
			# checks that there is not a wall in the way 
			if not self.maze.hasWall(self.maze.end[0], \
								self.maze.end[1], direction):

				# check locations around the player
				adjacent = self.maze.getNeighborCell(self.maze.end[0], \
									self.maze.end[1], direction)

				# if the adjacent cell is the current location
				# AND there is not wall in the way,
				if adjacent == self.currLoc \
				  and adjacent not in self.viewedEnd:	
					return True

		# Otherwise
		return False

	def checkViewCoin(self, verbose = False):
		'''Checks if the player has seen or can see coins in the maze. '''
		for direction in Direction:
			# checks that there is not a wall in the way 
			if not self.maze.hasWall(self.currLoc[0], \
								self.currLoc[1], direction):

				# check locations around the player
				adjacent = self.maze.getNeighborCell(self.currLoc[0], \
									self.currLoc[1], direction)

				# if the adjacent cell is a coin 
				# AND there is not a wall in the way
				if adjacent in self.maze.coin \
					and adjacent not in self.viewedCoins:
					self.viewedCoins.append(adjacent)

		if verbose:
			print(self.viewedCoins)

	def print(self):
		'''Outputs the maze using simple ASCII-art to the specified output.
		The output format is as follows, using the example maze from the
		assignment write-up.  (The text to the right of the maze is purely
		explanatory, and you don't need to output it.)
		
		3 4               (# of rows and then # of columns)
		+---+---+---+---+ (each cell is 3 spaces wide, with a + at each corner)
		| -   - | X   X |   (walls indicated by --- or |)
		+---+   +   +   +   (Player Location indicated by P)
		| X | - | X | X |   (Visited indicated by V)
		+   +   +   +   +
		|     P     | X |
		+---+---+---+---+
		 '''

		print()
		# print(self.maze.numRows, self.maze.numColumns)
		print("Current score: " + str(self.score))

		top_wall = '+'
		for c in range(self.maze.numColumns):
			if (0, c) in self.visited and self.maze.hasWall(0, c, "North"):
					top_wall += '---+'
			else:
				top_wall += '   +'
		print(top_wall)

		def print_cell(content, r, c):
			'''Prints the cell and the wall for a given content'''
			current = content
			if (r, c) in self.visited and self.maze.hasWall(r, c, "East"):
				current += '|'
			elif c < self.maze.numColumns - 1 and \
						(r, c + 1) in self.visited and \
						self.maze.hasWall(r, c + 1, "West")	:
				current += '|'
			else:
				current += ' '
			return current
		
		for r in range(self.maze.numRows):
			current_row = ''

			if (r, 0) in self.visited and self.maze.hasWall(r, 0, "West"):
				current_row += '|'
			# if c > 0 and (r, c - 1) in self.visited and \
			# 	self.maze.hasWall(r, c - 1, "East")	:
			# 	current_row += '|'
			else:
				current_row += ' '
			
			for c in range(self.maze.numColumns):
				if (r, c) == self.getCurrentLocation():
					current_row += print_cell(' P ', r, c)

				elif self.canViewEnd and (r, c) == self.maze.end:
					current_row += print_cell(' E ', r, c)

				elif (r, c) in self.viewedCoins:
					current_row += print_cell(' C ', r, c)

				elif (r, c) in self.visited:
					current_row += print_cell(' - ', r, c)

				else:
					current_row += print_cell('   ', r, c)

			print(current_row)

			current_floor = '+'
			if r < self.maze.numRows:
				for c in range(self.maze.numColumns):
					if (r, c) in self.visited and \
										self.maze.hasWall(r, c, "South"):
						current_floor += '---+'
					elif r < self.maze.numColumns and \
										(r + 1, c) in self.visited and \
										self.maze.hasWall(r + 1, c, "North"):
						current_floor += '---+'
					else:
						current_floor += '   +'
				print(current_floor)