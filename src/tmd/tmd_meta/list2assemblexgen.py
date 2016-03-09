import sys

def listSum(x):
    returnString = ""
    
    for i in x:
        returnString += i
        
    return returnString

def writeAssemblesUpToX(x, builtinSymbol):
    if x >= 1:
    
        output = open(builtinSymbol + "list2Assemble1.tfn", "w")
        output.write("input x i0\n\n")
        output.write("// Auto-generated code for function " + builtinSymbol + "list2Assemble1\n")
        output.write("// Assigns x to the value :i0:\n")
        output.write("// LPP list2 format assumed\n\n")
        output.write("function " + builtinSymbol + "clear x\n")
        output.write("function " + builtinSymbol + "appendTo2 x i0\n")
        output.write("return\n")
        
        for i in range(2, x+1):
            output = open(builtinSymbol + "list2Assemble" + str(i) + ".tfn", "w")
            inputLine = "input x " + listSum(["i" + str(j) + " " for j in range(i)])
            output.write(inputLine + "\n\n")
            output.write("// Auto-generated code for function " + builtinSymbol + \
                "assembleList" + str(i) + "\n")
            output.write("// Assigns x to the value :" + \
                listSum(["i" + str(j) + ", " for j in range(i-1)]) + "i" + str(i-1) + ":\n")
            output.write("// LPP list2 format assumed\n\n")
            output.write("function " + builtinSymbol + "list2Assemble" + str(i-1) + " x " + \
                listSum(["i" + str(j) + " " for j in range(i-1)]) + "\n")
            output.write("function " + builtinSymbol + "appendTo2 x i" + str(i-1) + "\n")
            output.write("return\n")    
                
if __name__ == "__main__":
    writeAssemblesUpToX(int(sys.argv[1]), "BUILTIN_")                
    