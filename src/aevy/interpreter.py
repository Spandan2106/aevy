
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
    ForStatement,
    WhileStatement,
    BreakStatement,
    ContinueStatement,
    FunctionDeclaration,
    FunctionCall,
    ReturnStatement,
)


class BreakSignal(Exception):
    pass


class ContinueSignal(Exception):
    pass


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self):
        self.environment = {}
        self.global_environment = self.environment
        self.functions = {}
        self.loop_depth = 0
        self.function_depth = 0

    # -------------------------
    # PROGRAM EXECUTION
    # -------------------------

    def interpret(self, program):
        if not isinstance(program, Program):
            raise TypeError("Expected a Program AST node")

        for statement in program.statements:
            self.execute(statement)

    def execute_block(self, statements):
        for statement in statements:
            self.execute(statement)

    def execute(self, statement):
        if isinstance(statement, Assignment):
            value = self.evaluate(statement.value)
            self.environment[statement.name] = value

        elif isinstance(statement, ShowStatement):
            print(self.evaluate(statement.value))

        elif isinstance(statement, ExpressionStatement):
            self.evaluate(statement.expression)

        elif isinstance(statement, FunctionDeclaration):
            self.functions[statement.name] = statement

        elif isinstance(statement, ReturnStatement):
            if self.function_depth == 0:
                raise RuntimeError(
                    "'return' can only be used inside a function"
                )

            value = (
                None
                if statement.value is None
                else self.evaluate(statement.value)
            )

            raise ReturnSignal(value)

        elif isinstance(statement, BreakStatement):
            if self.loop_depth == 0:
                raise RuntimeError(
                    "'break' can only be used inside a loop"
                )

            raise BreakSignal()

        elif isinstance(statement, ContinueStatement):
            if self.loop_depth == 0:
                raise RuntimeError(
                    "'continue' can only be used inside a loop"
                )

            raise ContinueSignal()

        elif isinstance(statement, IfStatement):
            condition = self.evaluate(statement.condition)

            if not isinstance(condition, bool):
                raise TypeError(
                    "An if condition must evaluate to True or False"
                )

            if condition:
                self.execute_block(statement.then_branch)
                return

            for branch in statement.elif_branches:
                result = self.evaluate(branch.condition)

                if not isinstance(result, bool):
                    raise TypeError(
                        "An elif condition must evaluate to True or False"
                    )

                if result:
                    self.execute_block(branch.statements)
                    return

            self.execute_block(statement.else_branch)

        elif isinstance(statement, ForStatement):
            start = self.evaluate(statement.start)
            end = self.evaluate(statement.end)

            if (
                isinstance(start, bool)
                or not isinstance(start, int)
                or isinstance(end, bool)
                or not isinstance(end, int)
            ):
                raise TypeError(
                    "For-loop range boundaries must be integers"
                )

            existed = statement.variable in self.environment
            old_value = self.environment.get(statement.variable)

            self.loop_depth += 1

            try:
                for value in range(start, end):
                    self.environment[statement.variable] = value

                    try:
                        self.execute_block(statement.body)
                    except ContinueSignal:
                        continue
                    except BreakSignal:
                        break

            finally:
                self.loop_depth -= 1

                if existed:
                    self.environment[statement.variable] = old_value
                else:
                    self.environment.pop(statement.variable, None)

        elif isinstance(statement, WhileStatement):
            self.loop_depth += 1

            try:
                while True:
                    condition = self.evaluate(statement.condition)

                    if not isinstance(condition, bool):
                        raise TypeError(
                            "A while condition must evaluate to True or False"
                        )

                    if not condition:
                        break

                    try:
                        self.execute_block(statement.body)
                    except ContinueSignal:
                        continue
                    except BreakSignal:
                        break

            finally:
                self.loop_depth -= 1

        else:
            raise RuntimeError(
                f"Unknown statement: {type(statement).__name__}"
            )

    # -------------------------
    # FUNCTION CALLS
    # -------------------------

    def call_function(self, expression):
        if not isinstance(expression.callee, Variable):
            raise RuntimeError(
                "Only named functions can be called"
            )

        name = expression.callee.name

        if name not in self.functions:
            raise NameError(f"Undefined function '{name}'")

        function = self.functions[name]

        if len(expression.arguments) != len(function.parameters):
            raise TypeError(
                f"Function '{name}' expects "
                f"{len(function.parameters)} argument(s), "
                f"but received {len(expression.arguments)}"
            )

        # Evaluate arguments in the caller's environment first.
        values = [
            self.evaluate(argument)
            for argument in expression.arguments
        ]

        # Each call gets a fresh local environment.
        local_environment = dict(zip(function.parameters, values))

        previous_environment = self.environment
        previous_loop_depth = self.loop_depth

        self.environment = local_environment
        self.loop_depth = 0
        self.function_depth += 1

        try:
            self.execute_block(function.body)
        except ReturnSignal as signal:
            return signal.value
        finally:
            self.environment = previous_environment
            self.loop_depth = previous_loop_depth
            self.function_depth -= 1

        # A function without an explicit return yields None.
        return None

    # -------------------------
    # EXPRESSION EVALUATION
    # -------------------------

    def evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value

        if isinstance(expression, Variable):
            name = expression.name

            if name in self.environment:
                return self.environment[name]

            if name in self.global_environment:
                return self.global_environment[name]

            raise NameError(f"Undefined variable '{name}'")

        if isinstance(expression, FunctionCall):
            return self.call_function(expression)

        if isinstance(expression, UnaryExpression):
            right = self.evaluate(expression.operand)

            if expression.operator == "-":
                if isinstance(right, bool) or not isinstance(
                    right, (int, float)
                ):
                    raise TypeError("Unary '-' requires a number")

                return -right

            if expression.operator == "not":
                if not isinstance(right, bool):
                    raise TypeError("'not' requires a boolean")

                return not right

            raise RuntimeError(
                f"Unknown unary operator: {expression.operator}"
            )

        if isinstance(expression, BinaryExpression):
            operator = expression.operator

            # Short-circuit OR.
            if operator == "or":
                left = self.evaluate(expression.left)

                if not isinstance(left, bool):
                    raise TypeError(
                        "'or' requires boolean operands"
                    )

                if left:
                    return True

                right = self.evaluate(expression.right)

                if not isinstance(right, bool):
                    raise TypeError(
                        "'or' requires boolean operands"
                    )

                return right

            # Short-circuit AND.
            if operator == "and":
                left = self.evaluate(expression.left)

                if not isinstance(left, bool):
                    raise TypeError(
                        "'and' requires boolean operands"
                    )

                if not left:
                    return False

                right = self.evaluate(expression.right)

                if not isinstance(right, bool):
                    raise TypeError(
                        "'and' requires boolean operands"
                    )

                return right

            left = self.evaluate(expression.left)
            right = self.evaluate(expression.right)

            if operator == "+":
                return left + right

            if operator == "-":
                return left - right

            if operator == "*":
                return left * right

            if operator == "/":
                return left / right

            if operator == "==":
                return left == right

            if operator == "!=":
                return left != right

            if operator == "<":
                return left < right

            if operator == "<=":
                return left <= right

            if operator == ">":
                return left > right

            if operator == ">=":
                return left >= right

            raise RuntimeError(
                f"Unknown binary operator: {operator}"
            )

        raise RuntimeError(
            f"Unsupported expression: {type(expression).__name__}"
        )
