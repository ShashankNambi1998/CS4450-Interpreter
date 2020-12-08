from lexer import *
from parser import *
import sys


def main():
    test = "+ - 123 9.8654 * /"
    lexer = Lexer(test)
    token = lexer.getToken()


    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()
    # Initialize lexer and parser	
    parser = Parser(lexer)	

    parser.program() # Start parser.	
    print("Parsing completed.")	


    print("Lexing Complete")


main()