from .token import Token, TokenType





KEYWORDS = {

    "func": TokenType.FUNC,

    "class": TokenType.CLASS,
    "extends": TokenType.EXTENDS,

    "if": TokenType.IF,

    "elif": TokenType.ELIF,

    "else": TokenType.ELSE,

    "for": TokenType.FOR,

    "while": TokenType.WHILE,

    "in": TokenType.IN,

    "and": TokenType.AND,

    "or": TokenType.OR,

    "not": TokenType.NOT,

    "True": TokenType.TRUE,

    "False": TokenType.FALSE,

    "break": TokenType.BREAK,

    "continue": TokenType.CONTINUE,

    "return": TokenType.RETURN,

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

        self.indent_stack = [0]

        self.at_line_start = True

        self.indent_style = None



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

        if self.current + 1 >= len(self.source):

            return "\0"

        return self.source[self.current + 1]



    def match(self, expected):

        if self.is_at_end() or self.source[self.current] != expected:

            return False



        self.advance()

        return True



    def add_token(self, token_type, value):

        self.tokens.append(

            Token(

                token_type,

                value,

                self.start_line,

                self.start_column,

            )

        )



    # -------------------------

    # INDENTATION

    # -------------------------



    def handle_indentation(self):

        indent = 0

        saw_space = False

        saw_tab = False



        while not self.is_at_end() and self.peek() in " \t":

            char = self.advance()



            if char == " ":

                indent += 1

                saw_space = True

            else:

                indent += 4

                saw_tab = True



        # Ignore blank lines and comment-only lines.

        if self.peek() == "\n" or self.is_at_end():

            return



        if self.peek() == "/" and self.peek_next() == "/":

            return



        if saw_space and saw_tab:

            raise SyntaxError(

                f"Mixed tabs and spaces at line {self.line}, column 1"

            )



        if saw_space or saw_tab:

            style = "tabs" if saw_tab else "spaces"



            if self.indent_style is None:

                self.indent_style = style

            elif self.indent_style != style:

                raise SyntaxError(

                    f"Inconsistent indentation style at line {self.line}, column 1"

                )



        current_indent = self.indent_stack[-1]



        if indent > current_indent:

            self.indent_stack.append(indent)

            self.tokens.append(

                Token(TokenType.INDENT, indent, self.line, 1)

            )



        elif indent < current_indent:

            while (

                len(self.indent_stack) > 1

                and indent < self.indent_stack[-1]

            ):

                self.indent_stack.pop()

                self.tokens.append(

                    Token(TokenType.DEDENT, indent, self.line, 1)

                )



            if indent != self.indent_stack[-1]:

                raise SyntaxError(

                    f"Invalid indentation at line {self.line}, column 1"

                )



    # -------------------------

    # SCAN TOKENS

    # -------------------------



    def scan_tokens(self):

        while not self.is_at_end():

            if self.at_line_start:

                self.handle_indentation()

                self.at_line_start = False



                if self.is_at_end():

                    break



                # Blank line

                if self.peek() == "\n":

                    self.start = self.current

                    self.start_line = self.line

                    self.start_column = self.column

                    self.scan_token()

                    self.at_line_start = True

                    continue



                # Comment-only line

                if self.peek() == "/" and self.peek_next() == "/":

                    while (

                        not self.is_at_end()

                        and self.peek() != "\n"

                    ):

                        self.advance()



                    if not self.is_at_end():

                        self.start = self.current

                        self.start_line = self.line

                        self.start_column = self.column

                        self.scan_token()



                    self.at_line_start = True

                    continue



            self.start = self.current

            self.start_line = self.line

            self.start_column = self.column



            self.scan_token()



            if (

                self.tokens

                and self.tokens[-1].type == TokenType.NEWLINE

            ):

                self.at_line_start = True



        # Close remaining indentation levels.

        while len(self.indent_stack) > 1:

            self.indent_stack.pop()

            self.tokens.append(

                Token(

                    TokenType.DEDENT,

                    None,

                    self.line,

                    self.column,

                )

            )



        self.tokens.append(

            Token(

                TokenType.EOF,

                None,

                self.line,

                self.column,

            )

        )



        return self.tokens



    def scan_token(self):

        char = self.advance()



        if char in " \t\r":

            return



        # Comments

        if char == "/" and self.peek() == "/":

            while (

                not self.is_at_end()

                and self.peek() != "\n"

            ):

                self.advance()

            return



        # Newline

        if char == "\n":

            self.line += 1

            self.column = 1

            self.add_token(TokenType.NEWLINE, "\n")

            return



        # Strings

        if char == '"':

            self.string()

            return



        # Numbers

        if char.isdigit():

            self.number()

            return



        # Identifiers and keywords

        if char.isalpha() or char == "_":

            self.identifier()

            return



        # Range operator: ..

        if char == ".":

            if self.match("."):

                self.add_token(TokenType.RANGE, "..")

            else:

                self.add_token(TokenType.DOT, ".")

            return



        # Two-character operators

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



        # Single-character tokens

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

        }



        if char in single_char_tokens:

            self.add_token(single_char_tokens[char], char)

            return



        raise SyntaxError(

            f"Unexpected character {char!r} at line "

            f"{self.start_line}, column {self.start_column}"

        )



    # -------------------------

    # STRINGS, NUMBERS, IDENTIFIERS

    # -------------------------



    def string(self):

        while (

            not self.is_at_end()

            and self.peek() != '"'

        ):

            if self.peek() == "\n":

                raise SyntaxError(

                    f"Unterminated string at line {self.start_line}, column {self.start_column}"

                )

            self.advance()



        if self.is_at_end():

            raise SyntaxError(

                f"Unterminated string at line {self.start_line}, column {self.start_column}"

            )



        self.advance()



        value = self.source[self.start + 1:self.current - 1]

        self.add_token(TokenType.STRING, value)



    def number(self):

        while self.peek().isdigit():

            self.advance()



        # Decimal point only when followed by a digit.

        # This keeps 1..5 separate from a decimal number.

        if self.peek() == "." and self.peek_next().isdigit():

            self.advance()



            while self.peek().isdigit():

                self.advance()



        text = self.source[self.start:self.current]

        value = float(text) if "." in text else int(text)



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