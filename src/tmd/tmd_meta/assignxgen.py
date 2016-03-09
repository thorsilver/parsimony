import sys

def writeAssignsUpToX(x, builtinSymbol):
    if x >= 1:
        output = open(builtinSymbol + "assign1.tfn", "w")
        output.write("input x\n\n")
        output.write("// Auto-generated code for function " + builtinSymbol + "assign1\n")
        output.write("// Assigns x to the value 1\n")
        output.write("// Unary assumed\n\n")
        output.write("function " + builtinSymbol + "clear x\n")
        output.write("function " + builtinSymbol + "add1 x\n")
        output.write("return\n")
            
        for i in range(2, x+1):
            output = open(builtinSymbol + "assign" + str(i) + ".tfn", "w")
            output.write("input x\n\n")
            output.write("// Auto-generated code for function " + builtinSymbol + "assign" + str(i) + "\n")
            output.write("// Assigns x to the value " + str(i) + "\n")
            output.write("// Unary assumed\n\n")
            output.write("function " + builtinSymbol + "assign" + str(i-1) + " x\n")
            output.write("function " + builtinSymbol + "add1 x\n")
            output.write("return\n")
            
if __name__ == "__main__":
    writeAssignsUpToX(int(sys.argv[1]), "BUILTIN_")