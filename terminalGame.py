# This program runs and saves a game from the terminal

import sys

from MazeGenerator.maze import *
from MazeGenerator.playerMaze import *
from MazeGenerator.genmaze import fullgenMaze


def startNewGame():
	'''Starts a new game.'''
	print("Starting a New Game")

	# Initializing quantities that will be needed later.
	size = ''
	numPlayers = 0
	coinPercent = -1

	# First we select the map size:
	sizeList = ['small', 'medium', 'big']
	if len(sys.argv) > 2:
		size = sys.argv[2]

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
			
	# Second we determine the number of players
	if len(sys.argv) > 3:
		numPlayers = int(sys.argv[3])

	while numPlayers <= 0:
		try:
			numPlayers = int(input("How many players: "))
		except ValueError as e:
			print("Not a valid number. Type the number value (e.g. 1 or 3)")
			numPlayers = 0
		if numPlayers <= 0:
			print("Try Again")

	# Third we determine the percentage of the board that will be filled with
	# coins
	if len(sys.argv) > 4:
		coinPercent = float(sys.argv[4])

	while coinPercent < 0 or coinPercent >= 1:
		try:
			coinPercent = float(input("Percentage of coins: "))
		except ValueError as e:
			print("Not a valid number. " + \
					" Type the number decimal between 0 and 1.")
			coinPercent = 0
		if coinPercent < 0 or coinPercent >= 1:
			print("Try Again")
	
	# For now we keep the branching threshold at 10, which works for all map
	# sizes. 
	threshold = 10

	# Display to user that the map/maze is being generated. 
	# It is also useful so that the user knows that the parameters have been
	# inputted correctly
	print(\
'''\nGenerating map with properties:
	{}: {} x {}
	{} Players
	{}% Coins
	{} Branching Threshold'''.\
	format(size, numRows, numCols, numPlayers, coinPercent * 100, threshold))

	# Here we generate the maze
	maze = fullgenMaze(numRows, numCols, numPlayers, threshold, coinPercent, \
		False, False)

	mazeName = input("Enter the name of the maze: ")
	print("\nWelcome to {}".format(mazeName))

	# In order to save the maze data, etc. The user needs to input the username
	# of the players.
	# In the current implementation, the user specifies all of the usernames.
	print("\nTime to create characters")

	allplayers = []

	for player in range(numPlayers):
		player_username = input(\
			"Please enter player {} username: ".format(player + 1))

		playerObj = playerMaze(maze, maze.start[player])
		allplayers.append((playerObj, player_username))

	for player in allplayers:
		obj, user = player
		for other_player in allplayers:
			other_obj, other_user = other_player

			if user != other_user:
				obj.setOtherUsername(other_user)

		filename = 'saveFiles/' + 'maze_' + mazeName + '_' + \
						user + '.csv'
		playerObj.savePlayerMaze(filename)


	# The map has been generated and the game is ready!
	print()
	print("The game is ready!")
	playGame = input("Would you like to play? [y/n]: ")

	if playGame == 'y':
		playExistingGame(False)

def endgame(player, maze):
	'''This is the end screen when a player has moved to the END tile. '''
	if player.currLoc == maze.end:
		maze.print(False)
		print('''
#################################
        Congratulations!!!!
        Score: {}
#################################
			'''.format(player.score))
		return True
	else:
		return False


def playExistingGame(sysValid = True):
	'''Loads up an existing game.'''
	print("Loading an Existing Game")
	fileFound = False

	# While loops that asks for user to input username and if the name matchs
	# with a file that is in saveFiles, the desired maze is displayed
	while fileFound == False:
		if sysValid and len(sys.argv) > 2:
			mazename = sys.argv[2]
			username = sys.argv[3]
		else:
			mazename = input("What is the name of the maze: ")
			username = input("What is your username: ")

		if username.lower() == "q":
			quit()

		try:
			playMaze = playerMaze()
			filename = "saveFiles/maze_" + mazename + '_' + username + ".csv"

			playMaze.loadPlayerMaze(filename)

			fileFound = True

		except FileNotFoundError as e:
			print("File {} not found. Please try again.".format(filename))
			sysValid = False

	playMaze.print()

	playTurn = input("Do you want to play your turn? [y/n]: ")
	turnStartAsk = True

	# While loops that asks if the player wants to play out their turn
	while turnStartAsk:
		if playTurn == "y":
			break

		elif playTurn == "n":
			quit()

		else: 
			playTurn = input("That is not a valid option. " + \
				"Do you want to play your turn? [y/n]: ")

	# While loop that asks user for input to move their character this turn
	# The loop then displays the updated maze if the move is valid
	turn = True

	while turn:

		moveChoice = input("Where would you like to move? " +\
			"[North/South/East/West/Cancel]: ")

		Direction = ["North", "East", "South", "West"]

		if moveChoice in ["n", "e", "s", "w"]:
			moveChoice = Direction[["n", "e", "s", "w"].index(moveChoice)]

		if (moveChoice == "North" or moveChoice == "South" \
			or moveChoice == "East" or moveChoice == "West") and \
			playMaze.checkMove(moveChoice):

				playMaze.moveLocation(moveChoice)

				if not endgame(playMaze, playMaze.maze):
					playMaze.print()

					turnSave = ''
					while turnSave not in ['y', 'n']:
						turnSave = input(
							"Do you want to save this turn? [y/n]: ")

						if turnSave == "y":
							print("Current score: " + str(playMaze.score))
							playMaze.savePlayerMaze(filename)
							turn = False

						elif turnSave == "n":
							redo = input(
								"Do you want to redo your turn? [y/n]: ")

							if redo == "y":
								playMaze.loadPlayerMaze(filename)
								playMaze.print()

							else:
								turn = False
				else:
					print("Current score: " + str(playMaze.score))
					playMaze.savePlayerMaze(filename)
					turn = False

		elif moveChoice == "Cancel":
			turn = False

		else:
			print("That is not a valid move.")

def runGame():
	'''Runs the game.'''
	newGame = ''


	while newGame.lower() not in ['y', 'n']:
		print("Welcome to Phantasmagoric!")
		print("")
		if len(sys.argv) > 1:
			newGame = sys.argv[1]
		else:
			newGame = input("Do you want to start a new game? [y/n]: ")

		if newGame.lower() == 'y':
			startNewGame()
		elif newGame.lower() == 'n':
			playExistingGame()
		else:
			print("Try again.")
			if len(sys.argv) > 1:
				quit()


if __name__ == '__main__':
	runGame()

