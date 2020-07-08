from lex import *
from parse import *
import sys


def main():
    print("Siren")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], "r") as inputFile:
        input = inputFile.read()

    lexer = Lexer(input)
    parser = Parser(lexer)

    parser.program()
    print("Parsing completed.")


main()
