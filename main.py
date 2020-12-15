from lexer import *
from parser import *
import sys

def main():
    print("Interpreter")
    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open (sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

    lexer = Lexer(input)
    token = lexer.getToken()

    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()
    
    parser = Parser(lexer)
    parser.program()

    print("Lexing Complete")
    print("Parsing Complete")
    print("File has been compiled")

main()
