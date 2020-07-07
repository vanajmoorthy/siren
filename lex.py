import enum
import sys


class TokenType(enum.Enum):
    # Chars.
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3

    # Keywords.
    # Arbitrarily set keyword values between 100 and 200 for later check.

    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111

    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211


class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText
        self.kind = tokenKind

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None


class Lexer:
    def __init__(self, input):
        self.source = input + "\n"  # Append \n to make lexing easier
        self.curChar = ""
        self.curPos = -1
        self.nextChar()

    # Go to next char
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = "\0"  # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Return peek char
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return "\0"  # EOF
        return self.source[self.curPos + 1]

    # Error out if invalid token
    def abort(self, message):
        sys.exit("Error while lexing: {}".format(message))

    # Skip whitespace except \n
    def skipWhitespace(self):
        while self.curChar == " " or self.curChar == "\t" or self.curChar == "\r":
            self.nextChar()

    # Skip comments
    def skipComments(self):
        if self.curChar == "#":
            while self.curChar != "\n":
                self.nextChar()

    # Return next token
    def getToken(self):
        self.skipWhitespace()
        self.skipComments()
        token = None

        # Identify tokens
        if self.curChar == "+":
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == "-":
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == "*":
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == "/":
            token = Token(self.curChar, TokenType.SLASH)

        elif self.curChar == "=":
            # Check whether this token is = or ==
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == ">":
            # Check whether this is token is > or >=
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == "<":
            # Check whether this is token is < or <=
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == "!":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.curChar == '"':
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '"':
                # Ban special chars in string
                if (
                    self.curChar == "\r"
                    or self.curChar == "\n"
                    or self.curChar == "\t"
                    or self.curChar == "\\"
                    or self.curChar == "%"
                ):
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos : self.curPos]  # Get the substring.
            token = Token(tokText, TokenType.STRING)
        elif self.curChar.isdigit():
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == ".":
                self.nextChar()

                # Must have at least one digit after decimal.
                if not self.peek().isdigit():
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1]  # Get the substring.
            token = Token(tokText, TokenType.NUMBER)
        elif self.curChar.isalpha():
            # Leading character is a letter, so this must be an identifier or a keyword.
            # Get all consecutive alpha numeric characters.
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()

            # Check if the token is in the list of keywords.
            tokText = self.source[startPos : self.curPos + 1]  # Get the substring.
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None:  # Identifier
                token = Token(tokText, TokenType.IDENT)
            else:  # Keyword
                token = Token(tokText, keyword)
        elif self.curChar == "\n":
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == "\0":
            token = Token(self.curChar, TokenType.EOF)
        else:
            self.abort("Unkown token {}".format(self.curChar))

        self.nextChar()
        return token

