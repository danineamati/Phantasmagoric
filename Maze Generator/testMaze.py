from maze import *
import playerMaze
import genmaze

import random
import sys
import copy

def printResult(text, numPassed, totalTests, truth):
	'''Formats the print result.'''
	text = text + (32 - len(text)) * ' '

	if truth:
		print(text + "PASSED {} / {}".format(numPassed, totalTests))
	else:
		print(text + "FAILED {} / {}".format(numPassed, totalTests), " * ")


def test(numRows, numCols, numPlayers, threshold, verbose = False):
	numPassed = 0

	totalTests = 8 + numPlayers

	if numRows == 10 and numCols == 15 and numPlayers == 2:
		totalTests += 18

	testMaze = genmaze.main(numRows, numCols, numPlayers, threshold,\
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

	filename = 'testSaveFile.csv'
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

	player1_Original = copy.deepcopy(p1)

	moves = ["South", "West", "South", "South", "West", "South", "East", \
				"East", "North", "North", "South", "South", "West", "West", \
				"South", "South", "West", "North", "West", "West", "West", \
				"South", "West", "West", "West", "West", "North", "North"]
	for move in moves:
		if p1.checkMove(move):
			p1.moveLocation(move)
		else:
			break

	p1.print()
	p2.print()

	# Now we check that we can save and load player data
	filename_p1 = "testP1SaveFile.csv"
	p1.savePlayerMaze(filename_p1)



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