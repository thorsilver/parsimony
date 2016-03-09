from antlr4 import *
import sys
import os
from LaconicLexer import LaconicLexer
from LaconicParser import LaconicParser
from LaconicListener import LaconicListener
from codeexecutor import *
import time

# Interprets a Laconic program on the fly, as though it was 
# a standard programming language. 

# Use this program to debug your Laconic program before 
# compiling it to a Turing Machine!

def main(argv):
    try:
        assert len(argv) == 2
    except:
        raise Exception("Usage: python laconic_interpreter.py [name of file without extension]")
    
    try:
        inp = FileStream("../laconic_files/" + argv[1] + ".lac")
    except:
        raise Exception("File not found: parsimony/src/laconic/laconic_files/" + argv[1] + ".lac")
        
    lexer = LaconicLexer(inp)
    stream = CommonTokenStream(lexer)
    parser = LaconicParser(stream)
    tree = parser.prog()

    executor = CodeExecutor()
    walker = ParseTreeWalker()
    walker.walk(executor, tree)

if __name__ == '__main__':
    main(sys.argv)
