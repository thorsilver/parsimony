import sys
import tmsim

# A script for converting my standard TM descriptions into a LaTeX-friendly form

def convertToNDigitString(x, n):
    return "0"*(n-len(str(x))) + str(x)

if __name__ == "__main__":
    tm = tmsim.SingleTapeTuringMachine(sys.argv[1], ["a", "b"])
    
    stateAbbrevDict = {}
        
#    outString = "{\\tiny \\tt \\noindent \\setstretch{0.5}"    


    outString = "\\centering\\resizebox{17cm}{!}{\\tt\\begin{tabular}{@{}l@{}}"    
        
    numDigitsPerName = len(str(len(tm.listOfRealStates)))        
        
    for i, state in enumerate(tm.listOfRealStates):
        stateAbbrevDict[state.stateName] = convertToNDigitString(i, numDigitsPerName)
        
    stateAbbrevDict["ERROR"] = "ERRO"
    stateAbbrevDict["HALT"] = "HALT"    
                
    lineBreakCounter = 0            
    pageBreakCounter = 0            
                
    for state in tm.listOfRealStates:
        
        aNextState = stateAbbrevDict[state.getNextState("a").stateName]
        aWrite = state.getWrite("a")
        aHeadMove = state.getHeadMove("a")
        bNextState = stateAbbrevDict[state.getNextState("b").stateName]
        bWrite = state.getWrite("b")
        bHeadMove = state.getHeadMove("b")
        
#        outString += stateAbbrevDict[state.stateName] + ":(a->" + aNextState + "," + aWrite + "," + aHeadMove + \
#            "|b->" + bNextState + "," + bWrite + "," + bHeadMove + ") "


        if aNextState == "ERRO":
            aString = "ERROR-"
        elif aNextState == "HALT":
            aString = "HALT--"
        else:
            aString = aNextState + "" + aWrite + "" + aHeadMove
            
        if bNextState == "ERRO":
            bString = "ERROR-"
        elif bNextState == "HALT":
            bString = "HALT--"
        else:
            bString = bNextState + "" + bWrite + "" + bHeadMove            
            
        outString += stateAbbrevDict[state.stateName] + "(" + aString + \
            "|" + bString + ") "
            
        lineBreakCounter = (lineBreakCounter + 1)%9
        pageBreakCounter = (pageBreakCounter + 1)%891
        
        if pageBreakCounter == 0:
            outString += "\\end{tabular}\\par}\\\\ \\resizebox{17cm}{!}{\\tt\\begin{tabular}{@{}l@{}}"
        elif lineBreakCounter == 0:
            outString += "\\\\"     


    outString += "\\end{tabular}\\par}\n"

    output = open(sys.argv[2], "w")
    output.write(outString)