import enum
import sys

class Lexer:
    def __init__(self, input):
        self.source = input + '\n'
        self.curChar = ''
        self.curPos = -1
        self.nextChar()

    def getToken(self):
        self.skipWhiteSpace()
        self.ignoreComments()

        token = None

        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == ':':
            token = Token(self.curChar, TokenType.COLON)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token(self.curChar, TokenType.EOF)
        elif self.curChar == '(':
            token = Token(self.curChar, TokenType.OPARN)
        elif self.curChar == ')':
            token = Token(self.curChar, TokenType.CPARN)
        elif self.curChar == ',':
            token = Token(self.curChar, TokenType.COMMA)

        elif self.curChar == '%':
            #Logic to differentiate between - and -=
            if self.lookNext() == '=':
                lastCharacter = self.curChar
                self.nextChar()
                token = Token(lastCharacter + self.curChar, TokenType.REMAINEQ)
            else:
                token = Token(self.curChar, TokenType.REMAINDER)

        elif self.curChar == '-':
            #Logic to differentiate between - and -=
            if self.lookNext() == '=':
                lastCharacter = self.curChar
                self.nextChar()
                token = Token(lastCharacter + self.curChar, TokenType.MINEQ)
            else:
                token = Token(self.curChar, TokenType.MINUS)

        elif self.curChar == '=':
            # logic in place to differentiate between = and ==
            if self.lookNext() == '=':
                lastCharacter = self.curChar
                self.nextChar()
                token = Token(lastCharacter + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)

        elif self.curChar == '>':
            # logic in place to differentiate between > and >=
            if self.lookNext() == '=':
                lastCharacter = self.curChar
                self.nextChar()
                token = Token(lastCharacter + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)

        elif self.curChar == '<':
            # logic in place to differentiate between < and <=
            if self.lookNext() == '=':
                lastCharacter = self.curChar
                self.nextChar()
                token = Token(lastCharacter + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)

        elif self.curChar == '!':
            # logic in place to differentiate between ! and !=
            if self.lookNext() == '=':
                lastCharacter = self.curChar
                self.nextChar()
                token = Token(lastCharacter + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.lookNext())
        
        elif self.curChar == '\"':
        # Get characters between quotations
            self.nextChar()
            startPos = self.curPos
        
            while self.curChar != '\"':
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos : self.curPos] # Get the substring
            token = Token(tokText, TokenType.STRING)

        elif self.curChar.isdigit():
            startPos = self.curPos

            while self.lookNext().isdigit():
                self.nextChar()

            if self.lookNext() == '.':
                self.nextChar()

                if not self.lookNext().isdigit():
                    self.abort("Illegal character in number.")
                while self.lookNext().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1]
            token = Token(tokText, TokenType.NUMBER)

        elif self.curChar.isalpha():
            startPosition = self.curPos
            while self.lookNext().isalnum() or self.lookNext() == '_':
                self.nextChar()

            tokenText = self.source[startPosition : self.curPos + 1]
            keyword = Token.checkIfKeyword(tokenText)
            if keyword == None:
                token = Token(tokenText, TokenType.IDENT)
            else:
                token = Token(tokenText, keyword)
        else:
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token

    def nextChar(self):
        self.curPos += 1

        if self.curPos >= len(self.source):
            self.curChar = '\0'
        else:
            self.curChar = self.source[self.curPos]

    def lookNext(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        else:
            return self.source[self.curPos + 1]

    def abort(self, message):
        sys.exit("Lexing error. " + message)

    def ignoreComments(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()
    
    def skipWhiteSpace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()
# Token contains the original text and the type of token.
class Token:   
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText   # The token's actual text. Used for identifiers, strings, and numbers.
        self.kind = tokenKind   # The TokenType that this token is classified as.

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            if kind.name == tokenText.upper() and kind.value >= 100 and kind.value < 200:
                return kind
        return None

# TokenType is our enum for all the types of tokens.
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    COLON = 4
    # Keywords.
    PRINT = 101
    IF = 102
    ELSE = 103
    FOR = 104
    WHILE = 105
    # Operators.
    EQ = 201  
    PLUS = 202
    MINUS = 203
    MINEQ = 204
    ASTERISK = 205
    SLASH = 206
    EQEQ = 207
    NOTEQ = 208
    LT = 209
    LTEQ = 210
    GT = 211
    GTEQ = 212
    OPARN = 213
    CPARN = 214
    COMMA = 215
    REMAINDER = 216
    REMAINEQ = 217
    # Assignment
    EQL = 301
    PEQL = 302
    MEQL = 303
    AEQL = 304
    DEQL = 305
    CEQL = 306
    MODEQL = 307
