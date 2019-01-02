# This program runs and saves a game from the terminal

import sys

from MazeGenerator.maze import *
from MazeGenerator.playerMaze import *
from MazeGenerator.genmaze import fullgenMaze


def startNewGame():
	'''Starts a new game.'''
	print("Starting a New Game")

	size = ''
	numPlayers = 0
	coinPercent = -1

	# First we select the map size:
	sizeList = ['small', 'medium', 'big']
	if len(sys.argv) > 1:
		size = sys.argv[1]

	while size.lower() not in sizeList:
		size = input("How big of a map? [small / medium / big] ")
		if size.lower() not in sizeList:
			print("Try Again")

	if size.lower() == sizeList[0]:
		numRows = 8
		numCols = 8
	elif size.lower() == sizeList[1]:
		numRows = 12
		numCols = 18
	elif size.lower() == sizeList[2]:
		numRows = 20
		numCols = 25
			

	if len(sys.argv) > 2:
		numPlayers = int(sys.argv[2])

	while numPlayers <= 0:
		try:
			numPlayers = int(input("How many players: "))
		except ValueError as e:
			print("Not a valid number. Type the number value (e.g. 1 or 3)")
			numPlayers = 0
		if numPlayers <= 0:
			print("Try Again")

	if len(sys.argv) > 3:
		coinPercent = float(sys.argv[3])

	while coinPercent < 0 or coinPercent >= 1:
		try:
			coinPercent = float(input("Percentage of coins: "))
		except ValueError as e:
			print("Not a valid number. " + \
					" Type the number decimal between 0 and 1.")
			coinPercent = 0
		if coinPercent < 0 or coinPercent >= 1:
			print("Try Again")
		
	threshold = 10
	print(\
'''\nGenerating map with properties:
	{}: {} x {}
	{} Players
	{}% Coins
	{} Branching Threshold'''.\
	format(size, numRows, numCols, numPlayers, coinPercent * 100, threshold))

	maze = fullgenMaze(numRows, numCols, numPlayers, threshold, coinPercent, \
		False, False)

	print("\nTime to create characters")

	for player in range(numPlayers):
		player_username = input(\
			"Please enter player {} username: ".format(player + 1))
		filename = 'saveFiles/' + player_username + '.csv'

		playerObj = playerMaze(maze, maze.start[player])
		playerObj.savePlayerMaze(filename)





def playExistingGame():
	'''Loads up an existing game.'''
	print("Loading an Existing Game")

def runGame():
	'''Runs the game.'''
	newGame = ''

	while newGame.lower() not in ['y', 'n']:
		newGame = input("Do you want to start a new game? [y/n]: ")

		if newGame.lower() == 'y':
			startNewGame()
		elif newGame.lower() == 'n':
			playExistingGame()
		else:
			print("Try again.")


if __name__ == '__main__':
	runGame()

