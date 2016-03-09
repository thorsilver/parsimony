import sys
import string
import math
from state import *
from stateTemplates import *

# return is already at the end of stack, so I split this
def standardPrepTopFunctionExceptReturn(inState, listOfStates, name, outState):
    # inState might have been called findStack
    getToEndOfStack = State(name + "_get_to_end_of_stack")
    if outState == None:
        outState = State(name + "_out")
        
    listOfStates.extend([inState, getToEndOfStack])
    
    inState.set3("_", inState, "R", "_")
    inState.set3("E", getToEndOfStack, "-", "E")
    
    findPattern(getToEndOfStack, outState, listOfStates, name + "_find_end_stack", "___",
        "R", "-", "_")

def standardPrepTopFunction(inState, listOfStates, name, outState):    
    # inState might have been called getToFirstFunction   
    writeH = State(name + "_write_H")
    if outState == None:
        outState = State(name + "_out")
                     
    listOfStates.extend([inState, writeH])         
             
    inState.set3("_", inState, "R", "_")
    inState.set3("E", writeH, "L", "E")
    
    writeH.set3("_", outState, "L", "H")
    
    return outState
    
def commonPrepTopFunction(inState, listOfStates, name):    
    # inState should have been called getRidOfSeparator
    getToStartLastFunction = State(name + "_get_to_start_last_func")
    writeH2 = State(name + "_write_H_2")
    outState = State(name + "_out")
    
    listOfStates.extend([inState, getToStartLastFunction, writeH2])
    
    inState.set3("_", inState, "L", "_")
    inState.set3("1", getToStartLastFunction, "-", "1")
    inState.set3("H", inState, "-", "_")
    inState.set3("E", getToStartLastFunction, "-", "E")
    
    findPattern(getToStartLastFunction, writeH2, listOfStates, name + "_get_to_start_last_func", "__",
        "L", "R", "_")
        
    writeH2.set3("_", outState, "R", "H")
    
    return outState
    
def prepLine(inState, listOfStates, name):
    # inState might have been called getPastStack
    findLineNumber = State(name + "_find_ln")
    getToStartLineNumber = State(name + "_get_to_start_ln")
    markFirstLine = State(name + "_mark_first_line")
    getPastFunctionName = State(name + "_get_past_fn")
    writeH = State(name + "_write_H")
    getToLineNumber = State(name + "_get_to_ln")
    outState = State(name + "_out")
    
    listOfStates.extend([inState, findLineNumber, getToStartLineNumber, markFirstLine, getPastFunctionName, 
        writeH, getToLineNumber])
    
    findPattern(inState, findLineNumber, listOfStates, name + "_get_past_stack", "___", "L", "-", "_")
    
    findLineNumber.set3("_", findLineNumber, "L", "_")
    findLineNumber.set3("1", getToStartLineNumber, "-", "1")
    findLineNumber.set3("E", getToStartLineNumber, "-", "E")
    
    findSymbolW(getToStartLineNumber, "_", "L", "R", "H", markFirstLine)
    
    findSymbolW(markFirstLine, "H", "R", "R", "_", getPastFunctionName)
    
    findSymbol(getPastFunctionName, "_", "R", "R", writeH)
        
    writeH.set3("_", getToLineNumber, "L", "H")
    
    findSymbol(getToLineNumber, "H", "L", "R", outState)

    return outState
    
def prepCopyVarName(inState, listOfStates, name):
    # inState might have been called destroyHState
    findHState = State(name + "_find_H")
    outState = State(name + "_out")
    
    listOfStates.extend([inState, findHState])
    
    findSymbolW(inState, "H", "L", "-", "_", findHState)
    
    findSymbol(findHState, "H", "R", "R", outState)
    
    return outState
    
# This function also creates the two underscores needed for the new function on the stack (should there be a function call)
def readLineType(inState, listOfStates, name):
    # inState might have been called moveRightState
    getPastAuxLineNumber = State(name + "_get_past_aux_ln")
    writeH = State(name + "_write_H")
    findFirstFunction = State(name + "_find_first_func")
    findThreeUnderscores = State(name + "_find_aux_fin")
    write1 = State(name + "_write_1")
    findAux = State(name + "_find_aux")
    checkIfShouldPushMore = State(name + "_check_if_should_push_more")
    findLine = State(name + "_find_line")
    getPastLineNumber = State(name + "_get_past_ln")
    readType = State(name + "_read_type")
    outStateDictionary = {"return": State(name + "_out_return"), "direct": State(name + "_out_direct"),
        "function": State(name + "_out_function")}
        
    listOfStates.extend([inState, getPastAuxLineNumber, writeH, findFirstFunction, findThreeUnderscores, 
        write1, findAux, checkIfShouldPushMore, findLine, getPastLineNumber, readType])
    
    moveBy(inState, name + "_get_past_early_garbage", 1, "R", getPastAuxLineNumber, listOfStates)
    
    findSymbol(getPastAuxLineNumber, "_", "R", "R", writeH)
    
    writeH.set3("_", findFirstFunction, "-", "H")
    
    findSymbol(findFirstFunction, "E", "R", "-", findThreeUnderscores)
    
    findPattern(findThreeUnderscores, write1, listOfStates, name + "_find_aux_fin", "___", "R", "R", "H")
    
    pushIn, pushOut = pushDownTilHHH("_", listOfStates, name + "_create_underscore_push")
    listOfStates.append(pushOut)
    
    # The writing 1 is to mark the tape, telling it to create an underscore twice
    write1.set3("_", pushIn, "R", "1")
    
    findSymbol(pushOut, "H", "L", "L", findAux)
    
    findSymbol(findAux, "H", "L", "R", checkIfShouldPushMore)
    
    checkIfShouldPushMore.set3("_", findLine, "-", "_")
    checkIfShouldPushMore.set3("1", pushIn, "-", "_")
    
    findSymbolW(findLine, "H", "R", "R", "_", getPastLineNumber)

    findSymbol(getPastLineNumber, "_", "R", "R", readType)
    
    readType.set3("_", outStateDictionary["return"], "-", "_")
    readType.set3("1", outStateDictionary["direct"], "L", "H")
    readType.set3("E", outStateDictionary["function"], "R", "E")

    return outStateDictionary

def pushDownTilHHH(startSymbol, listOfStates, name):
    startDict = {"_": State(name + "__"), "1": State(name + "_1"), 
        "H": State(name + "_H"), "E": State(name + "_E")}
        
    pushHH = State(name + "_HH")
    exit = State(name + "_exit")
    getPastFin = State(name + "_get_past_fin")
    outState = State(name + "_out")
    
    listOfStates.extend(startDict.values())
    listOfStates.extend([pushHH, exit, getPastFin])
    
    for symbolPush in ["_", "1", "H", "E"]:
        for symbolRead in ["_", "1", "H", "E"]:
            startDict[symbolPush].set3(symbolRead, startDict[symbolRead], "R", symbolPush)
            
    startDict["H"].set3("H", pushHH, "R", "H")
    
    pushHH.set3("_", startDict["_"], "R", "H")
    pushHH.set3("1", startDict["1"], "R", "H")
    pushHH.set3("H", exit, "R", "H")
    pushHH.set3("E", startDict["E"], "R", "H")
    
    exit.set3("_", getPastFin, "-", "H")
    
    getPastFin.set3("_", outState, "-", "_")
    getPastFin.set3("H", getPastFin, "L", "H")
    
    if startSymbol == "all":
        return startDict, outState
    else:
        return startDict[startSymbol], outState

def simpleTravelRight(inState, listOfStates, name, lastMove="R", lastWrite="H", outState=None):
    
    if outState == None:
        outState = State(name + "_out")
    
    listOfStates.extend([inState])

    findSymbolW(inState, "H", "R", "R", lastWrite, outState)
    
    return outState
    
def simpleTravelLeft(inState, listOfStates, name, lastMove="R", lastWrite="H", outState=None):
    
    foundHState = State(name + "_found_H")
    if outState == None:
        outState = State(name + "_out")    

    listOfStates.extend([inState])
        
    findSymbolW(inState, "H", "L", lastMove, lastWrite, outState)
    
    return outState
    
def travelAuxToVars(inState, listOfStates, name, lastMove="R", lastWrite="H", outState=None):
    # inState should have been called findHHState
    findValue = State(name + "_find_value")
    getPastValue = State(name + "_get_past_value")
    findID = State(name + "_find_id")
    getPastID = State(name + "_get_past_id")
    if outState == None:
        outState = State(name + "_out")
    
    listOfStates.extend([inState, findValue, getPastValue, findID, getPastID])
    
    findPattern(inState, findValue, listOfStates, name + "_get_to_vars", "HH", "L", "L", "H")
    
    findValue.set3("_", findValue, "L", "_")
    findValue.set3("1", getPastValue, "-", "1")
    findValue.set3("H", findValue, "L", "H")
    findValue.set3("E", getPastValue, "-", "E")
    
    findSymbol(getPastValue, "_", "L", "-", findID)    
    
    findID.set3("_", findID, "L", "_")
    findID.set3("1", getPastID, "-", "1")
    findID.set3("H", findID, "L", "H")
    findID.set3("E", getPastID, "-", "E")
    
    getPastID.set3("_", findValue, "-", "_")
    getPastID.set3("1", getPastID, "L", "1")
    getPastID.set3("H", outState, lastMove, lastWrite)
    getPastID.set3("E", getPastID, "L", "E")
    
    return outState
    
# allows for the possibility of an ID looking like __E1H__
# (H at the end)
def travelAuxToVarsCareful(inState, listOfStates, name, lastMove="R", lastWrite="H", outState=None):    
    # inState should have been called findHHState
    findValueNoH = State(name + "_find_value_no_H")
    findValueSeenH = State(name + "_find_value_seen_H")
    getPastValueNoH = State(name + "_get_past_value_no_H")
    getPastValueSeenH = State(name + "_get_past_value_seen_H")
    findIDNoH = State(name + "_find_id_no_H")
    findIDSeenH = State(name + "_find_id_seen_H")
    getPastID = State(name + "_get_past_id")
    if outState == None:
        outState = State(name + "_out")
    
    listOfStates.extend([inState, findValueNoH, findValueSeenH, getPastValueNoH, getPastValueSeenH,
        findIDNoH, findIDSeenH, getPastID])
    
    findPattern(inState, findValueNoH, listOfStates, name + "_get_to_vars", "HH", "L", "L", "H")
    
    findValueNoH.set3("_", findValueNoH, "L", "_")
    findValueNoH.set3("1", getPastValueNoH, "-", "1")
    findValueNoH.set3("H", findValueSeenH, "L", "H")
    findValueNoH.set3("E", getPastValueNoH, "-", "E")
    
    findValueSeenH.set3("_", findValueSeenH, "L", "_")
    findValueSeenH.set3("1", getPastValueSeenH, "-", "1")
    findValueSeenH.set3("E", getPastValueSeenH, "-", "E")
    
    getPastValueNoH.set3("_", findIDNoH, "-", "_")
    getPastValueNoH.set3("1", getPastValueNoH, "L", "1")
    getPastValueNoH.set3("H", getPastValueSeenH, "L", "H")
    getPastValueNoH.set3("E", getPastValueNoH, "L", "E")
    
    findSymbol(getPastValueSeenH, "_", "L", "-", findIDSeenH)
    
    findIDNoH.set3("_", findIDNoH, "L", "_")
    findIDNoH.set3("H", findIDSeenH, "L", "H")
    
    findIDSeenH.set3("_", findIDSeenH, "L", "_")
    findIDSeenH.set3("1", getPastID, "-", "1")
    findIDSeenH.set3("H", outState, lastMove, lastWrite)
    findIDSeenH.set3("E", getPastID, "-", "E")
    
    getPastID.set3("_", findValueNoH, "-", "_")
    getPastID.set3("1", getPastID, "L", "1")
    getPastID.set3("H", outState, lastMove, lastWrite)
    getPastID.set3("E", getPastID, "L", "E")
    
    return outState
    
def travelVarsToAux(inState, listOfStates, name, lastMove="R", lastWrite="H", outState=None):
    #inState should have been findHHState
    findHState = State(name + "_find_H")
    if outState == None:
        outState = State(name + "_out")
        
    listOfStates.extend([inState, findHState])
    
    findPattern(inState, findHState, listOfStates, name + "_get_to_aux", "HH", "R", "R", "H")
    
    findSymbolW(findHState, "H", "R", lastMove, lastWrite, outState)
    
    return outState
    
def moveVarMarker(inState, listOfStates, name, outState=None):
    # inState might have been called getPastID1
    findVar = State(name + "_find_var")
    getPastVar = State(name + "_get_past_var")
    findID = State(name + "_find_id")
    getPastID = State(name + "_get_past_id")
    getPastTapeHead = State(name + "_get_past_tape_head")
    getBackToFailedVar = State(name + "_get_back_to_failed_var")
    if outState == None:
        outState = State(name + "_out")
    
    listOfStates.extend([inState, findVar, getPastVar, findID, getPastID, getPastTapeHead, 
        getBackToFailedVar])
    
    findSymbol(inState, "_", "L", "-", findVar)
    
    findVar.set3("_", findVar, "L", "_")
    findVar.set3("1", getPastVar, "-", "1")
    findVar.set3("H", findVar, "L", "H")
    findVar.set3("E", getPastVar, "-", "E")
    
    findSymbol(getPastVar, "_", "L", "-", findID)
    
    findID.set3("_", findID, "L", "_")
    findID.set3("1", getPastID, "-", "1")
    findID.set3("H", findID, "L", "H")
    findID.set3("E", getPastID, "-", "E")
    
    findSymbolW(getPastID, "_", "L", "R", "H", getPastTapeHead)
    
    findSymbol(getPastTapeHead, "H", "R", "R", getBackToFailedVar)
    
    findSymbol(getBackToFailedVar, "H", "R", "-", outState)
    
    return outState
    
# This function is very similar to the function markFunctionNames in writer.py,
# for obvious reasons.
def moveFunctionMarker(inState, listOfStates, name, outState=None):
    
    # inState might have been called getPastVariableNameState
    readSymbolReadState = State(name + "_read_symbol_read")
    checkForLineState = State(name + "_check_for_line")
    getPastLineNumberState = State(name + "_get_past_ln")
    checkForLineTypeState = State(name + "_check_for_line_type")
    checkForReactionState = State(name + "_check_for_reaction")
    getPastArgumentNameState = State(name + "_get_past_arg_name")
    checkForArgumentState = State(name + "_check_for_arg")
    returnToFailedFunctionState = State(name + "_return_failed_func")
    if outState == None:
        outState = State(name + "_out")

    listOfStates.extend([checkForReactionState, readSymbolReadState, checkForLineState, getPastLineNumberState, checkForLineTypeState, \
            inState, getPastArgumentNameState, checkForArgumentState, returnToFailedFunctionState])
    
    checkForReactionState.set3("_", checkForLineState, "R", "_")
    checkForReactionState.set3("1", readSymbolReadState, "R", "1")
    
    moveBy(readSymbolReadState, name + "_reading_basic_info", 3, "R", inState, listOfStates)
    # a goto looks like a variale name
    
    # This here's the whole point (the first one)! Getting that H in there.
    checkForLineState.set3("_", returnToFailedFunctionState, "L", "H")
    checkForLineState.set3("1", getPastLineNumberState, "R", "1")
    checkForLineState.set3("E", getPastLineNumberState, "R", "E")
	
    findSymbol(getPastLineNumberState, "_", "R", "R", checkForLineTypeState)
	
    checkForLineTypeState.set3("_", checkForReactionState, "R", "_")
    checkForLineTypeState.set3("1", inState, "-", "1")
    checkForLineTypeState.set3("E", getPastArgumentNameState, "-", "E")
	
    findSymbol(inState, "_", "R", "R", checkForReactionState)
	
    findSymbol(getPastArgumentNameState, "_", "R", "R", checkForArgumentState)
	
    checkForArgumentState.set3("_", checkForLineState, "R", "_")
    checkForArgumentState.set3("1", getPastArgumentNameState, "-", "1")
    checkForArgumentState.set3("E", getPastArgumentNameState, "-", "E")
    
    findSymbol(returnToFailedFunctionState, "H", "L", "-", outState)
    
    return outState
    
def moveLineMarker(inState, listOfStates, name, outState=None):
    # inState might have been called getPastLineNumberState
    
    checkForReactionState = State(name + "_check_for_reaction")
    readSymbolReadState = State(name + "_read_symbol_read")
    checkForLineTypeState = State(name + "_check_for_line_type")
    getPastVariableNameState = State(name + "_get_past_var_name")
    getPastArgumentNameState = State(name + "_get_past_arg_name")
    checkForArgumentState = State(name + "_check_for_arg")
    returnToFailedLineState = State(name + "_return_failed_line")
    if outState == None:
        outState = State(name + "_out")
    
    listOfStates.extend([inState, checkForReactionState, readSymbolReadState, checkForLineTypeState, 
        getPastVariableNameState, getPastArgumentNameState, checkForArgumentState, returnToFailedLineState])
    
    # This is the whole point!
    checkForReactionState.set3("_", returnToFailedLineState, "L", "H")
    checkForReactionState.set3("1", readSymbolReadState, "R", "1")
    
    moveBy(readSymbolReadState, name + "_reading_basic_info", 3, "R", getPastVariableNameState, 
        listOfStates)
    
    findSymbol(inState, "_", "R", "R", checkForLineTypeState)
    
    checkForLineTypeState.set3("_", checkForReactionState, "R", "_")
    checkForLineTypeState.set3("1", getPastVariableNameState, "-", "1")
    checkForLineTypeState.set3("E", getPastArgumentNameState, "-", "E")
    
    findSymbol(getPastVariableNameState, "_", "R", "R", checkForReactionState)
    
    findSymbol(getPastArgumentNameState, "_", "R", "R", checkForArgumentState)
    
    # This is the whole point!
    checkForArgumentState.set3("_", returnToFailedLineState, "L", "H")
    checkForArgumentState.set3("1", getPastArgumentNameState, "-", "1")
    checkForArgumentState.set3("E", getPastArgumentNameState, "-", "E")
    
    findSymbol(returnToFailedLineState, "H", "L", "-", outState)
    
    return outState
    
def rectifyNumber(inState, listOfStates, name, rectifySymbol, outState=None):
    # inState might have been called returnPrepState
    shiftSymbolState = State(name + "_shift_symbol")
    shift1State = State(name + "_shift_1")
    shiftEState = State(name + "_shift_E")
    if outState == None:
        outState = State(name + "_out")

    listOfStates.extend([inState, shiftSymbolState, shift1State, shiftEState])
	
    findSymbol(inState, "_", "L", "R", shiftSymbolState)	
	
    shiftSymbolState.set3("H", outState, "-", rectifySymbol)
    shiftSymbolState.set3("1", shift1State, "R", rectifySymbol)
    shiftSymbolState.set3("E", shiftEState, "R", rectifySymbol)
    
    shift1State.set3("H", outState, "-", "1")
    shift1State.set3("1", shift1State, "R", "1")
    shift1State.set3("E", shiftEState, "R", "1")
    
    shiftEState.set3("H", outState, "-", "E")
    shiftEState.set3("1", shift1State, "R", "E")
    shiftEState.set3("E", shiftEState, "R", "E")

    return outState

# for when you need to read this here symbol
def readHereSymbol(inState, listOfStates, name):
    # maps from symbol read to corresponding outState
    outStateDictionary = {"_": State(name + "_out__"), "1": State(name + "_out_1"),
        "E": State(name + "_out_E")}

    write1 = State(name + "_write_1")
    writeE = State(name + "_write_E")

    listOfStates.extend([inState, write1, writeE])
	
    # inState might have been called readSymbol
	
    inState.set3("1", write1, "L", "H")
    inState.set3("E", writeE, "L", "H")
    inState.set3("_", outStateDictionary["_"], "L", "_")
	
    write1.set3("H", outStateDictionary["1"], "R", "1")

    writeE.set3("H", outStateDictionary["E"], "R", "E")

    return outStateDictionary
    
# For when you don't have the benefit of extra space
def readHereSymbolCramped(inState, listOfStates, name, outStateDictionary=None):
    if outStateDictionary == None:
        outStateDictionary = {"_": State(name + "_out__"), "1": State(name + "_out_1"),
            "E": State(name + "_out_E")}
        
    inState.set3("_", outStateDictionary["_"], "L", "_")
    inState.set3("1", outStateDictionary["1"], "L", "H")
    inState.set3("E", outStateDictionary["E"], "L", "H")
    
    listOfStates.append(inState)
    
    return outStateDictionary

def readThereSymbol(inState, listOfStates, name, symbol, outStateDictionary=None):
    
    if outStateDictionary == None:
        outStateDictionary = {"failure": State(name + "_out_fail"), "continue": State(name + "_out_continue"), 
            "success": State(name + "_out_success")}

    # inState might have been called readSymbol
    
    listOfStates.append(inState)

    if symbol == "_":
        inState.set3("_", outStateDictionary["success"], "L", "_")
        inState.set3("1", outStateDictionary["failure"], "-", "1")
        inState.set3("E", outStateDictionary["failure"], "-", "E")

    else:
        writeSymbolState = State(name + "_write_symbol")

        listOfStates.append(writeSymbolState)
        
        for symbolRead in ["_", "1", "E"]:
            if symbolRead == symbol:
                inState.set3(symbolRead, writeSymbolState, "L", "H")
            else:
                inState.set3(symbolRead, outStateDictionary["failure"], "-", symbolRead)
            
        writeSymbolState.set3("H", outStateDictionary["continue"], "-", symbol)
        
    return outStateDictionary
    
def readThereSymbolCramped(inState, listOfStates, name, symbol, outStateDictionary=None):
    
    if outStateDictionary == None:
        outStateDictionary = {"failure__": State(name + "_out_fail__"), 
            "failure_1": State(name + "_out_fail_1"),
            "failure_E": State(name + "_out_fail_E"),
            "continue_1": State(name + "_out_continue_1"), 
            "continue_E": State(name + "_out_continue_E"), 
            "success": State(name + "_out_success")}

    # inState might have been called readSymbol
    
    listOfStates.append(inState)

    if symbol == "_":
        inState.set3("_", outStateDictionary["success"], "L", "_")
        inState.set3("1", outStateDictionary["failure__"], "-", "1")
        inState.set3("E", outStateDictionary["failure__"], "-", "E")

    else:
        writeSymbolState = State(name + "_write_symbol")

        listOfStates.append(writeSymbolState)
        
        for symbolRead in ["_", "1", "E"]:
            if symbolRead == symbol:
                inState.set3(symbolRead, writeSymbolState, "L", "H")
            else:
                inState.set3(symbolRead, outStateDictionary["failure_" + symbol], "-", symbolRead)
            
        writeSymbolState.set3("H", outStateDictionary["continue_" + symbol], "-", symbol)
        
    return outStateDictionary
                
def findMatchingValue(inState, listOfStates, name, travelThere, travelBack, moveMarker):
    
    # Assumes we're already in position to read the next symbol                
    # inState might have been readFunctionSymbol
    
    readHereSymbolDict = readHereSymbol(inState, listOfStates, name + "_read_here")
    
    readUnderscore = rectifyNumber(readHereSymbolDict["_"], listOfStates, name + "_finished_here", "H")
    
    gotPastH1 = State(name + "_got_past_H_1")
    gotPastHE = State(name + "_got_past_H_E")

    listOfStates.extend([readHereSymbolDict["1"], readHereSymbolDict["E"]])

    readHereSymbolDict["1"].set3("H", gotPastH1, "R", "H")
    readHereSymbolDict["E"].set3("H", gotPastHE, "R", "H")

    checkForUnderscore = travelThere(readUnderscore, listOfStates, name + "_remember__")
    checkFor1 = travelThere(gotPastH1, listOfStates, name + "_remember_1")
    checkForE = travelThere(gotPastHE, listOfStates, name + "_remember_E")
    
    readThereSymbolDict = {"failure": State(name + "_out_fail"), "continue": State(name + "_out_continue"), 
        "success": State(name + "_out_success")}
    
    readThereSymbol(checkForUnderscore, listOfStates, name + "_check__", "_", readThereSymbolDict)
    readThereSymbol(checkFor1, listOfStates, name + "_check_1", "1", readThereSymbolDict)
    readThereSymbol(checkForE, listOfStates, name + "_check_E", "E", readThereSymbolDict)
    
    # if the symbol matches, and we haven't succeeded yet
    travelBack(readThereSymbolDict["continue"], listOfStates, name + "_continue", "R", "H", inState)
    
    # if the symbol doesn't match, and we need to move onto the next possibility
    markerMoved = moveMarker(readThereSymbolDict["failure"], listOfStates, name + "_failure")
    
    doneFailing = rectifyNumber(markerMoved, listOfStates, name + "_remove_failed_H", "_")
    
    cameHomeInShame = travelBack(doneFailing, listOfStates, name + "_failed", "-")
    
    getBackToStartLineNumber = State(name + "_get_back_to_start_ln")
    
    rectifyNumber(cameHomeInShame, listOfStates, name + "_reset_aux_on_failure", "H", 
        getBackToStartLineNumber)
        
    listOfStates.append(getBackToStartLineNumber)
    
    findSymbol(getBackToStartLineNumber, "H", "L", "R", inState)
    # if the symbol matches, and it was the last one, we have succeeded

    successRectified = rectifyNumber(readThereSymbolDict["success"], listOfStates, 
        name + "_goodnumber_rectify", "H")

    gotPastHSuccess = State(name + "_got_past_H_success")

    findSymbol(successRectified, "H", "L", "L", gotPastHSuccess)

    listOfStates.append(successRectified)

    cameHomeVictorious = travelBack(gotPastHSuccess, listOfStates, name + "_succeeded")
    
    outState = rectifyNumber(cameHomeVictorious, listOfStates, name + "_victorious_rectify", "_")
    
    return outState
    
# Like findMatchingValue, but the template doesn't have room for an extra character; need 
# to remember the read character in both directions.
def findMatchingValueCrampedRtoL(inState, listOfStates, name, travelThere, travelThereCareful,
    travelBack, moveMarker):
    # Assumes we start in position to read the next symbol
    
    readHereSymbolDict = readHereSymbolCramped(inState, listOfStates, name + "_read_here")
        
    remember_ = State(name + "_remember__")    
        
    findSymbolW(readHereSymbolDict["_"], "_", "L", "L", "H", remember_)    
    
    listOfStates.append(readHereSymbolDict["_"])
        
    checkForUnderscore = travelThereCareful(remember_, listOfStates, name + "_remember__")
    checkFor1 = travelThere(readHereSymbolDict["1"], listOfStates, name + "_remember_1")
    checkForE = travelThere(readHereSymbolDict["E"], listOfStates, name + "_remember_E")

    readThereSymbolDict = {"failure__": State(name + "out_fail__"),
        "failure_1": State(name + "_out_fail_1"),
        "failure_E": State(name + "_out_fail__"),
        "continue_1": State(name + "_out_continue_1"),
        "continue_E": State(name + "_out_continue_E"),
        "success": State(name + "_out_success")}
        
    readThereSymbolCramped(checkForUnderscore, listOfStates, name + "_check__", "_", readThereSymbolDict)
    readThereSymbolCramped(checkFor1, listOfStates, name + "_check_1", "1", readThereSymbolDict)
    readThereSymbolCramped(checkForE, listOfStates, name + "_check_E", "E", readThereSymbolDict)
    
    #if the symbol matches, and we haven't succeeded yet
    
    gotPastH1 = State(name + "_got_past_H_1")
    gotPastHE = State(name + "_got_past_H_E")
    
    findSymbol(readThereSymbolDict["continue_1"], "H", "R", "R", gotPastH1)
    findSymbol(readThereSymbolDict["continue_E"], "H", "R", "R", gotPastHE)
    
    listOfStates.extend([readThereSymbolDict["continue_1"], readThereSymbolDict["continue_E"]])
    
    travelBack(gotPastH1, listOfStates, name + "_continue_1", "R", "1", inState)
    travelBack(gotPastHE, listOfStates, name + "_continue_E", "R", "E", inState)
    
    # if the symbol doesn't match, and we need to move onto the next possibility
    
    resetH = State(name + "_reset_H")
    listOfStates.append(resetH)
    
    # don't need to come home on a failed underscore--it's already taken care of.
    cameHomeInShame1 = travelBack(readThereSymbolDict["failure_1"], listOfStates, 
        name + "_failure_1", "-", "1", resetH)
    cameHomeInShameE = travelBack(readThereSymbolDict["failure_E"], listOfStates,
        name + "_failure_E", "-", "E", resetH)
    
    headBackAgain = State(name + "_head_back_again")
        
    findSymbolW(resetH, "_", "L", "L", "H", headBackAgain)
        
    # now we need to go back again to move the marker! jeez.
    travelThere(headBackAgain, listOfStates, name + "_time_to_move_on", "-", "H", 
        readThereSymbolDict["failure__"])
    
    markerMoved = moveMarker(readThereSymbolDict["failure__"], listOfStates, name + "_failure")
    
    doneFailing = rectifyNumber(markerMoved, listOfStates, name + "_remove_failed_H", "_")
    
    cameHomeInShameFinal = travelBack(doneFailing, listOfStates, name + "_failed", "R", "_", inState)
        
    # if the symbol matches, and it was the last one, we have succeeded
    
    successRectified = rectifyNumber(readThereSymbolDict["success"], listOfStates,
        name + "_goodnumber_rectify", "H")

    readTape = State(name + "_read_tape")
    read_ = State(name + "_read__")
    read1 = State(name + "_read_1")
    readE = State(name + "_read_E")

    findSymbol(successRectified, "H", "R", "R", readTape)
        
    readTape.set3("_", read_, "-", "_")
    readTape.set3("1", read1, "-", "1")
    readTape.set3("E", readE, "-", "E")
    
    listOfStates.extend([successRectified, readTape])
    
    outStateDict = {"_": State(name + "_out__"), "1": State(name + "_out_1"), 
        "E": State(name + "_out_E")}

    cameHome_ = travelBack(read_, listOfStates, name + "_came_home__", "-", "_")
    cameHome1 = travelBack(read1, listOfStates, name + "_came_home_1", "-", "_")
    cameHomeE = travelBack(readE, listOfStates, name + "_came_home_E", "-", "_")

    findSymbolW(cameHome_, "H", "R", "R", "_", outStateDict["_"])
    findSymbolW(cameHome1, "H", "R", "R", "_", outStateDict["1"])
    findSymbolW(cameHomeE, "H", "R", "R", "_", outStateDict["E"])
    
    listOfStates.extend([cameHome_, cameHome1, cameHomeE])

    return outStateDict    
    
def copyNumberRtoL(inState, listOfStates, name, travelThere, travelBack):
    # inState should have been called readSymbol
    write1 = State(name + "_write_1")
    writeE = State(name + "_write_E")
    remember1 = State(name + "_remember_1")
    rememberE = State(name + "_remember_E")
    rectify = State(name + "_rectify")
    writeH = State(name + "_write_H")
    symbolCopied = State(name + "_symbol_copied")
    outState = State(name + "_out")
    
    listOfStates.extend([inState, write1, writeE, writeH])
    
    inState.set3("_", rectify, "L", "_")
    inState.set3("1", write1, "L", "H")
    inState.set3("E", writeE, "L", "H")
    
    write1.set3("H", remember1, "-", "1")
    
    writeE.set3("H", rememberE, "-", "E")
    
    travelThere(remember1, listOfStates, name + "_remember_1", "R", "1", writeH)
    
    travelThere(rememberE, listOfStates, name + "_remember_E", "R", "E", writeH)
    
    writeH.set3("_", symbolCopied, "R", "H")
    
    travelBack(symbolCopied, listOfStates, name + "_symbol_copied", "R", "H", inState)
    
    getToEndNumber = rectifyNumber(rectify, listOfStates, name + "_done_copy", "1")
    
    findSymbolW(getToEndNumber, "_", "R", "L", "H", outState)
    listOfStates.append(getToEndNumber)
    
    return outState
    
def prepIndexDirect(inState, listOfStates, name):
    # inState might have been called findHState
    findE = State(name + "_find_E")
    findEndStack = State(name + "_find_end_stack")
    goLeft = State(name + "_go_left")
    findStartLastFunc = State(name + "_find_start_last_func")
    writeH = State(name + "_write_H")
    getToIndex = State(name + "_get_to_index")
    outState = State(name + "_out")
    
    listOfStates.extend([inState, findE, findEndStack, goLeft, findStartLastFunc, writeH,
        getToIndex])
    
    findSymbol(inState, "H", "L", "R", findE)
    
    findSymbol(findE, "E", "R", "-", findEndStack)
    
    findPattern(findEndStack, goLeft, listOfStates, name + "_find_end_stack",
        "___", "R", "L", "_")
    
    goLeft.set3("_", findStartLastFunc, "L", "_")
    
    findPattern(findStartLastFunc, writeH, listOfStates, name + "_find_start_last_func",
        "__", "L", "R", "_")
        
    writeH.set3("_", getToIndex, "L", "H")
    
    findSymbol(getToIndex, "H", "L", "L", outState)
    
    return outState
    
def indexIntoStack(inState, listOfStates, name, outState=None):
    # Assumes I start at the end of the index number
    # inState might have been called decrementState
    delete1 = State(name + "_delete_1")
    getPastH = State(name + "_get_past_H")
    findH = State(name + "_find_H")
    moveH = State(name + "_move_H")
    getToIndex = State(name + "_get_to_index")
    if outState == None:
        outState = State(name + "_out")
    
    listOfStates.extend([inState, delete1, getPastH, findH, moveH, getToIndex])

    inState.set3("_", delete1, "R", "_")
    inState.set3("1", getPastH, "-", "E")
    inState.set3("E", inState, "L", "1")
    
    delete1.set3("1", getPastH, "R", "_")
    delete1.set3("H", outState, "R", "_")
    
    findSymbol(getPastH, "H", "R", "R", findH)
    
    findSymbolW(findH, "H", "R", "R", "_", moveH)
    
    findSymbolW(moveH, "_", "R", "L", "H", getToIndex)
    
    findSymbol(getToIndex, "H", "L", "L", inState)
    
    return outState    

def prepFindVariable(inState, listOfStates, name):
    #inState should have been called findHHState
    findValue = State(name + "_find_value")
    getPastValue = State(name + "_get_past_value")
    findID = State(name + "_find_id")
    getPastID = State(name + "_get_past_id")
    getToAux = State(name + "_get_to_aux")
    getToVarName = State(name + "_get_to_var_name")
    outState = State(name + "_out")
    
    listOfStates.extend([inState, findValue, getPastValue, findID, getPastID, getToAux,
        getToVarName])
    
    findPattern(inState, findValue, listOfStates, "_get_to_vars", "HH", "L", "L", "H")
    
    findValue.set3("_", findValue, "L", "_")
    findValue.set3("1", getPastValue, "-", "1")
    findValue.set3("H", findValue, "L", "H")
    findValue.set3("E", getPastValue, "-", "E")
    
    findSymbol(getPastValue, "_", "L", "-", findID)
    
    findID.set3("_", findID, "L", "_")
    findID.set3("1", getPastID, "-", "1")
    findID.set3("H", findID, "L", "H")
    findID.set3("E", getPastID, "-", "E")
    
    findSymbolW(getPastID, "_", "L", "-", "H", getToAux)
    
    findPattern(getToAux, getToVarName, listOfStates, name + "_get_to_aux", "HH", "R", "R", "H")
    
    findSymbolW(getToVarName, "H", "R", "R", "_", outState)

    return outState
    
def findCorrespondingReaction(inState, listOfStates, name, symbol, outState=None):
    #inState should have been called moveRight
    readSymbol = State(name + "_read_symbol")
    undoH = State(name + "_undo_H")
    getPastBasicInfo = State(name + "_get_past_basic_info")
    getPastGoto = State(name + "_get_past_goto")
    if outState == None:
        outState = State(name + "_out")
    
    listOfStates.extend([inState, readSymbol, undoH, getPastBasicInfo, getPastGoto])
    
    inState.set3("1", readSymbol, "R", "H")
    
    for reactionSymbol in ["_", "1", "E"]:
        if symbol == reactionSymbol:
            readSymbol.set3(reactionSymbol, outState, "R", reactionSymbol)            
        else:
            readSymbol.set3(reactionSymbol, undoH, "L", reactionSymbol)
            
    undoH.set3("H", getPastBasicInfo, "R", "1")
    
    moveBy(getPastBasicInfo, name + "_get_past_info", 3, "R", getPastGoto, listOfStates)
    
    findSymbol(getPastGoto, "_", "R", "R", inState)
    
    return outState
    
def incrementLineNumber(inState, listOfStates, name, outState=None):
    # inState should have been called findHState
    removeHState1 = State(name + "_remove_H_1")
    incrementState = State(name + "_incr")
    removeHState2 = State(name + "_remove_H_2")
    if outState == None:
        outState = State(name + "_out")
    
    listOfStates.extend([inState, removeHState1, incrementState, removeHState2])
    
    findSymbolW(inState, "H", "L", "L", "1", removeHState1)
    
    findSymbol(removeHState1, "H", "L", "L", incrementState)
    
    incrementState.set3("_", removeHState2, "-", "E")
    incrementState.set3("1", incrementState, "L", "E")
    incrementState.set3("E", removeHState2, "-", "1")
    
    findSymbolW(removeHState2, "H", "R", "-", "_", outState)
    
    return outState

def copyGoto(inState, listOfStates, name, outState=None):
    # inState should have been called getPastH
    findLineNumber = State(name + "_find_ln")
    clear = State(name + "_clear")
    getPastH = State(name + "_get_past_H")
    goHome = State(name + "_go_home")
    getPastBasicInfo = State(name + "_get_past_basic_info")
    readSymbol = State(name + "_read_symbol")
    findLineNumber1 = State(name + "_find_ln_1")
    findLineNumberE = State(name + "_find_ln_E")
    write11 = State(name + "_write_1_1")
    writeE1 = State(name + "_write_E_1")
    write1E = State(name + "_write_1_E")
    writeEE = State(name + "_write_E_E")
    getPastH1 = State(name + "_get_past_H_1")
    getPastHE = State(name + "_get_past_H_E")
    goHome1 = State(name + "_go_home_1")
    goHomeE = State(name + "_go_home_E")
    removeH = State(name + "_remove_H")
    if outState == None:
        outState = State(name + "_out")
    
    listOfStates.extend([inState, findLineNumber, clear, getPastH, goHome, getPastBasicInfo,
        readSymbol, findLineNumber1, findLineNumberE, write11, writeE1, write1E, writeEE, 
        getPastH1, getPastHE, goHome1, goHomeE, removeH])
    
    findSymbol(inState, "H", "L", "L", findLineNumber)
    
    findSymbol(findLineNumber, "H", "L", "L", clear)
    
    clear.set3("_", getPastH, "-", "_")
    clear.set3("1", clear, "L", "_")
    clear.set3("E", clear, "L", "_")
    
    findSymbol(getPastH, "H", "R", "R", goHome)
    
    findSymbolW(goHome, "H", "R", "R", "1", getPastBasicInfo)
    
    moveBy(getPastBasicInfo, name + "_past_basic_info", 3, "R", readSymbol, listOfStates)
    
    readSymbol.set3("_", removeH, "-", "_")
    readSymbol.set3("1", findLineNumber1, "L", "H")
    readSymbol.set3("E", findLineNumberE, "L", "H")
    
    findSymbol(findLineNumber1, "H", "L", "L", write11)
    
    findSymbol(findLineNumberE, "H", "L", "L", writeEE)
    
    write11.set3("_", getPastH1, "-", "1")
    write11.set3("1", write11, "L", "1")
    write11.set3("E", writeE1, "L", "1")
    
    writeE1.set3("_", getPastH1, "-", "E")
    writeE1.set3("1", write11, "L", "E")
    writeE1.set3("E", writeE1, "L", "E")
    
    write1E.set3("_", getPastHE, "-", "1")
    write1E.set3("1", write1E, "L", "1")
    write1E.set3("E", writeEE, "L", "1")
    
    writeEE.set3("_", getPastHE, "-", "E")
    writeEE.set3("1", write1E, "L", "E")
    writeEE.set3("E", writeEE, "L", "E")    
    
    findSymbol(getPastH1, "H", "R", "R", goHome1)
    
    findSymbol(getPastHE, "H", "R", "R", goHomeE)
    
    findSymbolW(goHome1, "H", "R", "R", "1", readSymbol)
    
    findSymbolW(goHomeE, "H", "R", "R", "E", readSymbol)
    
    findSymbolW(removeH, "H", "L", "-", "_", outState)
    
    return outState
    
def dealWithTape(inStateDict, listOfStates, name):     
    
    # Rotation order is ["_", "1", "E"]
    readHeadMove = State(name + "_read_head_move")
    rotateForward = State(name + "_rotate_forward")
    rotateBackward = State(name + "_rotate_backward")
    writeForward = State(name + "_write_forward")
    writeBackward = State(name + "_write_backward")
    gotPastHBack = State(name + "_got_past_H_back")
    gotPastHForward = State(name + "_got_past_H_forward")
    getPastVar = State(name + "_get_past_var")
    homeForHeadMove = State(name + "_home_for_head_move")
    dontMoveHead = State(name + "_dont_move_head")
    moveHeadLeft = State(name + "_move_head_left")
    moveHeadRight = State(name + "_move_head_right")
    readSwappedSymbolL = State(name + "_read_swapped_symbol_L")
    readSwappedSymbolR = State(name + "_read_swapped_symbol_R")
    swap_ = State(name + "_swap__")
    swap1 = State(name + "_swap_1")
    swapE = State(name + "_swap_E")
    getHomeForGoto = State(name + "_get_home_for_goto")
    findLineNumber = State(name + "_find_ln")
    markEndLineNumber = State(name + "_mark_end_ln")
    getBackToReaction = State(name + "_get_back_to_reaction")
    getPastBasicInfo = State(name + "_get_past_basic_info")
    checkIfRealGoto = State(name + "_check_if_real_goto")
    outStateDict = {"incr": State(name + "_out_incr"), "goto": State(name + "_out_goto")}
    
    foundReaction_ = findCorrespondingReaction(inStateDict["_"], listOfStates, 
        name + "_find_reaction__", "_")
    foundReaction1 = findCorrespondingReaction(inStateDict["1"], listOfStates, 
        name + "_find_reaction_1", "1")
    foundReactionE = findCorrespondingReaction(inStateDict["E"], listOfStates, 
        name + "_find_reaction_E", "E")
 
    listOfStates.extend([foundReaction_, foundReaction1, foundReactionE, rotateBackward,
        rotateForward, readHeadMove, writeForward, writeBackward,
        getPastVar, homeForHeadMove,
        readSwappedSymbolL, readSwappedSymbolR, swap_, swap1, swapE, getHomeForGoto,
        findLineNumber, markEndLineNumber, getBackToReaction, getPastBasicInfo,
        checkIfRealGoto])
 
    foundReaction_.set3("_", readHeadMove, "R", "_")
    foundReaction_.set3("1", rotateForward, "-", "1")
    foundReaction_.set3("E", rotateBackward, "-", "E")
    
    foundReaction1.set3("_", rotateBackward, "-", "_")
    foundReaction1.set3("1", readHeadMove, "R", "1")
    foundReaction1.set3("E", rotateForward, "-", "E")
    
    foundReactionE.set3("_", rotateForward, "-", "_")
    foundReactionE.set3("1", rotateBackward, "-", "1")
    foundReactionE.set3("E", readHeadMove, "R", "E")
                 
    findSymbol(rotateBackward, "H", "L", "L", gotPastHBack)
    findSymbol(rotateForward, "H", "L", "L", gotPastHForward)
    
    gotToIDBack = travelAuxToVars(gotPastHBack, listOfStates, name + "_get_to_ID_back")
    gotToIDForward = travelAuxToVars(gotPastHForward, listOfStates, name + "_get_to_ID_forward")
    
    listOfStates.extend([gotToIDBack, gotToIDForward])
    
    findSymbol(gotToIDBack, "H", "R", "R", writeBackward)
    findSymbol(gotToIDForward, "H", "R", "R", writeForward)
        
    writeBackward.set3("_", getPastVar, "-", "E")
    writeBackward.set3("1", getPastVar, "-", "_")
    writeBackward.set3("E", getPastVar, "-", "1")
                 
    writeForward.set3("_", getPastVar, "-", "1")
    writeForward.set3("1", getPastVar, "-", "E")
    writeForward.set3("E", getPastVar, "-", "_")
    
    pushDown_, goHomeForHeadMove = pushDownTilHHH("_", listOfStates, name + "_")
    
    findSymbol(getPastVar, "_", "R", "R", pushDown_)
    
    findSymbol(goHomeForHeadMove, "H", "L", "R", homeForHeadMove)    
    
    listOfStates.append(goHomeForHeadMove)         
    
    moveBy(homeForHeadMove, name + "_get_to_write", 2, "R", readHeadMove, listOfStates)
    
    readHeadMove.set3("_", dontMoveHead, "-", "_")
    readHeadMove.set3("1", moveHeadLeft, "-", "1")
    readHeadMove.set3("E", moveHeadRight, "-", "E")
    
    travelAuxToVars(dontMoveHead, listOfStates, name + "_get_to_ID__", "-", "_", getHomeForGoto)
    gotToIDL = travelAuxToVars(moveHeadLeft, listOfStates, name + "_get_to_ID_L", "R", "_")
    gotToIDR = travelAuxToVars(moveHeadRight, listOfStates, name + "_get_to_ID_R", "R", "_")
    
    listOfStates.extend([gotToIDL, gotToIDR])
    
    findSymbol(gotToIDL, "H", "R", "L", readSwappedSymbolL)
    findSymbol(gotToIDR, "H", "R", "R", readSwappedSymbolR)
    
    readSwappedSymbolL.set3("_", swap_, "R", "H")
    readSwappedSymbolL.set3("1", swap1, "R", "H")
    readSwappedSymbolL.set3("E", swapE, "R", "H")

    readSwappedSymbolR.set3("_", swap_, "L", "H")
    readSwappedSymbolR.set3("1", swap1, "L", "H")
    readSwappedSymbolR.set3("E", swapE, "L", "H")
             
    swap_.set3("H", getHomeForGoto, "-", "_")             
    swap1.set3("H", getHomeForGoto, "-", "1")             
    swapE.set3("H", getHomeForGoto, "-", "E")                          
                 
    findPattern(getHomeForGoto, findLineNumber, listOfStates, name + "_find_ln", "HH",
        "R", "R", "H")
        
    findLineNumber.set3("_", findLineNumber, "R", "_")
    findLineNumber.set3("1", markEndLineNumber, '-', '1')
    findLineNumber.set3('E', markEndLineNumber, '-', 'E')
    
    findSymbolW(markEndLineNumber, '_', 'R', 'R', "H", getBackToReaction)
    
    findSymbolW(getBackToReaction, "H", "R", "R", "H", getPastBasicInfo)
    
    moveBy(getPastBasicInfo, name + "_get_past_basic_info", 3, "R", checkIfRealGoto, listOfStates)
    
    checkIfRealGoto.set3("_", outStateDict["incr"], "-", "_")
    checkIfRealGoto.set3("1", outStateDict["goto"], "-", "1")
    checkIfRealGoto.set3("E", outStateDict["goto"], "-", "E")
        
    return outStateDict    
    
def handleDirectCommand(inState, listOfStates, name, outState):
    copyVarNamePrepped = prepCopyVarName(inState, listOfStates, name + "_prep_copy_var")
    varNameCopied = copyNumberRtoL(copyVarNamePrepped, listOfStates, name + "_copy_var_name", simpleTravelLeft,
        simpleTravelRight)
    indexPrepped = prepIndexDirect(varNameCopied, listOfStates, name + "_prep_index")
    stackIndexed = indexIntoStack(indexPrepped, listOfStates, name + "_index_stack")
    findVarPrepped = prepFindVariable(stackIndexed, listOfStates, name + "_prep_find_var")
    readAndFoundVarDict = findMatchingValueCrampedRtoL(findVarPrepped, listOfStates, name + "_find_var",
        travelAuxToVars, travelAuxToVarsCareful, travelVarsToAux, moveVarMarker)
    dealWithLineNumberDict = dealWithTape(readAndFoundVarDict, listOfStates, name + "_deal_with_tape")
    doneWithLineNumber = State(name + "_dealt_with_ln")
    incrementLineNumber(dealWithLineNumberDict["incr"], listOfStates, name + "_incr_ln", outState)
    copyGoto(dealWithLineNumberDict["goto"], listOfStates, name + "_copy_goto", outState)
    
    return outState
    
# This one is cramped	
def copyFunctionName(inState, listOfStates, name):
    # inState should have been called readSymbolState
    copy1 = State(name + "_copy_1")
    copyE = State(name + "_copy_E")
    outState = State(name + "_out")
	
    listOfStates.extend([inState, copy1, copyE])
	
    inState.set3("_", outState, "R", "_")
    inState.set3("1", copy1, "L", "H")
    inState.set3("E", copyE, "L", "H")
	
    pushIn1, pushOut1 = pushDownTilHHH("H", listOfStates, name + "_copy_1")
    pushInE, pushOutE = pushDownTilHHH("H", listOfStates, name + "_copy_E")
	
    listOfStates.extend([pushOut1, pushOutE])
	
    findSymbolW(copy1, "H", "L", "R", "1", pushIn1)
    findSymbolW(copyE, "H", "L", "R", "E", pushInE)
	
    findSymbolW(pushOut1, "H", "L", "R", "1", inState)
    findSymbolW(pushOutE, "H", "L", "R", "E", inState)
	
    return outState
    
# This one is cramped	
def copyArg(inState, listOfStates, name):
    # inState should have been called readSymbolState
    copy1 = State(name + "_copy_1")
    copyE = State(name + "_copy_E")
    gotPastH1 = State(name + "_got_past_H_1")
    gotPastHE = State(name + "_got_past_H_E")
    gotPastOtherH1 = State(name + "_got_past_other_H_1")
    gotPastOtherHE = State(name + "_got_past_other_H_E")
    outState = State(name + "_out")
	
    listOfStates.extend([inState, copy1, copyE, gotPastH1, gotPastHE, gotPastOtherH1, gotPastOtherHE])
	
    inState.set3("_", outState, "-", "_")
    inState.set3("1", copy1, "R", "H")
    inState.set3("E", copyE, "R", "H")
	
    pushIn1, pushOut1 = pushDownTilHHH("H", listOfStates, name + "_copy_1")
    pushInE, pushOutE = pushDownTilHHH("H", listOfStates, name + "_copy_E")
	
    listOfStates.extend([pushOut1, pushOutE])
	
    findSymbolW(copy1, "H", "R", "R", "1", pushIn1)
    findSymbolW(copyE, "H", "R", "R", "E", pushInE)
	
    findSymbol(pushOut1, "H", "L", "L", gotPastH1)
    findSymbol(pushOutE, "H", "L", "L", gotPastHE)
    
    findSymbol(gotPastH1, "H", "L", "L", gotPastOtherH1)
    findSymbol(gotPastHE, "H", "L", "L", gotPastOtherHE)
    
    findSymbolW(gotPastOtherH1, "H", "L", "R", "1", inState)
    findSymbolW(gotPastOtherHE, "H", "L", "R", "E", inState)
	
    return outState    
	
# This one is also cramped but at least not doubly so
def copyArgIndex(inState, listOfStates, name):
	# inState should have been called readSymbolState
    getPastHL1 = State(name + "_get_past_H_L_1")
    getPastHLE = State(name + "_get_past_H_L_E")
    copy1 = State(name + "_copy_1")
    copyE = State(name + "_copy_E")
    writeH1 = State(name + "_write_H_1")
    writeHE = State(name + "_write_H_E")
    getPastHR1 = State(name + "_get_past_H_R_1")
    getPastHRE = State(name + "_get_past_H_R_E")
    getHome1 = State(name + "_get_home_1")
    getHomeE = State(name + "_get_home_E")
    outState = State(name + "_out")
	    
    listOfStates.extend([inState, getPastHL1, getPastHLE, copy1, copyE, writeH1, writeHE, getPastHR1, getPastHRE,
        getHome1, getHomeE])
	
    inState.set3("_", outState, "L", "H")
    inState.set3("1", getPastHL1, "L", "H")
    inState.set3("E", getPastHLE, "L", "H")
	
    findSymbol(getPastHL1, "H", "L", "L", copy1)
    findSymbol(getPastHLE, "H", "L", "L", copyE)
	
    findSymbolW(copy1, "H", "L", "R", "1", writeH1)
    findSymbolW(copyE, "H", "L", "R", "E", writeHE)
	
    writeH1.set3("_", getPastHR1, "R", "H")
    writeHE.set3("_", getPastHRE, "R", "H")

    findSymbol(getPastHR1, "H", "R", "R", getHome1)
    findSymbol(getPastHRE, "H", "R", "R", getHomeE)
	
    findSymbolW(getHome1, "H", "R", "R", "1", inState)
    findSymbolW(getHomeE, "H", "R", "R", "E", inState)	
	
    return outState
	
def prepIndex(inState, listOfStates, name):
    # inState should have been called findEndStack
    getPastH = State(name + "_get_past_H")
    getPastUnderscores = State(name + "_get_past_underscores")
    findStartLastFunc = State(name + "_find_start_last_func")
    writeH = State(name + "_write_H")
    findIndex = State(name + "_find_index")
    outState = State(name + "_out")
    
    listOfStates.extend([inState, getPastH, getPastUnderscores, findStartLastFunc, writeH, findIndex])
    
    pushIn, pushOut = pushDownTilHHH("H", listOfStates, name + "_push_tack_on_underscore")
    
    # This is where I add on the hanging underscore. It's sort of arbitrary, but this was the most convenient spot
    findSymbolW(inState, "H", "L", "R", "_", pushIn)
    
    findSymbol(pushOut, "H", "L", "L", getPastH)
    listOfStates.append(pushOut)
    
    findSymbol(getPastH, "H", "L", "L", getPastUnderscores)
    
    findPattern(getPastUnderscores, findStartLastFunc, listOfStates, name + "_get_past_underscores", "__", "L", "L", "_")
    
    findPattern(findStartLastFunc, writeH, listOfStates, name + "_mark_last_func", "__", "L", "R", "_")
    
    writeH.set3("_", findIndex, "L", "H")
    
    findSymbol(findIndex, "H", "L", "L", outState)
    
    return outState
    
def prepCopyArg(inState, listOfStates, name):
    # inState might have been called findH
    outState = State(name + "_out")
    
    listOfStates.append(inState)
    
    findSymbolW(inState, "H", "R", "R", "_", outState)
    
    return outState
    
def prepCopyIndex(inState, listOfStates, name, otherArgOutState):
    # inState might have been called findH
    findLineNumber = State(name + "_find_ln")
    getPastLineNumber = State(name + "_get_past_ln")
    writeH = State(name + "_write_H")
    getPastH = State(name + "_get_past_H")
    findArg = State(name + "_find_arg")
    checkForOtherArg = State(name + "_check_for_other_arg")
    doneOutState = State(name + "_done_out")
    
    listOfStates.extend([inState, findLineNumber, getPastLineNumber, writeH, getPastH, findArg, checkForOtherArg])
    
    findSymbol(inState, "H", "L", "R", findLineNumber)
    
    findLineNumber.set3("_", findLineNumber, "R", "_")
    findLineNumber.set3("1", getPastLineNumber, "-", "1")
    findLineNumber.set3("E", getPastLineNumber, "-", "E")
    
    findSymbol(getPastLineNumber, "_", "R", "R", writeH)
    
    writeH.set3("_", getPastH, "R", "H")
    
    findSymbol(getPastH, "H", "R", "R", findArg)
    
    findSymbolW(findArg, "H", "R", "R", "_", checkForOtherArg)
    
    checkForOtherArg.set3("_", doneOutState, "-", "_")
    checkForOtherArg.set3("1", otherArgOutState, "-", "1")
    checkForOtherArg.set3("E", otherArgOutState, "-", "E")
    
    return doneOutState
    
def copyFunctionArgs(inState, listOfStates, name):
    # inState should have been called readSymbolState
    indexCopied = copyArgIndex(inState, listOfStates, name + "_copy_index")
    indexPrepped = prepIndex(indexCopied, listOfStates, name + "_prep_index")
    stackIndexed = indexIntoStack(indexPrepped, listOfStates, name + "_index_into_stack")
    copyArgPrepped = prepCopyArg(stackIndexed, listOfStates, name + "_prep_copy_arg")
    argCopied = copyArg(copyArgPrepped, listOfStates, name + "_copy_arg")
    copyingDone = prepCopyIndex(argCopied, listOfStates, name + "_prep_copy_index", inState)
    
    return copyingDone
	
def prepCopyLineNumber(inState, listOfStates, name):
    # inState should have been called getPastH
    removeH = State(name + "_remove_H")
    findLineNumber = State(name + "_find_ln")
    markLineNumber = State(name + "_mark_ln")
    outState = State(name + "_out")
    
    listOfStates.extend([inState, removeH, findLineNumber, markLineNumber])
    
    findSymbol(inState, "H", "L", "L", removeH)
    
    findSymbolW(removeH, "H", "L", "-", "_", findLineNumber)    
    
    findLineNumber.set3("_", findLineNumber, "L", "_")
    findLineNumber.set3("1", markLineNumber, "-", "1")
    findLineNumber.set3("E", markLineNumber, "-", "E")
    
    findSymbolW(markLineNumber, "_", "L", "-", "H", outState)
    
    return outState
    
def copyLineNumber(inState, listOfStates, name, outState):
    # inState should have been called readSymbol
    swap1 = State(name + "_swap_1")
    swapE = State(name + "_swap_E")
    getPastH1 = State(name + "_get_past_H_1")
    getPastHE = State(name + "_get_past_H_E")
    copy_ = State(name + "_copy__")
    copy1 = State(name + "_copy_1")
    copyE = State(name + "_copy_E")
    getHome = State(name + "_get_home")
    writeE = State(name + "_write_E")
    clear = State(name + "_clear")
    getPastLineNumber = State(name + "_get_past_ln")
    if outState == None:
        outState = State(name + "_out")
    
    listOfStates.extend([inState, swap1, swapE, getPastH1, getPastHE, copy_, copy1, copyE, getHome, writeE, clear,
        getPastLineNumber])
    
    inState.set3("_", writeE, "L", "_")
    inState.set3("1", swap1, "L", "H")
    inState.set3("H", copy_, "R", "H") # one weird trick to sneak that extra underscore in
    inState.set3("E", swapE, "L", "H")
    
    swap1.set3("H", getPastH1, "R", "1")
    swapE.set3("H", getPastHE, "R", "E")
    
    getPastH1.set3("H", copy1, "R", "H")
    getPastHE.set3("H", copyE, "R", "H")
    
    pushIn, pushOut = pushDownTilHHH("H", listOfStates, name + "_push")
    
    listOfStates.append(pushOut)
    
    findSymbolW(copy_, "H", "R", "R", "_", pushIn)
    findSymbolW(copy1, "H", "R", "R", "1", pushIn)    
    findSymbolW(copyE, "H", "R", "R", "E", pushIn)
    
    findSymbol(pushOut, "H", "L", "L", getHome)
    
    findSymbol(getHome, "H", "L", "R", inState)
    
    writeE.set3("H", clear, "L", "E")
    
    clear.set3("_", getPastLineNumber, "-", "_")
    clear.set3("1", clear, "L", "_")
    clear.set3("E", clear, "L", "_")
    
    findSymbol(getPastLineNumber, "E", "R", "R", outState)
    
    return outState
    
def handleFunctionCall(inState, listOfStates, name, outState):
    functionCallCopied = copyFunctionName(inState, listOfStates, name + "_copy_func_name")
    functionArgsCopied = copyFunctionArgs(functionCallCopied, listOfStates, name + "_copy_func_args")
    copyLineNumberPrepped = prepCopyLineNumber(functionArgsCopied, listOfStates, name + "_prep_copy_ln")
    lineNumberCopied = copyLineNumber(copyLineNumberPrepped, listOfStates, name + "_copy_ln", outState)
  
def prepCopyReturnAddress(inState, listOfStates, name):
    # inState might have been called findEndStackState
    findReturnAddress = State(name + "_find_return_address")
    getToStartReturnAddress = State(name + "_get_to_start_return_address")
    removeH = State(name + "_remove_H")
    writeH = State(name + "_write_H")
    clear = State(name + "_clear")
    getPastH = State(name + "_get_past_H")
    getToReturnAddress = State(name + "_get_to_return_address")
    outState = State(name + "_out")
    
    listOfStates.extend([inState, findReturnAddress, getToStartReturnAddress, removeH, writeH, clear, getPastH,
        getToReturnAddress])
    
    findSymbolW(inState, "H", "L", "L", "_", findReturnAddress)
    
    findReturnAddress.set3("_", findReturnAddress, "L", "_")
    findReturnAddress.set3("1", getToStartReturnAddress, "-", "1")
    findReturnAddress.set3("E", getToStartReturnAddress, "-", "E")
  
    findSymbolW(getToStartReturnAddress, "_", "L", "L", "H", removeH)
    
    findSymbolW(removeH, "H", "L", "L", "_", writeH)
    
    writeH.set3("_", clear, "L", "H")
    
    clear.set3("_", getPastH, "-", "_")
    clear.set3("1", clear, "L", "_")
    clear.set3("E", clear, "L", "_")
    
    findSymbol(getPastH, "H", "R", "R", getToReturnAddress)
    
    findSymbolW(getToReturnAddress, "H", "R", "R", "_", outState)
  
    return outState  
  
def copyReturnAddress(inState, listOfStates, name):
    # inState should have been called readSymbolState
    getToLineNumber1 = State(name + "_get_to_ln_1")
    getToLineNumberE = State(name + "_get_to_ln_E")
    write11 = State(name + "_write_1_1")
    writeE1 = State(name + "_write_E_1")
    write1E = State(name + "_write_1_E")
    writeEE = State(name + "_write_E_E")
    getPastH1 = State(name + "_get_past_H_1")
    getPastHE = State(name + "_get_past_H_E")
    getHome1 = State(name + "_get_home_1")
    getHomeE = State(name + "_get_home_E")
    outState = State(name + "_out")
    
    listOfStates.extend([inState, getToLineNumber1, getToLineNumberE, write11, writeE1, write1E, writeEE, getPastH1, 
        getPastHE, getHome1, getHomeE])
    
    inState.set3("_", outState, "-", "_")
    inState.set3("1", getToLineNumber1, "L", "H")
    inState.set3("E", getToLineNumberE, "L", "H")
    
    findSymbol(getToLineNumber1, "H", "L", "L", write11)
    findSymbol(getToLineNumberE, "H", "L", "L", writeEE)
    
    write11.set3("_", getPastH1, "-", "1")
    write11.set3("1", write11, "L", "1")
    write11.set3("E", writeE1, "L", "1")
    
    writeE1.set3("_", getPastH1, "-", "E")
    writeE1.set3("1", write11, "L", "E")
    writeE1.set3("E", writeE1, "L", "E")

    write1E.set3("_", getPastHE, "-", "1")
    write1E.set3("1", write1E, "L", "1")
    write1E.set3("E", writeEE, "L", "1")
    
    writeEE.set3("_", getPastHE, "-", "E")
    writeEE.set3("1", write1E, "L", "E")
    writeEE.set3("E", writeEE, "L", "E")
    
    findSymbol(getPastH1, "H", "R", "R", getHome1)
    findSymbol(getPastHE, "H", "R", "R", getHomeE)
    
    findSymbolW(getHome1, "H", "R", "R", "1", inState)
    findSymbolW(getHomeE, "H", "R", "R", "E", inState)
    
    return outState
    
def popTopFunction(inState, listOfStates, name, outState):
    # inState might have been clear
    seenUnderscore = State(name + "_seen_underscore")
    checkIfStackEmpty = State(name + "_check_if_stack_empty")
    removeH = State(name + "_remove_H")
    incrementState = State(name + "_increment")
    getPastReturnAddressState = State(name + "_get_past_return_address")
    
    listOfStates.extend([inState, seenUnderscore, checkIfStackEmpty, removeH, incrementState, getPastReturnAddressState])
    
    inState.set3("_", seenUnderscore, "L", "_")
    inState.set3("1", inState, "L", "_")
    inState.set3("E", inState, "L", "_")
    
    seenUnderscore.set3("_", checkIfStackEmpty, "L", "_")
    seenUnderscore.set3("1", inState, "L", "_")
    seenUnderscore.set3("E", inState, "L", "_")
    
    # This is the only place that the Turing machine can halt without errors!
    checkIfStackEmpty.set3("_", SimpleState("HALT"), "-", "_")
    checkIfStackEmpty.set3("1", removeH, "R", "1")
    checkIfStackEmpty.set3("E", removeH, "R", "E")
    
    findSymbolW(removeH, "H", "L", "L", "_", incrementState)
    
    # need to increment return address
    incrementState.set3("_", getPastReturnAddressState, "-", "E")
    incrementState.set3("1", incrementState, "L", "E")
    incrementState.set3("E", getPastReturnAddressState, "-", "1")
    
    findSymbol(getPastReturnAddressState, "_", "R", "R", outState)
    
    return outState
    
def handleReturn(inState, listOfStates, name, outState):
    # I NEED TO ADD ON AUTOMATIC GOING HOME!
    
    returnAddressCopyPrepped = prepCopyReturnAddress(inState, listOfStates, name + "_prep_copy_return_address")
    returnAddressCopied = copyReturnAddress(returnAddressCopyPrepped, listOfStates, name + "_copy_return_address")
    popTopFunction(returnAddressCopied, listOfStates, name + "_pop_top_func", outState)
    
    
def processCentrally(inState, listOfStates):
    functionPrepped = commonPrepTopFunction(inState, listOfStates, "cpu_prep_top_func")
    functionMatched = findMatchingValue(functionPrepped, listOfStates, "cpu_match_top_func", 
        simpleTravelRight, simpleTravelLeft, moveFunctionMarker)
    linePrepped = prepLine(functionMatched, listOfStates, "cpu_prep_line")
    lineMatched = findMatchingValue(linePrepped, listOfStates, "cpu_match_line", simpleTravelRight, \
        simpleTravelLeft, moveLineMarker)        
    lineTypeDict = readLineType(lineMatched, listOfStates, "cpu_read_line_type")
    
    doneProcessingLine = State("cpu_done_processing_line")
    doneProcessingLineReturn = State("cpu_done_processing_line_return")
    
    handleDirectCommand(lineTypeDict["direct"], listOfStates, "cpu_direct_command", doneProcessingLine)
    handleFunctionCall(lineTypeDict["function"], listOfStates, "cpu_function_call", doneProcessingLine)  
    handleReturn(lineTypeDict["return"], listOfStates, "cpu_return", doneProcessingLine)  
    
    # This separation is no longer necessary
    standardPrepTopFunctionExceptReturn(doneProcessingLine, listOfStates, "cpu_standard_prep_not_return", 
        doneProcessingLineReturn)
    standardPrepTopFunction(doneProcessingLineReturn, listOfStates, "cpu_standard_prep", inState)
		
#    print [state.stateName for state in listOfStates]
    
#    listOfStates.append(inState)
#    inState.setAllNextStates(SimpleState("ACCEPT"))
    
    return inState
#    listOfStates.append(readAndFoundVar)
#    findVarPrepped.setAllNextStates(SimpleState("ACCEPT"))

