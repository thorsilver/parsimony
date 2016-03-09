# This program melds together two Turing machines;
# that is, if the first machine ends up in an "OUT" state, 
# this program outputs a TM where the out state of the first machine
# is the start state of the second

import sys
import tmsim

def alphabetMSToTS():
    return ["a", "b"]

def convertStatesToString(listOfStates, output):

    numberOfStates = len(listOfStates)
    
    output.write("States: " + str(numberOfStates) + "\n")
    output.write("\n")
    
    statesIveAlreadyPrinted = {}

    for state in listOfStates:      
        try:
            assert (not state.stateName in statesIveAlreadyPrinted)
        except AssertionError:
            print state.stateName
            raise
        
        statesIveAlreadyPrinted[state.stateName] = None

        if state.isStartState:
            output.write("START ")
        
        output.write(state.stateName + ":\n")
        
        for symbol in alphabetMSToTS():         
            output.write("\t" + symbol + " -> " + state.getNextStateName(symbol) + "; " + \
                state.getHeadMove(symbol) + "; " + state.getWrite(symbol) + "\n")
        
        output.write("\n")

if __name__ == "__main__":
	inMachineName = sys.argv[1]
	outMachineName = sys.argv[2]
		
	try:
		assert inMachineName != outMachineName
	except:
		print "Error: cannot meld two machines that have the same name."
		raise
	
	inMachine = tmsim.SingleTapeTuringMachine("../tm2_files/" + sys.argv[1] + ".tm2", \
        alphabetMSToTS())
	outMachine = tmsim.SingleTapeTuringMachine("../tm2_files/" + sys.argv[2] + ".tm2", \
        alphabetMSToTS())
	
	for state in inMachine.listOfRealStates:		
		for symbol in alphabetMSToTS():
			nextState = state.getNextState(symbol)
			if nextState.stateName == "OUT":
				state.setNextState(symbol, outMachine.startState)
		
	for state in outMachine.listOfRealStates:		
		state.isStartState = False
		
	convertStatesToString(inMachine.listOfRealStates + outMachine.listOfRealStates, \
		open("../tm2_files/" + sys.argv[3] + ".tm2", "w"))