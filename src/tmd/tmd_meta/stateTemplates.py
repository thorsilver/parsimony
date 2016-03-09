from state import *
import sys

def moveBy(state, name, amount, direction, nextState, listOfStates=None, alphabet=["_", "1", "H", "E"]):
	
	returnList = [state]
	
	if amount == 0:
		state.setAllNextStates(nextState)

	elif amount == 1:
		state.setAllNextStates(nextState)
		state.setAllHeadMoves(direction)

	else:
		prevState = state
		for i in range(amount - 1):
			currentState = State(name + "_move_by_" + str(i+1), None, alphabet)
			
			if not listOfStates == None:
				listOfStates.append(currentState)

			returnList.append(currentState)
			prevState.setAllNextStates(currentState)
			prevState.setAllHeadMoves(direction)
			
			prevState = currentState
	
		currentState.setAllNextStates(nextState)
		currentState.setAllHeadMoves(direction)

	return returnList

def moveByNoStandingInPlace(state, name, amount, direction, nextState, listOfStates=None, alphabet=["_", "1", "H", "E"]):
    
    returnList = [state]
    
    if amount == 0:
        moveLeftState = State(name + "_move_by_move_left", None, alphabet)
        
        state.setAllNextStates(moveLeftState)
        state.setAllHeadMoves("R")
        
        moveLeftState.setAllNextStates(nextState)
        moveLeftState.setAllHeadMoves("L")
        
        if not listOfStates == None:
            listOfStates.append(moveLeftState)
            
        return [state, moveLeftState]    
        
    else:
        return moveBy(state, name, amount, direction, nextState, listOfStates, alphabet)


def findEnd(state, nextState):
	findSymbol(state, "E", "R", "-", nextState)

def findSymbol(state, symbol, direction, lastDirection, nextState):
	findSymbolW(state, symbol, direction, lastDirection, symbol, nextState)
	

def findSymbolW(state, symbol, direction, lastDirection, lastWrite, nextState):

	state.setAllNextStates(state)
	state.setNextState(symbol, nextState)

	state.setAllHeadMoves(direction)
	state.setHeadMove(symbol, lastDirection)
	
	state.setWrite(symbol, lastWrite)

# Helper function for findPattern.
# if string1 is "bbab", and string2 is "abb", then it returns "bb"; in other words, it finds the longest match between the start of string1 and the end of string2.
def getBestPrefix(string1, string2):
	# if string2 ends in string1
#	print string1, string2
	
	if string1 == "":	
		return ""

	elif string1 == string2[-len(string1):]:
		return string1
	
	else:
		return getBestPrefix(string1[:-1], string2)

# Finds the pattern, for example "H_". You can find it from the left or the right; you should NOT reverse the input if you're going left. (The function does it for you)
def findPattern(state, nextState, listOfStates, name, pattern, direction, lastDirection, lastWrite, alphabet=["_", "1", "H", "E"]):

	# reverse the pattern's order if we're going left
	if direction == "L":
		truePattern = pattern[::-1]

	else:
		truePattern = pattern

	stringSeenToStateDict = {"": state, truePattern: nextState}

	stringSoFar = ""	
	for char in truePattern[:-1]:
		stringSoFar += char
		
		stringSeenToStateDict[stringSoFar] = State(name + "_recog_pattern_" + stringSoFar)
		listOfStates.append(stringSeenToStateDict[stringSoFar])

	stringSoFar = ""
	for char in truePattern:

		stateSoFar = stringSeenToStateDict[stringSoFar]

		# for each possible next transition, go to the longest prefix of the pattern from what's been seen
		for symbol in alphabet:
			newString = stringSoFar + symbol
	
			if newString == truePattern:
				stateSoFar.setNextState(symbol, nextState)
				stateSoFar.setHeadMove(symbol, lastDirection)
				stateSoFar.setWrite(symbol, lastWrite)

			else:
				stateSoFar.setNextState(symbol, stringSeenToStateDict[getBestPrefix(pattern, newString)])
				stateSoFar.setHeadMove(symbol, direction)

		stringSoFar += char
