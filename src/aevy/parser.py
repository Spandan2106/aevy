
from .token import TokenType

from .ast_nodes import (
    Program,
    Literal,
    Variable,
    BinaryExpression,
    UnaryExpression,
    Assignment,
    ShowStatement,
    ExpressionStatement,
    IfStatement,
    ElifBranch,
    ForStatement,
    WhileStatement,
    BreakStatement,
    ContinueStatement,
    FunctionDeclaration,
    FunctionCall,
    ReturnStatement,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    # -------------------------
    # PROGRAM
    # -------------------------

    def parse(self):
        statements = []

        while not self.is_at_end():
            if self.match(TokenType.NEWLINE, TokenType.DEDENT):
                continue

            statements.append(self.statement())

        return Program(statements)

    # -------------------------
    # STATEMENTS
    # -------------------------

    def statement(self):
        if self.check(TokenType.FUNC):
            return self.function_declaration()

        if self.check(TokenType.RETURN):
            return self.return_statement()

        if self.check(TokenType.IF):
            return self.if_statement()

        if self.check(TokenType.FOR):
            return self.for_statement()

        if self.check(TokenType.WHILE):
            return self.while_statement()

        if self.check(TokenType.BREAK):
            self.advance()
            self.consume_line_end()
            return BreakStatement()

        if self.check(TokenType.CONTINUE):
            self.advance()
            self.consume_line_end()
            return ContinueStatement()

        if (
            self.check(TokenType.IDENTIFIER)
            and self.peek().value == "show"
        ):
            return self.show_statement()

        if (
            self.check(TokenType.IDENTIFIER)
            and self.check_next(TokenType.ASSIGN)
        ):
            return self.assignment()

        expression = self.expression()
        self.consume_line_end()
        return ExpressionStatement(expression)

    # -------------------------
    # FUNCTIONS
    # -------------------------

    def function_declaration(self):
        self.consume(TokenType.FUNC, "Expected 'func'")

        name = self.consume(
            TokenType.IDENTIFIER,
            "Expected a function name",
        ).value

        self.consume(
            TokenType.LPAREN,
            "Expected '(' after function name",
        )

        parameters = []

        if not self.check(TokenType.RPAREN):
            while True:
                parameter = self.consume(
                    TokenType.IDENTIFIER,
                    "Expected a parameter name",
                ).value

                if parameter in parameters:
                    raise SyntaxError(
                        f"Duplicate parameter '{parameter}'"
                    )

                parameters.append(parameter)

                if not self.match(TokenType.COMMA):
                    break

        self.consume(
            TokenType.RPAREN,
            "Expected ')' after parameters",
        )

        self.consume(
            TokenType.LBRACE,
            "Expected '{' before function body",
        )

        self.skip_newlines()

        # The lexer emits INDENT for an indented function body.
        self.match(TokenType.INDENT)

        body = []

        while not self.check(TokenType.RBRACE):
            if self.is_at_end():
                token = self.peek()
                raise SyntaxError(
                    f"Expected '}}' to close function "
                    f"at line {token.line}, column {token.column}"
                )

            if self.match(TokenType.NEWLINE):
                continue

            if self.match(TokenType.DEDENT):
                # The function body's indentation has ended.
                # Its closing brace should follow.
                if self.check(TokenType.RBRACE):
                    break
                continue

            body.append(self.statement())

        self.consume(
            TokenType.RBRACE,
            "Expected '}' after function body",
        )

        return FunctionDeclaration(name, parameters, body)

    def return_statement(self):
        self.consume(TokenType.RETURN, "Expected 'return'")

        # Allow return without a value.
        if (
            self.check(TokenType.NEWLINE)
            or self.check(TokenType.DEDENT)
            or self.check(TokenType.RBRACE)
            or self.check(TokenType.EOF)
        ):
            self.consume_line_end()
            return ReturnStatement()

        value = self.expression()
        self.consume_line_end()

        return ReturnStatement(value)

    # -------------------------
    # ASSIGNMENT
    # -------------------------

    def assignment(self):
        name = self.advance().value

        self.consume(
            TokenType.ASSIGN,
            "Expected '=' after variable name",
        )

        value = self.expression()
        self.consume_line_end()

        return Assignment(name, value)

    # -------------------------
    # OUTPUT
    # -------------------------

    def show_statement(self):
        self.advance()

        self.consume(
            TokenType.LPAREN,
            "Expected '(' after show",
        )

        value = self.expression()

        self.consume(
            TokenType.RPAREN,
            "Expected ')' after show argument",
        )

        self.consume_line_end()

        return ShowStatement(value)

    # -------------------------
    # INDENTED BLOCKS
    # -------------------------

    def parse_indented_block(self, message):
        self.consume(
            TokenType.COLON,
            "Expected ':' after condition",
        )

        self.consume(
            TokenType.NEWLINE,
            "Expected newline after ':'",
        )

        self.consume(
            TokenType.INDENT,
            message,
        )

        statements = self.block_statements()

        self.consume(
            TokenType.DEDENT,
            "Expected end of indented block",
        )

        return statements

    def block_statements(self):
        statements = []

        while (
            not self.check(TokenType.DEDENT)
            and not self.is_at_end()
        ):
            if self.match(TokenType.NEWLINE):
                continue

            statements.append(self.statement())

        return statements

    def skip_newlines(self):
        while self.match(TokenType.NEWLINE):
            pass

    # -------------------------
    # IF / ELIF / ELSE
    # -------------------------

    def if_statement(self):
        self.consume(TokenType.IF, "Expected 'if'")

        condition = self.expression()

        then_branch = self.parse_indented_block(
            "Expected an indented if block"
        )

        elif_branches = []
        else_branch = []

        self.skip_newlines()

        while self.match(TokenType.ELIF):
            elif_condition = self.expression()

            elif_statements = self.parse_indented_block(
                "Expected an indented elif block"
            )

            elif_branches.append(
                ElifBranch(elif_condition, elif_statements)
            )

            self.skip_newlines()

        if self.match(TokenType.ELSE):
            self.consume(
                TokenType.COLON,
                "Expected ':' after else",
            )

            self.consume(
                TokenType.NEWLINE,
                "Expected newline after else:",
            )

            self.consume(
                TokenType.INDENT,
                "Expected an indented else block",
            )

            else_branch = self.block_statements()

            self.consume(
                TokenType.DEDENT,
                "Expected end of else block",
            )

        return IfStatement(
            condition,
            then_branch,
            else_branch,
            elif_branches,
        )

    # -------------------------
    # FOR LOOP
    # -------------------------

    def for_statement(self):
        self.consume(TokenType.FOR, "Expected 'for'")

        variable = self.consume(
            TokenType.IDENTIFIER,
            "Expected a loop variable after 'for'",
        ).value

        self.consume(
            TokenType.IN,
            "Expected 'in' after loop variable",
        )

        start = self.expression()

        self.consume(
            TokenType.RANGE,
            "Expected '..' between range boundaries",
        )

        end = self.expression()

        body = self.parse_indented_block(
            "Expected an indented for-loop block"
        )

        return ForStatement(variable, start, end, body)

    # -------------------------
    # WHILE LOOP
    # -------------------------

    def while_statement(self):
        self.consume(TokenType.WHILE, "Expected 'while'")

        condition = self.expression()

        body = self.parse_indented_block(
            "Expected an indented while-loop block"
        )

        return WhileStatement(condition, body)

    # -------------------------
    # EXPRESSIONS
    # -------------------------

    def expression(self):
        return self.logical_or()

    def logical_or(self):
        expression = self.logical_and()

        while self.match(TokenType.OR):
            operator = self.previous().value
            right = self.logical_and()

            expression = BinaryExpression(
                expression, operator, right
            )

        return expression

    def logical_and(self):
        expression = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous().value
            right = self.equality()

            expression = BinaryExpression(
                expression, operator, right
            )

        return expression

    def equality(self):
        expression = self.comparison()

        while self.match(
            TokenType.EQUAL_EQUAL,
            TokenType.BANG_EQUAL,
        ):
            operator = self.previous().value
            right = self.comparison()

            expression = BinaryExpression(
                expression, operator, right
            )

        return expression

    def comparison(self):
        expression = self.term()

        while self.match(
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        ):
            operator = self.previous().value
            right = self.term()

            expression = BinaryExpression(
                expression, operator, right
            )

        return expression

    def term(self):
        expression = self.factor()

        while self.match(
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            operator = self.previous().value
            right = self.factor()

            expression = BinaryExpression(
                expression, operator, right
            )

        return expression

    def factor(self):
        expression = self.unary()

        while self.match(
            TokenType.STAR,
            TokenType.SLASH,
        ):
            operator = self.previous().value
            right = self.unary()

            expression = BinaryExpression(
                expression, operator, right
            )

        return expression

    def unary(self):
        if self.match(
            TokenType.NOT,
            TokenType.MINUS,
        ):
            operator = self.previous().value
            operand = self.unary()

            return UnaryExpression(operator, operand)

        return self.primary()

    def primary(self):
        if self.match(
            TokenType.NUMBER,
            TokenType.STRING,
        ):
            return Literal(self.previous().value)

        if self.match(TokenType.TRUE):
            return Literal(True)

        if self.match(TokenType.FALSE):
            return Literal(False)

        if self.match(TokenType.IDENTIFIER):
            callee = Variable(self.previous().value)

            # Parse function calls, including nested calls.
            if self.match(TokenType.LPAREN):
                return self.finish_call(callee)

            return callee

        if self.match(TokenType.LPAREN):
            expression = self.expression()

            self.consume(
                TokenType.RPAREN,
                "Expected ')' after expression",
            )

            return expression

        token = self.peek()

        raise SyntaxError(
            f"Expected an expression at line {token.line}, "
            f"column {token.column}"
        )

    def finish_call(self, callee):
        arguments = []

        if not self.check(TokenType.RPAREN):
            while True:
                arguments.append(self.expression())

                if not self.match(TokenType.COMMA):
                    break

        self.consume(
            TokenType.RPAREN,
            "Expected ')' after function arguments",
        )

        return FunctionCall(callee, arguments)

    # -------------------------
    # TOKEN HELPERS
    # -------------------------

    def consume_line_end(self):
        if self.match(TokenType.NEWLINE):
            return

        if (
            self.check(TokenType.EOF)
            or self.check(TokenType.DEDENT)
            or self.check(TokenType.RBRACE)
        ):
            return

        token = self.peek()

        raise SyntaxError(
            f"Expected end of line at line {token.line}, "
            f"column {token.column}"
        )

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()

        token = self.peek()

        raise SyntaxError(
            f"{message} at line {token.line}, "
            f"column {token.column}"
        )

    def match(self, *token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def check(self, token_type):
        if self.is_at_end():
            return token_type == TokenType.EOF

        return self.peek().type == token_type

    def check_next(self, token_type):
        if self.current + 1 >= len(self.tokens):
            return False

        return self.tokens[self.current + 1].type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
