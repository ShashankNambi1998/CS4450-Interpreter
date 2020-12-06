from lexer import *
from parse import *
import sys

def main():
    test = "+ - 123 9.8654 * /"
    lexer = Lexer(test)
    token = lexer.getToken()

    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()
    # Initialize lexer and parser
    lexer = Lexer(input)
    parser = Parser(lexer)

    parser.program() # Start parser.
    print("Parsing completed.")


main()
