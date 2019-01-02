from maze import Maze
import playerMaze
import genmaze

import random
import sys
import copy

def printResult(text, numPassed, totalTests, truth):
	'''Formats the print result.'''
	text = text + (50 - len(text)) * ' '

	if truth:
		print(text + "PASSED {} / {}".format(numPassed, totalTests))
	else:
		print(text + "FAILED {} / {}".format(numPassed, totalTests), " * ")


def test(numRows, numCols, numPlayers, threshold, verbose = False):
	numPassed = 0

	totalTests = 8 + numPlayers

	if numRows == 10 and numCols == 15 and numPlayers == 2:
		totalTests += 26

	testMaze = genmaze.fullgenMaze(numRows, numCols, numPlayers, threshold,\
	 verbose, verbose)

	# We first checked that all the cells have been visited
	visitedPassed = True
	for row, col in ((r, c) for r in range(testMaze.numRows) \
							for c in range(testMaze.numColumns)):
		if not testMaze.isVisited(row, col):
			visitedPassed = False
			break
	if visitedPassed:
		numPassed += 1
	printResult("ALL GEN CELLS VISITED", numPassed, totalTests, visitedPassed)

	
	# We also check that the player start locations have been added
	passed = (len(testMaze.start) > 0)
	if passed:
		numPassed += 1
	printResult("PLAYER START LOC ON MAZE", numPassed, totalTests, passed)

	# We check that the player location is logged in their own classes
	players = []
	for play in range(numPlayers):
		players.append(playerMaze.playerMaze(testMaze, testMaze.start[play]))

		passed = (players[play].getCurrentLocation() == testMaze.start[play])

		if passed:
			numPassed += 1
		printResult("PLAYER START LOC SAVED", numPassed, totalTests, passed)

	testPercents = [0, 0.05, 0.1, 0.5]

	for percent in testPercents:
		testMaze.coin = []

		coinCount = int((numRows * numCols) * percent)

		testMaze.setCoin(percent)

		if verbose:
			testMaze.print(False)

		passed = (len(testMaze.coin) == coinCount)

		if passed:
			numPassed += 1 
		printResult("ALL COINS ON MAZE", numPassed, totalTests, passed)
		

	# Test the saving feature
	# We first test inPlace loading
	testSavedMaze = copy.deepcopy(testMaze)

	filename = '../saveFiles/testSaveFile.csv'
	testMaze.saveMaze(filename)
	testMaze.loadMaze(filename)

	passed = (testMaze.numRows == testSavedMaze.numRows) and \
				(testMaze.numColumns == testSavedMaze.numColumns) and \
				(testMaze.start == testSavedMaze.start) and \
				(testMaze.end == testSavedMaze.end) and \
				(testMaze.cells == testSavedMaze.cells) and \
				(testMaze.cellNumToExit == testSavedMaze.cellNumToExit) and \
				(testMaze.coin == testSavedMaze.coin)

	if verbose:
		testMaze.print()
		testSavedMaze.print()
	if passed:
			numPassed += 1
	printResult("MAZE SAVE AND LOAD INPLACE", numPassed, totalTests, passed)

	# Now we test not inPlace loading
	testMaze.saveMaze(filename)
	newmaze = Maze(0, 0)
	newmaze.loadMaze(filename)

	passed = (newmaze.numRows == testSavedMaze.numRows) and \
				(newmaze.numColumns == testSavedMaze.numColumns) and \
				(newmaze.start == testSavedMaze.start) and \
				(newmaze.end == testSavedMaze.end) and \
				(newmaze.cells == testSavedMaze.cells) and \
				(newmaze.cellNumToExit == testSavedMaze.cellNumToExit) and \
				(newmaze.coin == testSavedMaze.coin)

	if verbose:
		newmaze.print()
		testSavedMaze.print()
	if passed:
			numPassed += 1
	printResult("MAZE SAVE AND LOAD NOT INPLACE", numPassed, totalTests, passed)


	# Using the test case of 10 rows and 15 cols with seed 'TestSeed'
	# with 2 players
	if numRows == 10 and numCols == 15 and numPlayers == 2:
		p1 = players[0]
		p2 = players[1]

	else:
		return numPassed

	# Test player 1 can move North and West but not East and South.
	passed = p1.checkMove("North")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK NORTH", numPassed, totalTests, passed)

	passed = not p1.checkMove("East")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK EAST", numPassed, totalTests, passed)

	passed = not p1.checkMove("South")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK SOUTH", numPassed, totalTests, passed)

	passed = p1.checkMove("West")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK WEST", numPassed, totalTests, passed)

	# Then attempt a move North. Check can only move South.
	p1.moveLocation("North")
	passed = (p1.getCurrentLocation() == (0, 14))
	if passed:
		numPassed += 1
	printResult("* PLAYER ONE MOVE NORTH *", numPassed, totalTests, passed)

	passed = not p1.checkMove("North")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK NORTH", numPassed, totalTests, passed)

	passed = not p1.checkMove("East")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK EAST", numPassed, totalTests, passed)

	passed = p1.checkMove("South")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK SOUTH", numPassed, totalTests, passed)

	passed = not p1.checkMove("West")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK WEST", numPassed, totalTests, passed)

	# Test player 2 can move West but not North, East, or South.
	passed = not p2.checkMove("North")
	if passed:
		numPassed += 1
	printResult("PLAYER TWO CHECK NORTH", numPassed, totalTests, passed)

	passed = not p2.checkMove("East")
	if passed:
		numPassed += 1
	printResult("PLAYER TWO CHECK EAST", numPassed, totalTests, passed)

	passed = not p2.checkMove("South")
	if passed:
		numPassed += 1
	printResult("PLAYER TWO CHECK SOUTH", numPassed, totalTests, passed)

	passed = p2.checkMove("West")
	if passed:
		numPassed += 1
	printResult("PLAYER TWO CHECK WEST", numPassed, totalTests, passed)

	# Then attempt a move West. Check can move East or South
	p2.moveLocation("West")
	passed = (p2.getCurrentLocation() == (5, 13))
	if passed:
		numPassed += 1
	printResult("* PLAYER ONE MOVE NORTH *", numPassed, totalTests, passed)

	passed = not p2.checkMove("North")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK NORTH", numPassed, totalTests, passed)

	passed = p2.checkMove("East")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK EAST", numPassed, totalTests, passed)

	passed = p2.checkMove("South")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK SOUTH", numPassed, totalTests, passed)

	passed = not p2.checkMove("West")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK WEST", numPassed, totalTests, passed)

	player1_Old = copy.deepcopy(p1)

	moves = ["South", "West", "South", "South", "West", "South", "East", \
				"East", "North", "North", "South", "South", "West", "West", \
				"South", "South", "West", "North", "West", "West", "West", \
				"South", "West", "West", "West", "West", "North", "North"]
	for move in moves:
		if p1.checkMove(move):
			p1.moveLocation(move)
		else:
			break

	player1_Original = copy.deepcopy(p1)

	# Now we check that we can save and load player data
	filename_p1 = "../saveFiles/testP1SaveFile.csv"
	p1.savePlayerMaze(filename_p1)
	p1.loadPlayerMaze(filename_p1)

	passed = (p1.maze.numRows == player1_Original.maze.numRows) and \
				(p1.maze.numColumns == player1_Original.maze.numColumns) and \
				(p1.maze.start == player1_Original.maze.start) and \
				(p1.maze.end == player1_Original.maze.end) and \
				(p1.maze.cells == player1_Original.maze.cells) and \
				(p1.maze.cellNumToExit == player1_Original.maze.cellNumToExit) \
				and \
				(p1.maze.coin == player1_Original.maze.coin)

	if verbose:
		p1.print()
		player1_Original.print()
	if passed:
		numPassed += 1
	printResult("PLAYER MAZE SAVE AND LOAD INPLACE", numPassed, \
								totalTests, passed)

	passed = (p1.currLoc == player1_Original.currLoc) and \
				(p1.visited == player1_Original.visited) and \
				(p1.canViewEnd == player1_Original.canViewEnd) and \
				(p1.viewedCoins == player1_Original.viewedCoins)
	if passed:
		numPassed += 1
	printResult("PLAYER SAVE AND LOAD INPLACE", numPassed, \
								totalTests, passed)

	# Now we test not inPlace loading
	p1.savePlayerMaze(filename_p1)
	p1_new = playerMaze.playerMaze()
	p1_new.loadPlayerMaze(filename_p1)

	passed = (p1.maze.numRows == p1_new.maze.numRows) and \
				(p1.maze.numColumns == p1_new.maze.numColumns) and \
				(p1.maze.start == p1_new.maze.start) and \
				(p1.maze.end == p1_new.maze.end) and \
				(p1.maze.cells == p1_new.maze.cells) and \
				(p1.maze.cellNumToExit == p1_new.maze.cellNumToExit) \
				and \
				(p1.maze.coin == p1_new.maze.coin)

	if verbose:
		p1.print()
		p1_new.print()
	if passed:
		numPassed += 1
	printResult("PLAYER MAZE SAVE AND LOAD NOT INPLACE", numPassed, \
								totalTests, passed)

	passed = (p1.currLoc == p1_new.currLoc) and \
				(p1.visited == p1_new.visited) and \
				(p1.canViewEnd == p1_new.canViewEnd) and \
				(p1.viewedCoins == p1_new.viewedCoins)
	if passed:
		numPassed += 1
	printResult("PLAYER SAVE AND LOAD NOT INPLACE", numPassed, \
								totalTests, passed)

	# Now we test data recovery
	filename_p1_old = "../saveFiles/testP1SaveFile_Old.csv"
	player1_Old.savePlayerMaze(filename_p1_old)
	p1_old = playerMaze.playerMaze()
	p1_old.loadPlayerMaze(filename_p1_old)

	passed = (player1_Old.maze.numRows == p1_old.maze.numRows) and \
				(player1_Old.maze.numColumns == p1_old.maze.numColumns) and \
				(player1_Old.maze.start == p1_old.maze.start) and \
				(player1_Old.maze.end == p1_old.maze.end) and \
				(player1_Old.maze.cells == p1_old.maze.cells) and \
				(player1_Old.maze.cellNumToExit == p1_old.maze.cellNumToExit) \
				and \
				(player1_Old.maze.coin == p1_old.maze.coin)

	if verbose:
		player1_Old.print()
		p1_old.print()
	if passed:
		numPassed += 1
	printResult("PLAYER MAZE RECOVERY NOT INPLACE", numPassed, \
								totalTests, passed)

	passed = (player1_Old.currLoc == p1_old.currLoc) and \
				(player1_Old.visited == p1_old.visited) and \
				(player1_Old.canViewEnd == p1_old.canViewEnd) and \
				(player1_Old.viewedCoins == p1_old.viewedCoins)
	if passed:
		numPassed += 1
	printResult("PLAYER RECOVERY NOT INPLACE", numPassed, \
								totalTests, passed)

	# Lastly, we test that the other player can save
	filename_p2 = "../saveFiles/testP2SaveFile.csv"
	p2.savePlayerMaze(filename_p2)
	p2_new = playerMaze.playerMaze()
	p2_new.loadPlayerMaze(filename_p2)

	passed = (p2.maze.numRows == p2_new.maze.numRows) and \
				(p2.maze.numColumns == p2_new.maze.numColumns) and \
				(p2.maze.start == p2_new.maze.start) and \
				(p2.maze.end == p2_new.maze.end) and \
				(p2.maze.cells == p2_new.maze.cells) and \
				(p2.maze.cellNumToExit == p2_new.maze.cellNumToExit) \
				and \
				(p2.maze.coin == p2_new.maze.coin)

	if verbose:
		p2.print()
		p2_new.print()
	if passed:
		numPassed += 1
	printResult("PLAYER 2 MAZE SAVE AND LOAD NOT INPLACE", numPassed, \
								totalTests, passed)

	passed = (p2.currLoc == p2_new.currLoc) and \
				(p2.visited == p2_new.visited) and \
				(p2.canViewEnd == p2_new.canViewEnd) and \
				(p2.viewedCoins == p2_new.viewedCoins)
	if passed:
		numPassed += 1
	printResult("PLAYER 2 SAVE AND LOAD NOT INPLACE", numPassed, \
								totalTests, passed)


	p1.print()

	if verbose:
		p1_new.print()
		p1_old.print()

	p2.print()

	if verbose:
		p2_new.print()



if __name__ == '__main__':
	numRows = 10
	numCols = 15
	if len(sys.argv) > 1:
		numRows = int(sys.argv[1])
		numCols = int(sys.argv[2])

	if len(sys.argv) > 3:
		numPlayers = int(sys.argv[3])
	else:
		numPlayers = 2

	if len(sys.argv) > 4:
		threshold = int(sys.argv[4])
	else:
		threshold = 10

	random.seed('TestSeed')
	test(numRows, numCols, numPlayers, threshold)