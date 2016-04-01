import string
import os
import sys

def pront(x):
    print x

def incrDict(elt, dic):
    if elt in dic:
        dic[elt] += 1
    else:
        dic[elt] = 1

functionsTFF = "main\n"
alreadyOpened = []

LIBRARY_LOCATION = "../../tmd/laconic_std_library/"

# Tracks how many times we see each function; we want frequently-seen functions to be at the top of functions.tff,
# so that they have shorter names in the binary
functionCount = {}

# automatically moves all the right functions to the target directory
def importFuncs(targetDir, func="main"):

    global alreadyOpened
    global functionsTFF

    print func

#    functionsTFF += func + "\n"
    
    alreadyOpened.append(func)
    
    if os.path.exists(func + ".tmd"):
        currentFile = open(func + ".tmd", "r").readlines()
                                
        for line in currentFile:
            lineSplit = string.split(line, ":")
            command = lineSplit[-1]
            commandSplit = string.split(command)
            if commandSplit != [] and commandSplit[0] == "function":
                functionName = commandSplit[1]
                incrDict(functionName, functionCount)
                
                if not functionName in alreadyOpened:
                    importFuncs(targetDir, functionName)
                
        os.system("mv " + func + ".tmd " + targetDir)
            
    elif os.path.exists(LIBRARY_LOCATION + func + ".tmd"):
        currentFile = open(LIBRARY_LOCATION + func + ".tmd", "r").readlines()

        for line in currentFile:
            lineSplit = string.split(line, ":")
            command = lineSplit[-1]
            commandSplit = string.split(command)
            if commandSplit != [] and commandSplit[0] == "function":
                functionName = commandSplit[1]
                incrDict(functionName, functionCount)
                
                if not functionName in alreadyOpened:
                    importFuncs(targetDir, functionName)
                
        os.system("cp " + LIBRARY_LOCATION + func + ".tmd " + targetDir)
        
    else:
        pront("Error: dependency file " + func + ".tmd does not exist.")
        raise
        
importFuncs(sys.argv[1])

functionCountItems = sorted(functionCount.items(), key=lambda x:x[1]) # sort by number of times seen
functionCountItems.reverse()
functionCountKeys = [i[0] for i in functionCountItems]

#print functionCountKeys
        
for func in functionCountKeys:
    if not func == "main":
        functionsTFF += func + "\n"   

open(sys.argv[1] + "/functions", "w").write(functionsTFF)
open(sys.argv[1] + "/initvar", "w").write("E\n")