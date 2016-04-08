import string
import re
import os
from writer import *
from tmsim import *

# Interprets a TMD program on the fly. Prints out the behaviors of the
# different tapes as it goes.

# Use this to debug your handwritten TMD program before compiling it
# to a Turing machine!

def pront(x):
    print x

class TuringMachineWithStack:
    def __init__(self, functions, path, functionLabelDictionary, functionLineDictionary, functionVariableDictionary, lineNumberToTextNumber, initVarString):
		
        mainFunctionName = string.strip(functions[0])
		
        self.stack = [(mainFunctionName, functionVariableDictionary[mainFunctionName], 1)]
        self.lineNumber = 1
		
        self.path = path
        self.functions = functions
        self.functionLabelDictionary = functionLabelDictionary
        self.functionLineDictionary = functionLineDictionary
        self.functionVariableDictionary = functionVariableDictionary
        self.lineNumberToTextNumber = lineNumberToTextNumber
		
        self.tapeDictionary = {}
        
        firstLineOfMainFunction = open(path + string.strip(functions[0]) + ".tmd", "r").readlines()[0]
        
        for i, varName in enumerate(string.split(firstLineOfMainFunction)[1:]):
            tape = Tape(varName, "_")
            
            self.tapeDictionary[i+1] = tape
            
            for j, symbol in enumerate(initVarString):
                self.tapeDictionary[i+1].tapeDict[j] = symbol
    
    # Returns 1 upon halting, 0 otherwise    
    def runOneStep(self):
                
        currentFunction = self.stack[-1][0]
        currentLine = self.functionLineDictionary[currentFunction][self.lineNumber]
        
        # get rid of labels
        currentLine = string.split(currentLine, ":")[-1]
        
        if "[" in currentLine:
            # direct command
            splitLine = re.split("[\[|\]]", currentLine)
			
            variableName = splitLine[1]
            reactions = string.split(splitLine[2], ";")
            
            foundAppropriateReaction = False
            
            tapeName = self.stack[-1][1][variableName]
            
            currentTape = self.tapeDictionary[tapeName]
            currentSymbol = currentTape.readSymbol()
                                    
            for reaction in reactions:
                                
                # ugly stuff at the end of next line is for removing whitespce
                splitReaction = re.split("[(|)|,]", string.strip(reaction).replace(" ", ""))
                if splitReaction[0] == currentSymbol:
                    foundAppropriateReaction = True
                
                    for command in splitReaction[1:]:
                        if command in ["1", "E", "_"]:
                            currentTape.writeSymbol(command)
                    
                    for command in splitReaction[1:]:
                        if command in ["L", "R", "-"]:
                            currentTape.moveHead(command)
                    
                    foundGoto = False
                    for command in splitReaction[1:]:
                        if not command in ["1", "E", "_", "L", "R", "-", ""]:
                            try:                                
                                self.lineNumber = self.functionLabelDictionary[currentFunction][command]
                                foundGoto = True
                            except:
                                raise Exception("Unrecognized label on line " + str(self.lineNumberToTextNumber[self.lineNumber]) + " of function " + currentFunction)
                            
                    
                    if not foundGoto:
                        self.lineNumber += 1
                    
            if not foundAppropriateReaction:
                raise Exception("Turing machine threw error on line " + str(self.lineNumberToTextNumber[self.lineNumber]) + " of function " +  currentFunction)
                return 1
        
        elif string.split(currentLine)[0] == "function":
            
            oldMappingDict = self.stack[-1][1]
            
            calledFunction = string.split(currentLine)[1]
            firstLineOfCalledFunctionSplit = string.split(open(self.path + calledFunction + ".tmd", "r").readlines()[0])
            
            argList = string.split(currentLine)[2:]
            
            try:
                assert len(firstLineOfCalledFunctionSplit[1:]) == len(argList)
            except:
                raise Exception("Function call on line " + str(self.lineNumberToTextNumber[self.lineNumber]) + " of function " + currentFunction + " has " + str(len(argList)) + \
                    " arguments, but the function being called has " + str(len(firstLineOfCalledFunctionSplit[1:])) + " inputs.")
            
            newMappingDict = {}
            
            for i, variableName in enumerate(firstLineOfCalledFunctionSplit[1:]):
                newMappingDict[variableName] = oldMappingDict[argList[i]]
            
            self.stack.append((calledFunction, newMappingDict, self.lineNumber + 1))
            self.lineNumber = 1
            
        elif string.split(currentLine)[0] == "return":
            
            oldLineNumber = self.lineNumber
            
            self.lineNumber = self.stack[-1][2]
            self.stack.pop()
            
            if len(self.stack) == 0:
                pront("Turing machine halted on line " + str(self.lineNumberToTextNumber[oldLineNumber]) + " of function " + currentFunction)
                return 1
            
        else:
            raise Exception("Line " + str(self.lineNumberToTextNumber[self.lineNumber]) + " of function " + currentFunction + " is malformed.")
            
        return 0
                        

    def run(self, quiet=False, numSteps=float("Inf"), outputFile=None):
        stepCounter = 0        
        
        while self.runOneStep() == 0:
            stepCounter += 1
            if stepCounter >= numSteps:
                pront("Turing machine ran for " + str(numSteps) + " steps without halting.")
                break
            
            if not quiet:                    
                self.printAllTapes(-2, 160, outputFile)
        
    def printAllTapes(self, start, end, output):
        
        outString = "Function: " + self.stack[-1][0] + "\n"
        outString += "Line number: " + str(self.lineNumberToTextNumber[self.lineNumber]) + "\n"
        outString += "\n"
        
        for tape in self.tapeDictionary.values():
            outString += tape.getTapeOutput(start, end)
            
        outString += "\n"
        outString += "Stack:\n"
        outString += "\n"
        
        for tupIndex in range(len(self.stack) - 1, -1, -1):
            outString += "Function " + self.stack[tupIndex][0] + " with return address " + \
                str(self.lineNumberToTextNumber[self.stack[tupIndex][2]]) + " and with mapping " + str(self.stack[tupIndex][1]) + "\n"
        
        outString += "\n"
        outString += "---------------------------------------"
        
        if output == None:
            pront(outString)

        else:
            output.write(outString + "\n")
    
def main():    
    dirName = sys.argv[-1]
    
    path = "../tmd_dirs/" + dirName + "/"

    try:
        assert len(sys.argv) > 1
        for flag in sys.argv[2:-1]:
            if not (flag in ["-q", "-s", "-f"]):
                int(flag)
        
    except:
        raise Exception("Usage: python tmd_interpreter [-q] [-s] [# steps before aborting] [-f] [name of TMD directory]\n \
            Enable -q if you want no program output\n \
            Enable -s followed by the max number of steps if you want to stop interpreting after a certain number of commands\n \
            Enable -f if you want to dump the history into a file in tmd_histories instead of the standard output.")

    try:
        assert os.path.exists(path)
    except:
        raise Exception("Directory " + path + " does not exist.")

    try:
        functions = [string.strip(x) for x in open(path + "functions", "r").readlines()]
    except:  
        raise Exception("No functions file found in directory " + path) 

    functionLabelDictionary, functionDictionary, functionLineDictionary, lineNumberToTextNumber = getFunctionLabelDictionary(functions, path)
    functionVariableDictionary = getFunctionVariableDictionary(functions, path)

    try:
        initVarString = string.strip(open(path + "initvar", "r").read())
    except:
        raise Exception("No initvar file found in directory " + path)
    
    if "-q" in sys.argv:
        quiet = True
    else:
        quiet = False
            
    if "-s" in sys.argv:
        numSteps = int(sys.argv[sys.argv.index("-s") + 1])
    else:
        numSteps = float("inf")
    
    HISTORY_PATH = "../tmd_histories/"
    
    if "-f" in sys.argv:
        outputFile = open(HISTORY_PATH + dirName + "_tmd_history.txt", "w")
        outputFile.write("\n")
        
        try:
            assert "-s" in sys.argv
        except:
            raise Exception("You can't include the -f flag without also specifying a maximum step count with the -s flag!")
        
    else:
        outputFile = None
    
    TuringMachineWithStack(functions, path, functionLabelDictionary, functionLineDictionary, 
        functionVariableDictionary, lineNumberToTextNumber, initVarString).run(quiet, numSteps, outputFile)
    
    
if __name__ == "__main__":
    main()