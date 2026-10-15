from .token import TokenType
from .ast_nodes import (
    Program, Literal, Variable, BinaryExpression, UnaryExpression,
    Assignment, AttributeAccess, AttributeAssignment, ListLiteral, DictLiteral,
    IndexAccess, IndexAssignment, ShowStatement,
    ExpressionStatement, IfStatement, ElifBranch, ForStatement,
    WhileStatement, BreakStatement, ContinueStatement,
    FunctionDeclaration, ClassDeclaration, FunctionCall, ReturnStatement,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            if self.match(TokenType.NEWLINE, TokenType.DEDENT):
                continue
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
        token = self.peek()
        node = self._statement()
        return self.locate(node, token)

    def _statement(self):
        if self.check(TokenType.CLASS):
            return self.class_declaration()
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
        if self.check(TokenType.IDENTIFIER) and self.peek().value == "show":
            return self.show_statement()

        if self.check(TokenType.IDENTIFIER) and self.check_next(TokenType.ASSIGN):
            return self.assignment()

        if self.check(TokenType.IDENTIFIER) and self.check_next(TokenType.LBRACKET):
            close_index = self.current + 2
            depth = 1
            while close_index < len(self.tokens) and depth:
                if self.tokens[close_index].type == TokenType.LBRACKET:
                    depth += 1
                elif self.tokens[close_index].type == TokenType.RBRACKET:
                    depth -= 1
                close_index += 1
            if depth == 0 and close_index < len(self.tokens) and self.tokens[close_index].type == TokenType.ASSIGN:
                return self.index_assignment()

        if (
            self.check(TokenType.IDENTIFIER)
            and self.check_next(TokenType.DOT)
            and self.check_nth(3, TokenType.IDENTIFIER)
            and self.check_nth(4, TokenType.ASSIGN)
        ):
            return self.attribute_assignment()

        expression = self.expression()
        self.consume_line_end()
        return ExpressionStatement(expression)

    # CLASS / FUNCTION DECLARATIONS

    def class_declaration(self):
        self.consume(TokenType.CLASS, "Expected 'class'")
        name = self.consume(TokenType.IDENTIFIER, "Expected a class name").value
        parent_name = None
        if self.match(TokenType.EXTENDS):
            parent_name = self.consume(
                TokenType.IDENTIFIER, "Expected a parent class name after 'extends'"
            ).value
        self.consume(TokenType.LBRACE, "Expected '{' after class declaration")
        self.skip_newlines()
        self.match(TokenType.INDENT)

        methods = []
        while not self.check(TokenType.RBRACE):
            if self.is_at_end():
                token = self.peek()
                raise SyntaxError(
                    f"Expected '}}' to close class at line {token.line}, "
                    f"column {token.column}"
                )
            if self.match(TokenType.NEWLINE, TokenType.DEDENT):
                continue
            if not self.check(TokenType.FUNC):
                token = self.peek()
                raise SyntaxError(
                    f"Only methods are supported inside classes "
                    f"(line {token.line}, column {token.column})"
                )
            methods.append(self.function_declaration())

        self.consume(TokenType.RBRACE, "Expected '}' after class body")
        return ClassDeclaration(name, methods, parent_name)

    def function_declaration(self):
        self.consume(TokenType.FUNC, "Expected 'func'")
        name = self.consume(TokenType.IDENTIFIER, "Expected a function name").value
        self.consume(TokenType.LPAREN, "Expected '(' after function name")

        parameters = []
        if not self.check(TokenType.RPAREN):
            while True:
                parameter = self.consume(
                    TokenType.IDENTIFIER, "Expected a parameter name"
                ).value
                if parameter in parameters:
                    token = self.previous()
                    raise SyntaxError(
                        f"Duplicate parameter '{parameter}' at line "
                        f"{token.line}, column {token.column}"
                    )
                parameters.append(parameter)
                if not self.match(TokenType.COMMA):
                    break

        self.consume(TokenType.RPAREN, "Expected ')' after parameters")
        self.consume(TokenType.LBRACE, "Expected '{' before function body")
        self.skip_newlines()
        self.match(TokenType.INDENT)

        body = []
        while not self.check(TokenType.RBRACE):
            if self.is_at_end():
                token = self.peek()
                raise SyntaxError(
                    f"Expected '}}' to close function at line {token.line}, "
                    f"column {token.column}"
                )
            if self.match(TokenType.NEWLINE):
                continue
            if self.match(TokenType.DEDENT):
                if self.check(TokenType.RBRACE):
                    break
                continue
            body.append(self.statement())

        self.consume(TokenType.RBRACE, "Expected '}' after function body")
        return FunctionDeclaration(name, parameters, body)

    def return_statement(self):
        self.consume(TokenType.RETURN, "Expected 'return'")
        if (
            self.check(TokenType.NEWLINE) or self.check(TokenType.DEDENT)
            or self.check(TokenType.RBRACE) or self.check(TokenType.EOF)
        ):
            self.consume_line_end()
            return ReturnStatement()
        value = self.expression()
        self.consume_line_end()
        return ReturnStatement(value)

    # ASSIGNMENT / OUTPUT

    def assignment(self):
        name = self.advance().value
        self.consume(TokenType.ASSIGN, "Expected '=' after variable name")
        value = self.expression()
        self.consume_line_end()
        return Assignment(name, value)

    def index_assignment(self):
        name_token = self.consume(TokenType.IDENTIFIER, "Expected list name")
        self.consume(TokenType.LBRACKET, "Expected '[' after list name")
        index = self.expression()
        self.consume(TokenType.RBRACKET, "Expected ']' after index")
        self.consume(TokenType.ASSIGN, "Expected '=' after list index")
        value = self.expression()
        self.consume_line_end()
        return self.locate(IndexAssignment(self.locate(Variable(name_token.value), name_token), index, value), name_token)

    def attribute_assignment(self):
        object_name = self.consume(TokenType.IDENTIFIER, "Expected object name").value
        self.consume(TokenType.DOT, "Expected '.'")
        attribute_name = self.consume(
            TokenType.IDENTIFIER, "Expected an attribute name"
        ).value
        self.consume(TokenType.ASSIGN, "Expected '=' after attribute name")
        value = self.expression()
        self.consume_line_end()
        return AttributeAssignment(Variable(object_name), attribute_name, value)

    def show_statement(self):
        self.advance()
        self.consume(TokenType.LPAREN, "Expected '(' after show")
        value = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after show argument")
        self.consume_line_end()
        return ShowStatement(value)

    # INDENTED BLOCKS

    def parse_indented_block(self, message):
        self.consume(TokenType.COLON, "Expected ':' after condition")
        self.consume(TokenType.NEWLINE, "Expected newline after ':'")
        self.consume(TokenType.INDENT, message)
        statements = self.block_statements()
        self.consume(TokenType.DEDENT, "Expected end of indented block")
        return statements

    def block_statements(self):
        statements = []
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            if self.match(TokenType.NEWLINE):
                continue
            statements.append(self.statement())
        return statements

    def skip_newlines(self):
        while self.match(TokenType.NEWLINE):
            pass

    # CONDITIONALS / LOOPS

    def if_statement(self):
        self.consume(TokenType.IF, "Expected 'if'")
        condition = self.expression()
        then_branch = self.parse_indented_block("Expected an indented if block")
        elif_branches = []
        else_branch = []
        self.skip_newlines()

        while self.match(TokenType.ELIF):
            elif_condition = self.expression()
            elif_statements = self.parse_indented_block(
                "Expected an indented elif block"
            )
            elif_branches.append(ElifBranch(elif_condition, elif_statements))
            self.skip_newlines()

        if self.match(TokenType.ELSE):
            self.consume(TokenType.COLON, "Expected ':' after else")
            self.consume(TokenType.NEWLINE, "Expected newline after else:")
            self.consume(TokenType.INDENT, "Expected an indented else block")
            else_branch = self.block_statements()
            self.consume(TokenType.DEDENT, "Expected end of else block")

        return IfStatement(condition, then_branch, else_branch, elif_branches)

    def for_statement(self):
        self.consume(TokenType.FOR, "Expected 'for'")
        variable = self.consume(
            TokenType.IDENTIFIER, "Expected a loop variable after 'for'"
        ).value
        self.consume(TokenType.IN, "Expected 'in' after loop variable")
        start = self.expression()
        if self.match(TokenType.RANGE):
            end = self.expression()
            iterable = None
        else:
            end = None
            iterable = start
        body = self.parse_indented_block("Expected an indented for-loop block")
        return ForStatement(variable, start, end, body, iterable)

    def while_statement(self):
        self.consume(TokenType.WHILE, "Expected 'while'")
        condition = self.expression()
        body = self.parse_indented_block("Expected an indented while-loop block")
        return WhileStatement(condition, body)

    # EXPRESSIONS

    def expression(self):
        return self.logical_or()

    @staticmethod
    def locate(node, token):
        # AST nodes intentionally keep source positions as metadata so their
        # existing constructors and public API remain backward compatible.
        node.line = token.line
        node.column = token.column
        return node

    def logical_or(self):
        expression = self.logical_and()
        while self.match(TokenType.OR):
            operator_token = self.previous()
            expression = self.locate(
                BinaryExpression(expression, operator_token.value, self.logical_and()),
                operator_token,
            )
        return expression

    def logical_and(self):
        expression = self.equality()
        while self.match(TokenType.AND):
            operator_token = self.previous()
            expression = self.locate(
                BinaryExpression(expression, operator_token.value, self.equality()),
                operator_token,
            )
        return expression

    def equality(self):
        expression = self.comparison()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL, TokenType.IN):
            operator_token = self.previous()
            expression = self.locate(
                BinaryExpression(expression, "in" if operator_token.type == TokenType.IN else operator_token.value, self.comparison()),
                operator_token,
            )
        return expression

    def comparison(self):
        expression = self.term()
        while self.match(
            TokenType.LESS, TokenType.LESS_EQUAL,
            TokenType.GREATER, TokenType.GREATER_EQUAL,
        ):
            operator_token = self.previous()
            expression = self.locate(
                BinaryExpression(expression, operator_token.value, self.term()),
                operator_token,
            )
        return expression

    def term(self):
        expression = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator_token = self.previous()
            expression = self.locate(
                BinaryExpression(expression, operator_token.value, self.factor()),
                operator_token,
            )
        return expression

    def factor(self):
        expression = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            operator_token = self.previous()
            expression = self.locate(
                BinaryExpression(expression, operator_token.value, self.unary()),
                operator_token,
            )
        return expression

    def unary(self):
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator_token = self.previous()
            return self.locate(
                UnaryExpression(operator_token.value, self.unary()), operator_token
            )
        return self.primary()

    def primary(self):
        if self.match(TokenType.NUMBER, TokenType.STRING):
            token = self.previous()
            return self.locate(Literal(token.value), token)
        if self.match(TokenType.TRUE):
            token = self.previous()
            return self.locate(Literal(True), token)
        if self.match(TokenType.FALSE):
            token = self.previous()
            return self.locate(Literal(False), token)

        if self.match(TokenType.IDENTIFIER):
            token = self.previous()
            expression = self.locate(Variable(token.value), token)
            return self.finish_postfix(expression)

        if self.match(TokenType.LBRACE):
            token = self.previous()
            entries = []
            if not self.check(TokenType.RBRACE):
                while True:
                    key = self.expression()
                    self.consume(TokenType.COLON, "Expected ':' between dictionary key and value")
                    value = self.expression()
                    entries.append((key, value))
                    if not self.match(TokenType.COMMA):
                        break
                    if self.check(TokenType.RBRACE):
                        break
            self.consume(TokenType.RBRACE, "Expected '}' after dictionary entries")
            return self.finish_postfix(self.locate(DictLiteral(entries), token))

        if self.match(TokenType.LBRACKET):
            token = self.previous()
            elements = []
            if not self.check(TokenType.RBRACKET):
                while True:
                    elements.append(self.expression())
                    if not self.match(TokenType.COMMA):
                        break
            self.consume(TokenType.RBRACKET, "Expected ']' after list elements")
            return self.finish_postfix(self.locate(ListLiteral(elements), token))

        if self.match(TokenType.LPAREN):
            token = self.previous()
            expression = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            if not hasattr(expression, "line"):
                self.locate(expression, token)
            return self.finish_postfix(expression)

        token = self.peek()
        raise SyntaxError(
            f"Expected an expression at line {token.line}, column {token.column}"
        )

    def finish_postfix(self, expression):
        # Allows calls and property access, including object.method(...)
        while True:
            if self.match(TokenType.LPAREN):
                token = self.previous()
                expression = self.locate(self.finish_call(expression), token)
            elif self.match(TokenType.LBRACKET):
                token = self.previous()
                index = self.expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after index")
                expression = self.locate(IndexAccess(expression, index), token)
            elif self.match(TokenType.DOT):
                token = self.previous()
                name = self.consume(
                    TokenType.IDENTIFIER, "Expected a property or method name"
                ).value
                expression = self.locate(AttributeAccess(expression, name), token)
            else:
                break
        return expression

    def finish_call(self, callee):
        arguments = []
        if not self.check(TokenType.RPAREN):
            while True:
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RPAREN, "Expected ')' after function arguments")
        return FunctionCall(callee, arguments)

    # TOKEN HELPERS

    def consume_line_end(self):
        if self.match(TokenType.NEWLINE):
            return
        if (
            self.check(TokenType.EOF) or self.check(TokenType.DEDENT)
            or self.check(TokenType.RBRACE)
        ):
            return
        token = self.peek()
        raise SyntaxError(
            f"Expected end of line at line {token.line}, column {token.column}"
        )

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        token = self.peek()
        raise SyntaxError(
            f"{message} at line {token.line}, column {token.column}"
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
        return (
            self.current + 1 < len(self.tokens)
            and self.tokens[self.current + 1].type == token_type
        )

    def check_nth(self, offset, token_type):
        index = self.current + offset - 1
        return index < len(self.tokens) and self.tokens[index].type == token_type

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
