import sys
import string
import math
import os
from writer import *
from cpu import *

# Transforms a TMD directory in your tmd_dirs directory
# (parsimony/src/tmd/tmd_dirs/)
# into a single-tape, 4-symbol Turing machine in your tm4_files directory
# (parsimony/src/tm/tm4/tm4_files)
# whose behavior is the same.

# Before compiling your TMD directory, if you wrote it by hand,
# it is highly recommended that you debug it using tmd_interpreter.py!

# NOTE: this compiler does not use introspection and as such is likely 
# to use many more states than necessary. For demonstrating the parsimony
# of something, convert to a 2-symbol TM instead, with 
# tmd_to_2s_tm_compiler.py!
   
def main():
    try:
        assert len(sys.argv) == 2
    except:
        raise Exception("Usage: python tmd_to_4s_tm_compiler.py [name of TMD directory]")
    
    dirName = sys.argv[1]
    
    path = "../tmd_dirs/" + dirName + "/"

    try:
        assert os.path.exists(path)
    except:
        raise Exception("Directory " + path + " not found.")

    try:
        functions = [string.strip(x) for x in open(path + "functions", "r").readlines()]
    except:  
        raise Exception("No functions file found in directory " + path) 

    functionLabelDictionary, functionDictionary, _, _ = getFunctionLabelDictionary(functions, path)
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
    
    inState = write(listOfStates, inState, numberOfVariables, initValueString, numberOfFunctions, \
        functions, functionVariableDictionary, functionLabelDictionary, functionDictionary, path)
    inState = processCentrally(inState, listOfStates)
    
    convertStatesToString(listOfStates, open("../../tm/tm4/tm4_files/" + dirName + ".tm4", "w"))
    
if __name__ == "__main__":    
    main()
 
