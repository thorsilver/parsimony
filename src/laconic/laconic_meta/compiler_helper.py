from antlr4 import *
import sys
import os
from LaconicLexer import LaconicLexer
from LaconicParser import LaconicParser
from LaconicListener import LaconicListener
from codewriter import *
import time

def main(argv):
    input = FileStream(argv[1])
    lexer = LaconicLexer(input)
    stream = CommonTokenStream(lexer)
    parser = LaconicParser(stream)
    tree = parser.prog()

    writer = CodeWriter()
    walker = ParseTreeWalker()
    walker.walk(writer, tree)

if __name__ == '__main__':
    main(sys.argv)
