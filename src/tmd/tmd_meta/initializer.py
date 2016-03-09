import sys
import string
import math
from state import *
from stateTemplates import *

# This code generates the Turing machine that does everything before writing the code onto the tape

# It's the exact same thing as writer.py, which does everything, except that writeProgram,
# the part where you put the actual code on the tape, is commented out.

def convertStatesToString(listOfStates, output):

    numberOfStates = len(listOfStates)
    
    output.write("States: " + str(numberOfStates) + "\n")
    output.write("\n")
    
    statesIveAlreadyPrinted = {}

    for state in listOfStates:
#       print state.stateName
        
        try:
            assert (not state.stateName in statesIveAlreadyPrinted)
        except:
            print "duplicated state:", state.stateName
            raise       

        statesIveAlreadyPrinted[state.stateName] = None
        
        if state.isStartState:
            output.write("START ")
        
        output.write(state.stateName + ":\n")
        
        for symbol in ["_", "1", "H", "E"]:         
            output.write("\t" + symbol + " -> " + state.getNextStateName(symbol) + "; " + \
                state.getHeadMove(symbol) + "; " + state.getWrite(symbol) + "\n")
        
        output.write("\n")
        
def getFunctionLabelDictionary(functions, path):

    # All line numbers ignore empty lines, input lines and comments. The number that appears in your editor I call a "text number."

    # Maps from functions to a map from labels within that function to the appropriate line number
    functionLabelDictionary = {}
    functionDictionary = {}
    functionLineDictionary = {}
    
    lineNumberToTextNumber = {}
    

    functionCounter = 1

    for function in functions:

        functionLineDictionary[function] = {}
        functionLabelDictionary[function] = {}      
        functionDictionary[function] = functionCounter
 
        functionLines = open(path + string.strip(function) + ".tmd", "r")

        textCounter = 1
        lineCounter = 1
        
        for line in functionLines:
            if not ("input" in line or "//" in line or line == "\n"):

                # getting rid of whitespace, then splitting by colons
                labels = string.split(string.replace(line, " ", ""), ":")[:-1]
                for label in labels:
                    try:
                        assert not label in functionLabelDictionary[function] 
                    except:
                        print "Error: duplicate label", label, "on line", lineCounter, "of function", function
                        raise
                        
                    functionLabelDictionary[function][label] = lineCounter
                
                functionLineDictionary[function][lineCounter] = line
                lineNumberToTextNumber[lineCounter] = textCounter
                lineCounter += 1    
                    
            textCounter += 1
            

        functionCounter += 1
        
    return functionLabelDictionary, functionDictionary, functionLineDictionary, lineNumberToTextNumber
    
def getFunctionVariableDictionary(functions, path):
    functionVariableDictionary = {}
    
    for function in functions:
        
        functionVariableDictionary[function] = {}
        
        functionLines = open(path + string.strip(function) + ".tmd", "r").readlines()
        
        firstLine = functionLines[0]
        
        for i, variableName in enumerate(string.split(firstLine)[1:]):
            functionVariableDictionary[function][variableName] = i+1
            
    return functionVariableDictionary

def convertNumberToBarCode(number, setOfSymbols = ["E", "1"]):

    barCode = ""    
    newBarCode = ""
    barCodeIndexCounter = -1

    overallCounter = 0
    
    incrementing = True

    while overallCounter < number:
        if incrementing:
            if barCodeIndexCounter == -1:
                newBarCode = setOfSymbols[0] + newBarCode
                barCodeIndexCounter = len(newBarCode) - 1
                overallCounter += 1
                barCode = newBarCode
                newBarCode = ""
                incrementing = True 

            else:
                indexOfSymbol = setOfSymbols.index(barCode[barCodeIndexCounter])

                if indexOfSymbol == len(setOfSymbols) - 1:
                    newBarCode = setOfSymbols[0] + newBarCode
                    barCodeIndexCounter -= 1

                else:
                    newBarCode = setOfSymbols[indexOfSymbol + 1] + newBarCode
                    barCodeIndexCounter -= 1
                    incrementing = False

        else:
            if barCodeIndexCounter == -1:
                overallCounter += 1
                barCode = newBarCode
                barCodeIndexCounter = len(barCode) - 1
                newBarCode = ""
                incrementing = True

            else:
                newBarCode = barCode[barCodeIndexCounter] + newBarCode
                barCodeIndexCounter -= 1

    return barCode

def writeFunctionGuts(functionName, functionLines, labelDictionary):
    for line in functionLines:
        pass

# This writes a counter onto the tape, which will count down from x, where x is the number of variables.

def writeCounter(listOfStates, name, inState, x):
    assert x > 0

    # Fencepost for the -1 
    barCode = convertNumberToBarCode(x-1)
    listOfCounterWritingStates = [inState]

    writeHState = State(name + "_counter_H")
    
    listOfStates.append(inState)
    listOfStates.append(writeHState)

    for i in range(1, len(barCode)):
        newState = State(name + "_counter_" + str(i))
        listOfCounterWritingStates.append(newState)
        listOfStates.append(newState)

    outState = State(name + "_counter_out")
    
    listOfCounterWritingStates.append(writeHState)

    writeHState.set3("_", outState, "R", "H")
    
    for i, state in enumerate(listOfCounterWritingStates[:-1]):
        state.set3("_", listOfCounterWritingStates[i+1], "R", barCode[i])

    return outState

def writeEachVariableValue(listOfStates, inState, initValueString, numberOfVariables):

    # inState might have been called write_State1
    write_State2 = State("write_var_value_underscore_2")
    writeNameState = State("write_var_value_name")
    write_State3 = State("write_var_value_underscore_3")
    write_State4 = State("write_var_value_underscore_4")
    write_State5 = State("write_var_value_underscore_5")
    write_State6 = State("write_var_value_underscore_6")
    findHState1 = State("write_var_value_find_H_1")
    decrementCounterState = State("write_var_value_decrement_counter")
    delete1State = State("write_var_value_delete_1")
    findHState2 = State("write_var_value_find_H_2")
    findHState3 = State("write_var_value_find_H_3")
    outState = State("write_var_value_out")

    listOfStates.extend([inState, write_State2, writeNameState, write_State3, write_State4, write_State5, write_State6, \
        findHState1, decrementCounterState, delete1State, findHState2, findHState3])

    listOfInitValueStates = []

    for i in range(len(initValueString)):
        listOfInitValueStates.append(State("write_var_value_initvalue_" + str(i)))
            
    inState.set3("_", write_State2, "R", "_")

    listOfNameSpaceStates = []
    for i in range(int(math.log(numberOfVariables, 2))):
        listOfNameSpaceStates.append(State("write_var_value_name_space_" + str(i)))
    listOfNameSpaceStates.append(writeNameState)

    write_State2.set3("_", listOfNameSpaceStates[0], "R", "_")

    for i, state in enumerate(listOfNameSpaceStates[:-1]):
        state.set3("_", listOfNameSpaceStates[i+1], "R", "_")
        listOfStates.append(state)

    writeNameState.set3("_", write_State3, "R", "E")
    write_State3.set3("_", write_State4, "R", "_")
    write_State4.set3("_", write_State5, "R", "_")
    write_State5.set3("_", write_State6, "R", "_")
    write_State6.set3("_", listOfInitValueStates[0], "R", "_")

    for i, state in enumerate(listOfInitValueStates[:-1]):
        state.set3("_", listOfInitValueStates[i+1], "R", initValueString[i])

    listOfStates.extend(listOfInitValueStates)

    listOfInitValueStates[-1].set3("_", findHState1, "L", "H")

    findSymbol(findHState1, "H", "L", "L", decrementCounterState)
    
    decrementCounterState.set3("E", decrementCounterState, "L", "1")
    decrementCounterState.set3("1", findHState2, "-", "E")
    decrementCounterState.set3("_", delete1State, "R", "_")
    
    delete1State.set3("1", findHState2, "-", "_")
    delete1State.set3("H", outState, "R", "H")

    findSymbol(findHState2, "H", "R", "R", findHState3)
    findSymbolW(findHState3, "H", "R", "R", "_", inState)   

    return outState

def incrementEachIdentifier(listOfStates, inState):

    markState = State("write_var_incr_mark")
    findFinState = State("write_var_incr_find_fin")
    getPastValueLeftState = State("write_var_incr_get_past_value_left")
    findIdentifierState = State("write_var_incr_find_id")
    incrementIdentifierState = State("write_var_incr_id")
    find_State = State("write_var_incr_find_underscore")
    findValueLeftState = State("write_var_incr_find_value_left")
    findValueRightState = State("write_var_incr_find_value_right")
    getPastValueRightState = State("write_var_incr_get_past_value_right")
#   outState = SimpleState("ACCEPT")
    outState = State("write_var_incr_out")

    listOfStates.extend([inState, markState, findFinState, getPastValueLeftState, findIdentifierState, incrementIdentifierState, \
        find_State, findValueLeftState, findValueRightState, getPastValueRightState])

    # inState might have been called findNot_State
    inState.set3("_", inState, "R", "_")
    inState.set3("1", markState, "-", "1")
    inState.set3("E", markState, "-", "E")

    findSymbolW(markState, "_", "R", "R", "H", findFinState)
    
    findSymbol(findFinState, "H", "R", "L", getPastValueLeftState)
    
    findSymbol(getPastValueLeftState, "_", "L", "-", findIdentifierState)
    
    findIdentifierState.set3("_", findIdentifierState, "L", "_")
    findIdentifierState.set3("1", incrementIdentifierState, "-", "1")
    findIdentifierState.set3("E", incrementIdentifierState, "-", "E")
    findIdentifierState.set3("H", findValueRightState, "-", "_")

    incrementIdentifierState.set3("_", findValueLeftState, "L", "E")
    incrementIdentifierState.set3("1", incrementIdentifierState, "L", "E")
    incrementIdentifierState.set3("E", find_State, "-", "1")

    findSymbol(find_State, "_", "L", "-", findValueLeftState)

    findValueLeftState.set3("_", findValueLeftState, "L", "_")
    findValueLeftState.set3("1", getPastValueLeftState, "-", "1")
    findValueLeftState.set3("E", getPastValueLeftState, "-", "E")

    findValueRightState.set3("_", findValueRightState, "R", "_")
    findValueRightState.set3("1", getPastValueRightState, "-", "1")
    findValueRightState.set3("E", getPastValueRightState, "-", "E")
    
    getPastValueRightState.set3("_", inState, "-", "_")
    getPastValueRightState.set3("1", getPastValueRightState, "R", "1")
    getPastValueRightState.set3("E", getPastValueRightState, "R", "E")
    getPastValueRightState.set3("H", outState, "R", "_")

    return outState

# Puts heads in front of all the values, and puts the HH symbol to signal end of variable values
def putHeadsEverywhere(listOfStates, inState):

    # inState might have been called write_State
    writeHState = State("write_var_heads_write_H")
    findValueState = State("write_var_heads_find_value")
    getPastValueState = State("write_var_heads_get_past_value")
    findIdentifierState = State("write_var_heads_find_id")
    getPastIdentifierState = State("write_var_heads_get_past_id")
    getToFinState = State("write_var_heads_get_to_fin")
    outState = State("write_var_heads_out")
#   outState = SimpleState("ACCEPT")

    listOfStates.extend([inState, writeHState, findValueState, getPastValueState, findIdentifierState, getPastIdentifierState, getToFinState])

    inState.set3("_", writeHState, "R", "_")

    writeHState.set3("_", findValueState, "L", "H")
    
    findValueState.set3("_", findValueState, "L", "_")
    findValueState.set3("1", getPastValueState, "-", "1")
    findValueState.set3("E", getPastValueState, "-", "E")
    findValueState.set3("H", getToFinState, "R", "H")

    findSymbolW(getPastValueState, "_", "L", "L", "H", findIdentifierState)

    findIdentifierState.set3("_", findIdentifierState, "L", "_")
    findIdentifierState.set3("1", getPastIdentifierState, "-", "1")
    findIdentifierState.set3("E", getPastIdentifierState, "-", "E")
    
    findSymbol(getPastIdentifierState, "_", "L", "-", findValueState)

    findPattern(getToFinState, outState, listOfStates, "write_var_heads", "H_", "R", "R", "H")

    return outState

def writeVariableValuesSkeleton(listOfStates, inState, numberOfVariables, initValueString):
    inState = writeCounter(listOfStates, "write_var", inState, numberOfVariables)
    inState = writeEachVariableValue(listOfStates, inState, initValueString, numberOfVariables)
    inState = incrementEachIdentifier(listOfStates, inState)
    inState = putHeadsEverywhere(listOfStates, inState)
    return inState  
    
def writeAuxValues(listOfStates, inState, numberOfVariables, numberOfFunctions):
    inState = writeAuxSkeleton(listOfStates, inState, numberOfVariables, numberOfFunctions)
    inState = writeEachVariableName(listOfStates, inState)
    outState = incrementVariableNames(listOfStates, inState)
    return outState
    
def writeAuxSkeleton(listOfStates, inState, numberOfVariables, numberOfFunctions):
    # Write "Keep head in place, write _, line 1, function 1"
    # Then write some blank space for later use for indexing into variables.

    # inState might have been called write_State1
    write_State2 = State("write_aux_underscore_2")
    write_State3 = State("write_aux_underscore_3")
    writeEState1 = State("write_aux_E_1")
    write_State4 = State("write_aux_underscore_4")
    counterInState = State("write_aux_counter_in")
    writeEState2 = State("write_aux_E_2")
    writeHState = State("write_aux_H")
    outState = State("write_aux_out")
#   outState = SimpleState("ACCEPT")    

    listOfStates.extend([inState, write_State2, write_State3, writeEState1, write_State4, writeEState2, writeHState])

    inState.set3("_", write_State2, "R", "_")
    write_State2.set3("_", write_State3, "R", "_")

    listOfLineNumberSpaceStates = []
    for i in range(int(math.log(numberOfVariables, 2))+2):
        listOfLineNumberSpaceStates.append(State("write_aux_line_number_space_" + str(i)))
    listOfLineNumberSpaceStates.append(writeEState1)

    write_State3.set3("_", listOfLineNumberSpaceStates[0], "R", "_")

    for i, state in enumerate(listOfLineNumberSpaceStates[:-1]):
        state.set3("_", listOfLineNumberSpaceStates[i+1], "R", "_")
        listOfStates.append(state)

    writeEState1.set3("_", write_State4, "R", "E")

    write_State4.set3("_", counterInState, "R", "_")

    write_State5 = writeCounter(listOfStates, "write_aux", counterInState, numberOfVariables+1)
    listOfStates.append(write_State5)

    listOfFunctionNameSpaceStates = []
    for i in range(int(math.log(numberOfFunctions, 2))+2):
        listOfFunctionNameSpaceStates.append(State("write_aux_function_name_space_" + str(i)))
    listOfFunctionNameSpaceStates.append(writeEState2)
    
    write_State5.set3("_", listOfFunctionNameSpaceStates[0], "R", "_")

    for i, state in enumerate(listOfFunctionNameSpaceStates[:-1]):
        state.set3("_", listOfFunctionNameSpaceStates[i+1], "R", "_")
        listOfStates.append(state)
    
    writeEState2.set3("_", writeHState, "R", "E")
    
    writeHState.set3("_", outState, "L", "H")

    return outState
    
def writeEachVariableName(listOfStates, inState):
    
    # inState might have been called findCounterState
    name = "write_aux_var"
    decrementCounterState = State(name + "_decr_counter")
    delete1State = State(name + "_delete_1")
    getPastHState = State(name + "_get_past_H")
    findNewVarNameState = State(name + "_find_new_var")
    writeEState = State(name + "_write_E")
    writeHState = State(name + "_write_H")
    outState = State(name + "_out")
    
    listOfStates.extend([inState, decrementCounterState, delete1State, \
        getPastHState, findNewVarNameState, writeEState, writeHState])
    
    findSymbol(inState, "H", "L", "L", decrementCounterState)
    
    decrementCounterState.set3("_", delete1State, "R", "_")
    decrementCounterState.set3("1", getPastHState, "-", "E")
    decrementCounterState.set3("E", decrementCounterState, "L", "1")
    
    delete1State.set3("H", outState, "R", "_")
    delete1State.set3("1", getPastHState, "-", "_")
    
    findSymbol(getPastHState, "H", "R", "R", findNewVarNameState)
    
    findSymbolW(findNewVarNameState, "H", "R", "R", "_", writeEState)
    
    writeEState.set3("_", writeHState, "R", "E")
    
    writeHState.set3("_", inState, "L", "H")
    
    return outState

def incrementVariableNames(listOfStates, inState):
    
    name = "write_aux_incr"
    
    # this might have been inState findFirstEState = State(name + "_find_first_E")
    goRightTwiceState = State(name + "_go_right_twice")
    writeHState1 = State(name + "_write_H_1")
    getToFinState = State(name + "_get_to_fin")
    incrementState = State(name + "_incr")
    pushDown_State = State(name + "_push__")
    pushDown1State = State(name + "_push_1")
    pushDownEState = State(name + "_push_E")
    exitPushState = State(name + "_exit_push")
    findPushyNumberState = State(name + "_find_pushy")
    getPastNumberState = State(name + "_get_past_number")
    moveHOverState = State(name + "_move_H")
    writeEState = State(name + "_write_E")
    write_State1 = State(name + "_underscore_1")
    write_State2 = State(name + "_underscore_2")
    writeHState2 = State(name + "_write_H_2")
    outState = SimpleState("OUT")
    
    listOfStates.extend([inState, goRightTwiceState, writeHState1, getToFinState, \
        incrementState, pushDown_State, \
        pushDown1State, pushDownEState, exitPushState, findPushyNumberState, getPastNumberState, \
        moveHOverState, writeEState, write_State1, write_State2, writeHState2])
    
    
    findSymbolW(inState, "E", "R", "R", "E", goRightTwiceState)
    
    moveBy(goRightTwiceState, name + "_go_right_twice", 2, "R", writeHState1, listOfStates)
    
    writeHState1.set3("_", getToFinState, "R", "H")
    
    findSymbol(getToFinState, "H", "R", "L", incrementState)
    
    incrementState.set3("_", pushDownEState, "R", "_")
    incrementState.set3("1", incrementState, "L", "E")
    incrementState.set3("H", pushDownEState, "R", "H")
    incrementState.set3("E", getPastNumberState, "-", "1")
    
    pushDown_State.set3("_", pushDown_State, "R", "_")
    pushDown_State.set3("1", pushDown1State, "R", "_")
    pushDown_State.set3("H", exitPushState, "R", "_")
    pushDown_State.set3("E", pushDownEState, "R", "_")
    
    pushDown1State.set3("_", pushDown_State, "R", "1")
    pushDown1State.set3("1", pushDown1State, "R", "1")
    pushDown1State.set3("H", exitPushState, "R", "1")
    pushDown1State.set3("E", pushDownEState, "R", "1")
    
    pushDownEState.set3("_", pushDown_State, "R", "E")
    pushDownEState.set3("1", pushDown1State, "R", "E")
    pushDownEState.set3("H", exitPushState, "R", "E")
    pushDownEState.set3("E", pushDownEState, "R", "E")
    
    exitPushState.set3("_", findPushyNumberState, "L", "H") 

    findPushyNumberState.set3("_", findPushyNumberState, "L", "_")
    findPushyNumberState.set3("1", incrementState, "-", "1")
    findPushyNumberState.set3("H", moveHOverState, "R", "_")
    findPushyNumberState.set3("E", findPushyNumberState, "L", "E")
    
    getPastNumberState.set3("_", incrementState, "L", "_")
    getPastNumberState.set3("1", getPastNumberState, "L", "1")
    getPastNumberState.set3("H", moveHOverState, "R", "_")
    getPastNumberState.set3("E", getPastNumberState, "L", "E")
    
    moveHOverState.set3("_", getToFinState, "R", "H")
    moveHOverState.set3("1", moveHOverState, "R", "1")
    moveHOverState.set3("H", writeEState, "R", "_")
    moveHOverState.set3("E", moveHOverState, "R", "E")
    
    writeEState.set3("_", write_State1, "R", "E")
    
    write_State1.set3("_", write_State2, "R", "_")

    write_State2.set3("_", writeHState2, "R", "_")
    
    writeHState2.set3("_", outState, "R", "H")
    
    return outState
    
def writeProgram(listOfStates, inState, functions, functionVariableDictionary, \
    functionLabelDictionary, functionDictionary, path):

    inState = writeProgramSkeleton(listOfStates, inState, functions, functionVariableDictionary, \
        functionLabelDictionary, functionDictionary, path)
    inState = incrementLineNumberIDs(listOfStates, inState)
    inState = markFunctionNames(listOfStates, inState)
    inState = incrementFunctionIDs(listOfStates, inState)
    
    return inState
    
def incrementLineNumberIDs(listOfStates, inState):
    # inState might have been called "write_code_incr_ln_underscore"
    writeHState = State("write_code_incr_ln_H")
    findLineNumberState = State("write_code_incr_ln_find_ln")
    incrementLineNumberState = State("write_code_incr_ln_incr_ln")
    pushEverythingDown_State = State("write_code_incr_ln_push__")
    pushEverythingDown1State = State("write_code_incr_ln_push_1")
    pushEverythingDownHState = State("write_code_incr_ln_push_H")
    pushEverythingDownEState = State("write_code_incr_ln_push_E")
    exitPushState = State("write_code_incr_ln_exit_push")
    findPushyLineNumberState1 = State("write_code_incr_ln_find_pushy_ln_1")
    findPushyLineNumberState2 = State("write_code_incr_ln_find_pushy_ln_2")
    moveIncrementEnderState1 = State("write_code_incr_ln_move_incr_end_1")
    moveIncrementEnderState2 = State("write_code_incr_ln_move_incr_end_2")
    checkForFinState = State("write_code_incr_ln_check_for_fin")
    getToFinState = State("write_code_incr_ln_get_to_fin")
    getToNextFunctionState = State("write_code_incr_ln_get_to_next_function")
    checkIfLastFunctionState = State("write_code_incr_ln_check_if_last_function")
    outState = State("write_code_incr_ln_out")
#   outState = SimpleState("ACCEPT")
    
    listOfStates.extend([inState, writeHState, findLineNumberState, incrementLineNumberState, \
        pushEverythingDown_State, pushEverythingDown1State, pushEverythingDownHState, \
        pushEverythingDownEState, exitPushState, findPushyLineNumberState1, findPushyLineNumberState2, \
        moveIncrementEnderState1, moveIncrementEnderState2, \
        checkForFinState, getToFinState, getToNextFunctionState, checkIfLastFunctionState])
    
    inState.set3("_", writeHState, "R", "_")
    writeHState.set3("_", findLineNumberState, "L", "H")
    
    findSymbol(findLineNumberState, "H", "L", "L", incrementLineNumberState)
    
    incrementLineNumberState.set3("_", pushEverythingDownEState, "R", "_")
    incrementLineNumberState.set3("1", incrementLineNumberState, "L", "E")
    incrementLineNumberState.set3("H", moveIncrementEnderState1, "R", "H")
    incrementLineNumberState.set3("E", findLineNumberState, "L", "1")
    
    # push everything down until "_H_" is found
    pushEverythingDown_State.set3("_", pushEverythingDown_State, "R", "_")
    pushEverythingDown_State.set3("1", pushEverythingDown1State, "R", "_")
    pushEverythingDown_State.set3("H", exitPushState, "R", "_")
    pushEverythingDown_State.set3("E", pushEverythingDownEState, "R", "_")

    pushEverythingDown1State.set3("_", pushEverythingDown_State, "R", "1")
    pushEverythingDown1State.set3("1", pushEverythingDown1State, "R", "1")
    pushEverythingDown1State.set3("H", pushEverythingDownHState, "R", "1")
    pushEverythingDown1State.set3("E", pushEverythingDownEState, "R", "1")
    
    pushEverythingDownHState.set3("_", pushEverythingDown_State, "R", "H")
    pushEverythingDownHState.set3("1", pushEverythingDown1State, "R", "H")
    pushEverythingDownHState.set3("H", pushEverythingDownHState, "R", "H")
    pushEverythingDownHState.set3("E", pushEverythingDownEState, "R", "H")
    
    pushEverythingDownEState.set3("_", pushEverythingDown_State, "R", "E")
    pushEverythingDownEState.set3("1", pushEverythingDown1State, "R", "E")
    pushEverythingDownEState.set3("H", pushEverythingDownHState, "R", "E")
    pushEverythingDownEState.set3("E", pushEverythingDownEState, "R", "E")  
    
    exitPushState.set3("_", findPushyLineNumberState1, "L", "H")
    exitPushState.set3("1", pushEverythingDown1State, "R", "H")
    exitPushState.set3("H", pushEverythingDownHState, "R", "H")
    exitPushState.set3("E", pushEverythingDownEState, "R", "H")
        
    # need to find a "1H" or "_H" pattern; this indicates something that hasn't 
    # already been incremented
    findSymbol(findPushyLineNumberState1, "H", "L", "L", findPushyLineNumberState2)
    
    findPushyLineNumberState2.set3("_", incrementLineNumberState, "-", "_")
    findPushyLineNumberState2.set3("1", incrementLineNumberState, "-", "1")
    findPushyLineNumberState2.set3("H", moveIncrementEnderState1, "R", "H")
    findPushyLineNumberState2.set3("E", findPushyLineNumberState1, "L", "E")
    
    moveIncrementEnderState1.set3("H", moveIncrementEnderState2, "R", "H")
    
    # if we find a "_H" pattern then we know we're done
    # otherwise we delete the first H we see and go another round
    
    moveIncrementEnderState2.set3("_", checkForFinState, "R", "_")
    moveIncrementEnderState2.set3("1", moveIncrementEnderState2, "R", "1")
    moveIncrementEnderState2.set3("H", getToFinState, "R", "_")
    moveIncrementEnderState2.set3("E", moveIncrementEnderState2, "R", "E")
    
    checkForFinState.set3("_", checkForFinState, "R", "_")
    checkForFinState.set3("1", moveIncrementEnderState2, "R", "1")
    checkForFinState.set3("H", getToNextFunctionState, "L", "H")
    checkForFinState.set3("E", moveIncrementEnderState2, "R", "E")
    
    findPattern(getToFinState, findLineNumberState, listOfStates, "write_code_incr_ln_get_to_fin", \
        "_H", "R", "L", "H")
        
    findPattern(getToNextFunctionState, checkIfLastFunctionState, listOfStates, "write_code_incr_ln_get_to_next_function", "HH", "L", "L", "_") 
    getToNextFunctionState.setWrite("H", "_")
    
    checkIfLastFunctionState.set3("_", findLineNumberState, "-", "_")
    checkIfLastFunctionState.set3("H", outState, "R", "H")
    
    return outState
    
    
# finds function name locations and marks them with an "H"  
def markFunctionNames(listOfStates, inState):
    
    name = "write_code_mark_fn"
    
    readSymbolReadState = State(name + "_read_symbol_read")
    readSymbolWrittenState = State(name + "_read_symbol_written")
    readHeadMoveState = State(name + "_read_head_move")
    checkForLineState = State(name + "_check_for_line")
    getPastLineNumberState = State(name + "_get_past_ln")
    checkForLineTypeState = State(name + "_check_for_line_type")
    getPastVariableNameState = State(name + "_get_past_var_name")
    getPastArgumentNameState = State(name + "_get_past_arg_name")
    checkForArgumentState = State(name + "_check_for_arg")
    checkForFunctionState = State(name + "_check_for_func")
    outState = State(name + "_out")
#   outState = SimpleState("ACCEPT")

    listOfStates.extend([inState, readSymbolReadState, readSymbolWrittenState, \
        readHeadMoveState, checkForLineState, getPastLineNumberState, \
        checkForLineTypeState, getPastVariableNameState, getPastArgumentNameState, \
        checkForArgumentState, checkForFunctionState])
    
    #inState might have been checkForReactionState
    inState.set3("_", checkForLineState, "R", "_")
    inState.set3("1", readSymbolReadState, "R", "1")
    inState.set3("H", outState, "L", "H")
    
    moveBy(readSymbolReadState, "", 1, "R", readSymbolWrittenState)
    
    moveBy(readSymbolWrittenState, "", 1, "R", readHeadMoveState)
    
    moveBy(readHeadMoveState, "", 1, "R", getPastVariableNameState)
    # a goto looks like a variable name
        
    checkForLineState.set3("_", checkForFunctionState, "R", "_")
    checkForLineState.set3("1", getPastLineNumberState, "R", "1")
    checkForLineState.set3("E", getPastLineNumberState, "R", "E")
    
    findSymbol(getPastLineNumberState, "_", "R", "R", checkForLineTypeState)
    
    checkForLineTypeState.set3("_", inState, "R", "_")
    checkForLineTypeState.set3("1", getPastVariableNameState, "-", "1")
    checkForLineTypeState.set3("E", getPastArgumentNameState, "-", "E")
    
    findSymbol(getPastVariableNameState, "_", "R", "R", inState)
    
    findSymbol(getPastArgumentNameState, "_", "R", "R", checkForArgumentState)
    
    checkForArgumentState.set3("_", checkForLineState, "R", "_")
    checkForArgumentState.set3("1", getPastArgumentNameState, "-", "1")
    checkForArgumentState.set3("E", getPastArgumentNameState, "-", "E")
        
    # this is the whole point! Note there's a minor inefficency here
    # in that no information is gained from this symbol. Wonder if this could
    # be easily fixed?
    checkForFunctionState.set3("E", inState, "R", "H")
        
    return outState
        
def incrementFunctionIDs(listOfStates, inState):
    
    name = "write_code_incr_fn"
    
    incrementState = State(name + "_incr")
    pushEverythingDown_State = State(name + "_push__")
    pushEverythingDown1State = State(name + "_push_1")
    pushEverythingDownHState = State(name + "_push_H")
    pushEverythingDownEState = State(name + "_push_E")
    exitPushState = State(name + "_exit_push")
    findPushyFunctionNameState1 = State(name + "_find_pushy_1")
    findPushyFunctionNameState2 = State(name + "_find_pushy_2")
    moveIncrementEnderState1 = State(name + "_move_incr_end_1")
    moveIncrementEnderState2 = State(name + "_move_incr_end_2")
    checkForFinState = State(name + "_check_for_fin")
    getToFinState = State(name + "_get_to_fin")
    outState = State(name + "_out")
#   outState = SimpleState("ACCEPT")
    
    listOfStates.extend([inState, incrementState, pushEverythingDown_State, \
        pushEverythingDown1State, pushEverythingDownHState, pushEverythingDownEState, \
        exitPushState, findPushyFunctionNameState1, findPushyFunctionNameState2, \
        moveIncrementEnderState1, moveIncrementEnderState2, checkForFinState, getToFinState])
    
    # inState might have been called findFunctionNameState
    findSymbol(inState, "H", "L", "L", incrementState)
    
    incrementState.set3("_", pushEverythingDownEState, "R", "_")
    incrementState.set3("1", incrementState, "L", "E")
    incrementState.set3("H", moveIncrementEnderState1, "R", "H")
    incrementState.set3("E", inState, "L", "1")
    
    pushEverythingDown_State.set3("_", pushEverythingDown_State, "R", "_")
    pushEverythingDown_State.set3("1", pushEverythingDown1State, "R", "_")
    pushEverythingDown_State.set3("H", exitPushState, "R", "_")
    pushEverythingDown_State.set3("E", pushEverythingDownEState, "R", "_")
    
    pushEverythingDown1State.set3("_", pushEverythingDown_State, "R", "1")
    pushEverythingDown1State.set3("1", pushEverythingDown1State, "R", "1")
    pushEverythingDown1State.set3("H", pushEverythingDownHState, "R", "1")
    pushEverythingDown1State.set3("E", pushEverythingDownEState, "R", "1")

    pushEverythingDownHState.set3("_", pushEverythingDown_State, "R", "H")
    pushEverythingDownHState.set3("1", pushEverythingDown1State, "R", "H")
    pushEverythingDownHState.set3("H", pushEverythingDownHState, "R", "H")
    pushEverythingDownHState.set3("E", pushEverythingDownEState, "R", "H")
    
    pushEverythingDownEState.set3("_", pushEverythingDown_State, "R", "E")
    pushEverythingDownEState.set3("1", pushEverythingDown1State, "R", "E")
    pushEverythingDownEState.set3("H", pushEverythingDownHState, "R", "E")
    pushEverythingDownEState.set3("E", pushEverythingDownEState, "R", "E")

    exitPushState.set3("_", findPushyFunctionNameState1, "L", "H")
    
    findSymbol(findPushyFunctionNameState1, "H", "L", "L", findPushyFunctionNameState2)
    
    findPushyFunctionNameState2.set3("_", incrementState, "-", "_")
    findPushyFunctionNameState2.set3("1", incrementState, "-", "1")
    findPushyFunctionNameState2.set3("H", moveIncrementEnderState1, "R", "H")
    findPushyFunctionNameState2.set3("E", findPushyFunctionNameState1, "-", "E")
    
    moveIncrementEnderState1.set3("H", moveIncrementEnderState2, "R", "H")
    
    moveIncrementEnderState2.set3("_", checkForFinState, "R", "_")
    moveIncrementEnderState2.set3("1", moveIncrementEnderState2, "R", "1")
    moveIncrementEnderState2.set3("H", getToFinState, "R", "_")
    moveIncrementEnderState2.set3("E", moveIncrementEnderState2, "R", "E")
    
    checkForFinState.set3("_", moveIncrementEnderState2, "-", "_")
    checkForFinState.set3("1", moveIncrementEnderState2, "-", "1")
    checkForFinState.set3("H", outState, "L", "H")
    checkForFinState.set3("E", moveIncrementEnderState2, "-", "E")
    
    findPattern(getToFinState, inState, listOfStates, name, "_H", "R", "L", "H")
    
    return outState 
    
def firstPrepTopFunction(inState, listOfStates, name):
    markFirstFunctionState = State(name + "_mark_first_fn")
    writeHState1 = State(name + "_write_H_1")
    getToFinState = State(name + "_get_to_fin")
    writeHState2 = State(name + "_write_H_2")
    writeHState3 = State(name + "_write_H_3")
    getPastFinState = State(name + "_get_past_fin")
    findHState = State(name + "_find_H")
    outState = State(name + "_out")
    
    listOfStates.extend([inState, markFirstFunctionState, writeHState1, getToFinState,
        writeHState2, writeHState3, getPastFinState, findHState])
    
    findPattern(inState, markFirstFunctionState, listOfStates, name + "_mark_first_fn", "HH", "L", "R", "H")
    
    moveBy(markFirstFunctionState, name + "_mark_first_fn", 2, "R", writeHState1, listOfStates)

    writeHState1.set3("_", getToFinState, "R", "H")
    
    findSymbol(getToFinState, "H", "R", "R", writeHState2)
    
    writeHState2.set3("_", writeHState3, "R", "H")
    
    writeHState3.set3("_", getPastFinState, "L", "H")
    
    getPastFinState.set3("_", findHState, "-", "_")
    getPastFinState.set3("H", getPastFinState, "L", "H")
    
    findSymbol(findHState, "H", "L", "L", outState)
    
    return outState    
    
def write(listOfStates, inState, numberOfVariables, initValueString, numberOfFunctions, \
    functions, functionVariableDictionary, functionLabelDictionary, functionDictionary, path):
    
    inState = writeVariableValuesSkeleton(listOfStates, inState, numberOfVariables, initValueString)    
    inState = writeAuxValues(listOfStates, inState, numberOfVariables, numberOfFunctions)
    inState = writeProgram(listOfStates, inState, functions, functionVariableDictionary,
        functionLabelDictionary, functionDictionary, path)
    
    # This is initial preparation for the execution of the CPU
    inState = firstPrepTopFunction(inState, listOfStates, "first_prep")
        
    return inState  
    
def main():
    

################################################################

### Setting up the functionLabelDictionary

    dirName = sys.argv[1]
    
    path = "../tmd_dirs/" + dirName + "/"

    try:
        functions = [string.strip(x) for x in open(path + "functions", "r").readlines()]
    except:  
        raise Exception("No functions file found in directory " + path) 

    functionLabelDictionary, functionDictionary, functionLineDictionary, \
        lineNumberToTextNumber = getFunctionLabelDictionary(functions, path)
        
    functionVariableDictionary = getFunctionVariableDictionary(functions, path)

###################################################################

    try:
        initValueString = string.strip(open(path + "initvar", "r").read()) + "H"
    except:
        raise Exception("No initvar file found in directory " + path)

###################################################################
    
    inState = State("start")
    inState.makeStartState()

    listOfStates = []
    
    mainFunctionInputLine = open(path + functions[0] + ".tmd", "r").readlines()[0]
    
    numberOfVariables = len(string.split(mainFunctionInputLine)) - 1
    numberOfFunctions = len(functions)

    inState = writeVariableValuesSkeleton(listOfStates, inState, numberOfVariables, initValueString)    
    outState = writeAuxValues(listOfStates, inState, numberOfVariables, numberOfFunctions)
    
#   inState = writeProgram(listOfStates, inState, functions, functionVariableDictionary,
#       functionLabelDictionary, functionDictionary, path)

    convertStatesToString(listOfStates, open("../../tm/tm4/tm4_files/" + dirName + "_init.tm4", "w"))



################################################################
        


if __name__ == "__main__":
    main()