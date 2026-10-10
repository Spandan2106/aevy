
from .token import Token, TokenType


KEYWORDS = {
    "func": TokenType.FUNC,
    "class": TokenType.CLASS,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "for": TokenType.FOR,
    "in": TokenType.IN,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "True": TokenType.TRUE,
    "False": TokenType.FALSE,
}


class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []

        self.start = 0
        self.current = 0

        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column
            self.scan_token()

        self.tokens.append(
            Token(TokenType.EOF, None, self.line, self.column)
        )
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        next_index = self.current + 1
        if next_index >= len(self.source):
            return "\0"
        return self.source[next_index]

    def match(self, expected):
        if self.is_at_end() or self.source[self.current] != expected:
            return False

        self.advance()
        return True

    def scan_token(self):
        char = self.advance()

        # Ignore spaces and tabs between tokens.
        if char in " \t\r":
            return

        # Ignore comments beginning with //.
        if char == "/" and self.peek() == "/":
            while not self.is_at_end() and self.peek() != "\n":
                self.advance()
            return

        # Newline.
        if char == "\n":
            self.line += 1
            self.column = 1
            self.tokens.append(
                Token(
                    TokenType.NEWLINE,
                    "\n",
                    self.start_line,
                    self.start_column,
                )
            )
            return

        # Strings.
        if char == '"':
            self.string()
            return

        # Numbers.
        if char.isdigit():
            self.number()
            return

        # Identifiers and keywords.
        if char.isalpha() or char == "_":
            self.identifier()
            return

        # Two-character operators must be checked first.
        if char == "=" and self.match("="):
            self.add_token(TokenType.EQUAL_EQUAL, "==")
            return

        if char == "!" and self.match("="):
            self.add_token(TokenType.BANG_EQUAL, "!=")
            return

        if char == "<":
            if self.match("="):
                self.add_token(TokenType.LESS_EQUAL, "<=")
            else:
                self.add_token(TokenType.LESS, "<")
            return

        if char == ">":
            if self.match("="):
                self.add_token(TokenType.GREATER_EQUAL, ">=")
            else:
                self.add_token(TokenType.GREATER, ">")
            return

        # One-character operators and punctuation.
        single_char_tokens = {
            "=": TokenType.ASSIGN,
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
            "/": TokenType.SLASH,
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            "{": TokenType.LBRACE,
            "}": TokenType.RBRACE,
            ",": TokenType.COMMA,
            ":": TokenType.COLON,
            ".": TokenType.DOT,
        }

        if char in single_char_tokens:
            self.add_token(single_char_tokens[char], char)
            return

        if char == "!":
            raise SyntaxError(
                f"Unexpected character '!' at line {self.start_line}, "
                f"column {self.start_column}. Did you mean '!='?"
            )

        raise SyntaxError(
            f"Unexpected character {char!r} "
            f"at line {self.start_line}, "
            f"column {self.start_column}"
        )

    def add_token(self, token_type, value):
        self.tokens.append(
            Token(
                token_type,
                value,
                self.start_line,
                self.start_column,
            )
        )

    def string(self):
        while not self.is_at_end() and self.peek() != '"':
            if self.peek() == "\n":
                raise SyntaxError(
                    f"Unterminated string at line {self.start_line}"
                )
            self.advance()

        if self.is_at_end():
            raise SyntaxError(
                f"Unterminated string at line {self.start_line}"
            )

        # Consume the closing quote.
        self.advance()

        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        # Accept a decimal point when a digit follows it.
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        text = self.source[self.start:self.current]

        if "." in text:
            value = float(text)
        else:
            value = int(text)

        self.add_token(TokenType.NUMBER, value)

    def identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()

        text = self.source[self.start:self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)

        if token_type == TokenType.TRUE:
            value = True
        elif token_type == TokenType.FALSE:
            value = False
        else:
            value = text

        self.add_token(token_type, value)
