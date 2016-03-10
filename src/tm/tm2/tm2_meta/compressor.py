import sys
import tmsim

# A script for converting my standard TM descriptions into a LaTeX-friendly form

def convertToNDigitString(x, n):
    return "0"*(n-len(str(x))) + str(x)

if __name__ == "__main__":
    tm = tmsim.SingleTapeTuringMachine(sys.argv[1], ["a", "b"])
    
    stateAbbrevDict = {}
        
#    outString = "{\\tiny \\tt \\noindent \\setstretch{0.5}"    

    outString = "\\scalebox{0.4}{\\tt \\noindent \\setstretch{0.5}\\hbox{"    
        
    numDigitsPerName = len(str(len(tm.listOfRealStates)))        
        
    for i, state in enumerate(tm.listOfRealStates):
        stateAbbrevDict[state.stateName] = convertToNDigitString(i, numDigitsPerName)
        
    stateAbbrevDict["ERROR"] = "ERRO"
    stateAbbrevDict["HALT"] = "HALT"    
                
    counter = 0            
                
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
            
        counter = (counter + 1)%10
        if counter == 0:
            outString += "}\\hbox{"     


    outString += "}\\par}\n"

    output = open(sys.argv[2], "w")
    output.write(outString)