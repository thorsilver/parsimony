from LaconicListener import LaconicListener

def pront(x):
    print x

def listSum(l):
    returnString = ""
    for i in l:
        returnString += i
        
    return returnString

class Function():
    def __init__(self, name):
        self.name = name
        self.funcString = "\n// Auto-generated code for function " + name + "\n\n"
        self.largestFilledReg = -1
        self.filledRegs = []
        self.ifCounter = 0
        self.whileCounter = 0
        self.ifElseCounter = 0
    
    def add(self, s):
        self.funcString += s
        
    def findSmallestUnfilledReg(self):
        x = 0
        while x in self.filledRegs:
            x += 1
            
        self.largestFilledReg = max(self.largestFilledReg, x)    
            
        return x
                
    def fillReg(self, reg):
        assert not (reg in self.filledRegs)
        self.filledRegs.append(reg)
    
    def emptyReg(self, reg):
        assert reg in self.filledRegs
        self.filledRegs.remove(reg)

class CodeWriter(LaconicListener):

    def enterProg(self, ctx):
        self.variableDictionary = {}
        self.funcProcDictionary = {}
        self.funcAuxCountDictionary = {}
        self.mainFunc = Function("main")
        self.funcSet = {}
        self.currentFunc = self.mainFunc
        self.currentFile = open("main.tmd", "w")
        self.BUILTIN_SYMBOL = "BUILTIN_"

    def exitTrueprog(self, ctx):
        self.writeMainInputLine()
        self.currentFile.write(self.mainFunc.funcString)
        
    def exitCommand(self, ctx):
        pass
        
    def enterFuncdef(self, ctx):
        funcName = ctx.funcprocbody().funcproccallbody().VAR(0).getText()
        self.funcProcDictionary[funcName] = "func"
        self.currentFunc = Function(funcName)
        self.currentFile = open(funcName + ".tmd", "w")
        
    def exitFuncdef(self, ctx):
        inputLine = "input "
        
        listOfArguments = []
        argumentBody = ctx.funcprocbody().funcproccallbody()
        
        varCounter = 1
        while argumentBody.VAR(varCounter) != None:
            listOfArguments.append(argumentBody.VAR(varCounter).getText())
            varCounter += 1
            
        for argument in listOfArguments:
            inputLine += argument + " "
            
        for reg in range(self.currentFunc.largestFilledReg + 1):
            inputLine += stringify(reg) + " "

        self.currentFunc.funcString = inputLine + "\n" + self.currentFunc.funcString

        self.currentFile.write(self.currentFunc.funcString)
        
        self.funcAuxCountDictionary[self.currentFunc.name] = self.currentFunc.largestFilledReg + 1
        self.currentFunc = self.mainFunc
        self.currentFile = open("main.tmd", "w")

    def enterProcDef(self, ctx):
        procName = ctx.funcprocbody().funcproccallbody().VAR(0).getText()
        self.funcProcDictionary[procName] = "proc"
        self.procArgsDictionary[procName] = ctx.funcprocbody().funcproccallbody()
        self.procBodyDictionary[procName] = ctx.funcprocbody().nondefprog()

    def enterFuncproccall(self, ctx):
        funcProcName = ctx.funcproccallbody().VAR(0).getText()
        
        try:
            assert funcProcName in self.funcProcDictionary
        except:
            pront("Error: unrecognized function name", funcProcName)
            raise

        args = ctx.funcproccallbody()
        
        if self.funcProcDictionary[funcProcName] == "func":
            self.currentFunc.add("function " + funcProcName + " ")
            # add in the arguments
            argCounter = 1
            while args.VAR(argCounter) != None:
                self.currentFunc.add(args.VAR(argCounter).getText() + " ")
                argCounter += 1
                
                
            assert len(self.currentFunc.filledRegs) == 0    
            # add in the dummy registers
            regsUsingForCall = []
            for i in range(self.funcAuxCountDictionary[funcProcName]):
                
                reg = self.currentFunc.findSmallestUnfilledReg()
                self.currentFunc.add(stringify(reg) + " ")  
                self.currentFunc.fillReg(reg)
                regsUsingForCall.append(reg)
                
            [self.currentFunc.emptyReg(reg) for reg in regsUsingForCall]
                
            self.currentFunc.add("\n")
            
        if self.funcProcDictionary[funcProcName] == "proc":
            
            # figure out which variables in the function declaration map to which variables in the function call
            mapping = {}
            declArgs = self.procArgsDictionary[funcProcName]
            callArgs = args
            
            argCounter = 1
            
            while declArgs.VAR(argCounter) != None:
                mapping[declArgs.VAR(argCounter)] = callArgs.VAR(argCounter)
                
                try:
                    assert callArgs.VAR(argCounter) != None
                except:
                    pront("Function call", funcProcName, "has too few arguments.")
                    raise
                
                argCounter += 1
                
            try:
                assert callArgs.VAR(argCounter) == None
            except:
                pront("Function call", funcProcName, "has too many arguments.")
                raise
                
            # ok procs just don't work for the time being
            
            
            self.currentFunc.add("")

    def manageRegs(self, ctx, listOfExprs, marker):
        ctx.associatedReg = self.currentFunc.findSmallestUnfilledReg()
        self.currentFunc.fillReg(ctx.associatedReg)
        
 #       print ctx.getText()
 #       print marker
 #       if ctx.getText() == "x<(#l)":
 #           print ctx.OPERATOR_COMPARE().getText()
        
        self.currentFunc.add(self.dealWithExpr(ctx, [ctx.associatedReg] + 
            [expr.associatedReg for expr in listOfExprs], marker))
            
        # release lock    
        for expr in listOfExprs:
            self.currentFunc.emptyReg(expr.associatedReg)        
        
    # release locks on the children and take hold of the lock on yourself
    def exitIntexpr(self, ctx):
        
        # 0 intexprs possibilities:
        # INT
        # VAR
        # OPERATOR_LENGTH listexpr
        # OPERATOR_LENGTH2 listexpr
        if (ctx.intexpr(0) == None):
            if ctx.INT() != None:
                # INT
                self.manageRegs(ctx, [], "intint")
                
            if ctx.VAR() != None:
                try:
                    pass
   #                 assert self.variableDictionary[ctx.VAR(0).getText()] == "int"
                except:
                    pront("Error: expected integer")
                    raise
                    
                self.manageRegs(ctx, [], "intvar")
                
            if ctx.OPERATOR_LENGTH() != None:
                self.manageRegs(ctx, [ctx.listexpr()], "len")
                
            if ctx.OPERATOR_LENGTH2() != None:
                self.manageRegs(ctx, [ctx.list2expr()], "len2")

        # Each expr has an associatedReg. That's where the value is stored.

        # 1 intexpr possibilities:
        # OPERATOR_NOT intexpr
        # OPERATOR_NEGATE intexpr
        # listexpr OPERATOR_INDEX intexpr
        # '(' intexpr ')'
        elif (ctx.intexpr(1) == None):
            
            if ctx.OPERATOR_INDEX() != None:
                # listexpr '[' intexpr ']'
                self.manageRegs(ctx, [ctx.listexpr(), ctx.intexpr(0)], "listindex")
        
            elif ctx.OPERATOR_NOT() != None:
                # OPERATOR_NOT intexpr
                self.manageRegs(ctx, [ctx.intexpr(0)], "intnot")
                
            elif ctx.OPERATOR_NEGATE() != None:
                # OPERATOR_NEGATE intexpr
                self.manageRegs(ctx, [ctx.intexpr(0)], "intneg")
        
            else:
                # if it's just parens don't do shit
                ctx.associatedReg = ctx.intexpr(0).associatedReg    
                
        # 2 intexpr possibilities
        # intexpr OPERATOR_MUL_DIV intexpr
        # intexpr OPERATOR_ADD_SUB intexpr 
        # intexpr OPERATOR_COMPARE intexpr
        # intexpr OPERATOR_BOOLEAN intexpr        
        else:
            # intexpr OPERATOR intexpr
            self.manageRegs(ctx, [ctx.intexpr(0), ctx.intexpr(1)], "intop")
            
    def exitListexpr(self, ctx):
        
        # 0 listexprs possibilities:
        # list2expr '[' intexpr ']'
        # '[' (intexpr ',')* intexpr ']'
        # '[' ']'
        # VAR
        if (ctx.listexpr(0) == None):
            
            if ctx.list2expr() != None:
                # list2expr '[' intexpr ']'
                self.manageRegs(ctx, [ctx.list2expr(), ctx.intexpr(0)], "list2index")
                
            elif ctx.intexpr(0) != None:
                # '[' (intexpr ',')* intexpr ']'
                                
                listOfExprs = []
                exprCounter = 0
                nextExpr = ctx.intexpr(exprCounter)
                
                while nextExpr != None:
                    listOfExprs.append(nextExpr)
                    
                    exprCounter += 1
                    nextExpr = ctx.intexpr(exprCounter)
                    
                self.manageRegs(ctx, listOfExprs, "constlist")    
                
            elif ctx.VAR() == None:
                # '[' ']'
                self.manageRegs(ctx, [], "emptylist")
                
            else: 
                # VAR
                try:
                    pass
  #                  assert self.variableDictionary[ctx.VAR().getText()] == "list"
                except:                    
                    pront("Error: expected list")
                    raise

                self.manageRegs(ctx, [], "listvar")
                
        # 1 list expr possiblities:
        # listexpr 'append' intexpr
        # '(' listexpr ')'
        elif ctx.listexpr(1) == None:
            
            if ctx.intexpr(0) != None:
                # listexpr 'append' intexpr
                self.manageRegs(ctx, [ctx.listexpr(0), ctx.intexpr(0)], "listappend")
                
            else:    
                # if it's just parens don't do shit
                ctx.associatedReg = ctx.listexpr(0).associatedReg  
                
        # 2 list expr possibilities:
        # listexpr 'concat' listexpr
        
        elif ctx.listexpr(2) == None:
            # listexpr 'concat' listexpr
            self.manageRegs(ctx, [ctx.listexpr(0), ctx.listexpr(1)], "listconcat")
                
        else:
            raise
            
            
    def exitList2expr(self, ctx):
        # 0 list2expr possibilities:
        # '[' (listexpr ',')* listexpr ']'
        # '[' ']'
        # VAR
        if ctx.list2expr(0) == None:
            
            if ctx.listexpr(0) != None:
                # '[' (listexpr ',')* listexpr ']'
                listOfExprs = []
                exprCounter = 0
                nextExpr = ctx.listexpr(exprCounter)
            
                while nextExpr != None:
                    listOfExprs.append(nextExpr)
                
                    exprCounter += 1
                    nextExpr = ctx.listexpr(exprCounter)
                
                self.manageRegs(ctx, listOfExprs, "constlist2")
            
            elif ctx.VAR() != None:
                # VAR
                try:
                    pass
#                    assert self.variableDictionary[ctx.VAR().getText()] == "list2"
                except:
                    pront("Error: expected list2")
                    raise

                self.manageRegs(ctx, [], "list2var")
                
            else:
                # '[' ']'
                self.manageRegs(ctx, [], "emptylist2")

        # 1 list2expr possibilities:
        # list2expr 'append' listexpr
        # '(' list2expr ')'
        elif ctx.list2expr(1) == None:
            
            if ctx.listexpr(0) != None:
                # listexpr 'append' intexpr
                self.manageRegs(ctx, [ctx.list2expr(0), ctx.listexpr(0)], "list2append")
                
            else:    
                # if it's just parens don't do shit
                ctx.associatedReg = ctx.list2expr(0).associatedReg 
                
        # 2 list2expr possibilities:
        # list2expr 'concat' list2expr
        else:
            # list2expr 'concat' list2expr
            self.manageRegs(ctx, [ctx.list2expr(0), ctx.list2expr(1)], "list2concat")   
                            
    def enterWhileloop(self, ctx):
        # Associate with the component parts the current whileCounter
        # This is an identifier to distinguish the various while loops
        ctx.whileexpr().whileCounter = self.currentFunc.whileCounter
        ctx.whilenondefprog().whileCounter = self.currentFunc.whileCounter
        
        self.currentFunc.whileCounter += 1
            
    def enterWhileexpr(self, ctx):
        self.currentFunc.add("WHILE_TEST_" + str(ctx.whileCounter) + ": ")

    def exitWhileexpr(self, ctx):
        assert len(self.currentFunc.filledRegs) == 1
        self.currentFunc.add("[" + stringify(self.currentFunc.filledRegs[0]) + \
            "] E (WHILE_STATE_" + str(ctx.whileCounter) + "_FALSE); 1 ()\n")
        
        self.currentFunc.emptyReg(self.currentFunc.filledRegs[0])
        
    def exitWhilenondefprog(self, ctx):
        dummyReg = self.currentFunc.findSmallestUnfilledReg()
        
        self.currentFunc.add("[" + stringify(dummyReg) + "] E (WHILE_TEST_" + str(ctx.whileCounter) + \
            "); 1 (WHILE_TEST_" + str(ctx.whileCounter) + ")\n")
        # goto top of while loop no matter what    
        self.currentFunc.add("WHILE_STATE_" + str(ctx.whileCounter) + "_FALSE: ")
            
    def enterIfstate(self, ctx):
        # Associate with the component parts the current ifCounter
        # This is an identifier to distinguish the various while loops
        ctx.ifexpr().ifCounter = self.currentFunc.ifCounter
        ctx.ifnondefprog().ifCounter = self.currentFunc.ifCounter
                
        self.currentFunc.ifCounter += 1

    # if the holder variable that holds the expression has a positive value, skip to the label at the end of the if statement
    def exitIfexpr(self, ctx):
        assert len(self.currentFunc.filledRegs) == 1
        self.currentFunc.add("[" + stringify(self.currentFunc.filledRegs[0]) + "] E (IF_STATE_" + \
            str(ctx.ifCounter) + "_FALSE); 1 ()\n")
        
        self.currentFunc.emptyReg(self.currentFunc.filledRegs[0])    
        
    # Place the label at the end of the concluded if statement. Note the intentional lack of \n
    def exitIfnondefprog(self, ctx):        
        self.currentFunc.add("IF_STATE_" + str(ctx.ifCounter) + "_FALSE: ")
        
    def enterIfelsestate(self, ctx):    
        # Associate with the component parts the current ifElseCounter
        # This is an identifier to distinguish the various while loops      
        ctx.ifelseexpr().ifElseCounter = self.currentFunc.ifElseCounter
        ctx.ifelsenondefprog().ifElseCounter = self.currentFunc.ifElseCounter
        ctx.elsenondefprog().ifElseCounter = self.currentFunc.ifElseCounter
          
        self.currentFunc.ifElseCounter += 1  
          
    def exitIfelseexpr(self, ctx):
        assert len(self.currentFunc.filledRegs) == 1
        self.currentFunc.add("[" + stringify(self.currentFunc.filledRegs[0]) + "] E (IF_ELSE_STATE_" + \
            str(ctx.ifElseCounter) + "_FALSE); 1 ()\n")
        
        self.currentFunc.emptyReg(self.currentFunc.filledRegs[0])
    
    def exitIfelsenondefprog(self, ctx):
        dummyReg = self.currentFunc.findSmallestUnfilledReg()        
        
        self.currentFunc.add("[" + stringify(dummyReg) + "] E (IF_ELSE_STATE_" + str(ctx.ifElseCounter) + \
            "_TRUE); 1 (IF_ELSE_STATE_" + str(ctx.ifElseCounter) + "_TRUE)\n")
        # goto end no matter what
        self.currentFunc.add("IF_ELSE_STATE_" + str(ctx.ifElseCounter) + "_FALSE: ")
        
    def exitElsenondefprog(self, ctx):
        self.currentFunc.add("IF_ELSE_STATE_" + str(ctx.ifElseCounter) + "_TRUE: ")

    def exitAssign(self, ctx):
        # should be just one reg full, since it's the root of the expression tree
        assert len(self.currentFunc.filledRegs) == 1
        self.currentFunc.add("function " + self.BUILTIN_SYMBOL + "assign " + ctx.VAR().getText() + " " + stringify(self.currentFunc.filledRegs[0]) + "\n")

        self.currentFunc.emptyReg(self.currentFunc.filledRegs[0])

#        self.currentFile.write(self.dealWithExpr(ctx.expr(), ctx.VAR(), self.filledRegs[0], None))

    def exitReturnstate(self, ctx):
        self.currentFunc.add("return\n")

    def makeStandardNoteAndLine(self, funcName, regListInStringForm):
        self.funcSet[funcName] = True
        return "function " + self.BUILTIN_SYMBOL + funcName + regListInStringForm

    # Loads the result of the operation ctx on regs listOfRegs into reg 1
    def dealWithExpr(self, ctx, listOfRegs, marker):
        # This doesn't get used every time, only when it fits the
        # situation
        regListInStringForm = listSum([" " + stringify(i) for i in listOfRegs]) + "\n"
        
        if marker == "intint":
            assert len(listOfRegs) == 1
            if ctx.INT().getText() == "0":
                self.funcSet["clear"] = True
                return "function " + self.BUILTIN_SYMBOL + "clear " + regListInStringForm
            
            else:
                self.funcSet["assign" + ctx.INT().getText()] = True
                return "function " + self.BUILTIN_SYMBOL + "assign" + ctx.INT().getText() + " " + \
                    stringify(listOfRegs[0]) + "\n"
                
        elif (marker == "intvar") or (marker == "listvar") or (marker == "list2var"):
            assert len(listOfRegs) == 1
            self.funcSet["assign"] = True
            return "function " + self.BUILTIN_SYMBOL + "assign " + stringify(listOfRegs[0]) + " " + ctx.VAR().getText() + "\n"
        
        elif marker == "intnot":
            assert len(listOfRegs) == 2
            return self.makeStandardNoteAndLine("assignNot", regListInStringForm)
        
        elif marker == "intop":
            if ctx.OPERATOR_BOOLEAN() != None:
                assert len(listOfRegs) == 3
                if ctx.OPERATOR_BOOLEAN().getText() == "&":
                    return self.makeStandardNoteAndLine("and", regListInStringForm)
                
                elif ctx.OPERATOR_BOOLEAN().getText() == "|":
                    return self.makeStandardNoteAndLine("or", regListInStringForm)  
            
                else:
                    pront("bad operator " + ctx.OPERATOR_BOOLEAN.getText())
                    raise             
                    
            elif ctx.OPERATOR_MUL_DIV() != None:    
                assert len(listOfRegs) == 3
                if ctx.OPERATOR_MUL_DIV().getText() == "*":
                    return self.makeStandardNoteAndLine("multiply", regListInStringForm)
            
                elif ctx.OPERATOR_MUL_DIV().getText() == "/":
                    return self.makeStandardNoteAndLine("divide", regListInStringForm)
            
                elif ctx.OPERATOR_MUL_DIV().getText() == "%":
                    return self.makeStandardNoteAndLine("modulus", regListInStringForm)
            
                else:
                    pront("bad operator " + ctx.OPERATOR_MUL_DIV().getText())
                    raise        
                    
            elif ctx.OPERATOR_ADD_SUB() != None:    
                if ctx.OPERATOR_ADD_SUB().getText() == "+":
                    return self.makeStandardNoteAndLine("add", regListInStringForm)
            
                elif ctx.OPERATOR_ADD_SUB().getText() == "-":
                    return self.makeStandardNoteAndLine("subtract", regListInStringForm)
                
                else:
                    pront("bad operator " + ctx.OPERATOR_ADD_SUB().getText())     
                    raise  

            elif ctx.OPERATOR_COMPARE() != None:
                if ctx.OPERATOR_COMPARE().getText() == ">":
                    return self.makeStandardNoteAndLine("greaterThan", regListInStringForm)

                elif ctx.OPERATOR_COMPARE().getText() == "<":
                    
                    # Note the inversion of reg2 and reg3
                    self.funcSet["greaterThan"] = True
                    return "function " + self.BUILTIN_SYMBOL + "greaterThan " + stringify(listOfRegs[0]) + " " + \
                        stringify(listOfRegs[2]) + " " + stringify(listOfRegs[1]) + "\n"
        
                elif ctx.OPERATOR_COMPARE().getText() == ">=":
                    return self.makeStandardNoteAndLine("greaterOrEqual", regListInStringForm)
        
                elif ctx.OPERATOR_COMPARE().getText() == "<=":
                    # Note the inversion of reg2 and reg3
                    self.funcSet["greaterOrEqual"] = True
                    return "function " + self.BUILTIN_SYMBOL + "greaterOrEqual " + stringify(listOfRegs[0]) + " " + \
                        stringify(listOfRegs[2]) + " " + stringify(listOfRegs[1]) + "\n"
        
                elif ctx.OPERATOR_COMPARE().getText() == "==":
                    return self.makeStandardNoteAndLine("equal", regListInStringForm)
        
                elif ctx.OPERATOR_COMPARE().getText() == "!=":
                    return self.makeStandardNoteAndLine("notEqual", regListInStringForm)
            
                else:
                    pront("bad operator " + comp.getText())
                    raise                                
                
        elif marker == "constlist":
            return self.makeStandardNoteAndLine("listAssemble" + str(len(listOfRegs)-1), \
                regListInStringForm)
                    
        elif marker == "constlist2":            
            return self.makeStandardNoteAndLine("list2Assemble" + str(len(listOfRegs)-1), \
                regListInStringForm)
                
        else:
            return self.makeStandardNoteAndLine(marker, regListInStringForm)
            
    def exitProg(self, ctx):
        pass

    def enterIntdecl(self, ctx):                
        self.variableDictionary[ctx.VAR().getText()] = "int"

    def enterListdecl(self, ctx):                
        self.variableDictionary[ctx.VAR().getText()] = "list"

    def enterList2decl(self, ctx):              
        self.variableDictionary[ctx.VAR().getText()] = "list2"
        
    def writeMainInputLine(self):
        inputLine = "input "
        
        for varName in self.variableDictionary:
            inputLine += varName + " "
        
        for reg in range(self.currentFunc.largestFilledReg + 1):
            inputLine += stringify(reg) + " "    
            
        inputLine += "\n"
        
        self.mainFunc.funcString = inputLine + self.mainFunc.funcString

def stringify(regNum):
    return "!" + str(regNum)
