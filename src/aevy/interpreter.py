from .ast_nodes import (
    Program, Literal, Variable, BinaryExpression, UnaryExpression,
    Assignment, AttributeAccess, AttributeAssignment, ShowStatement,
    ExpressionStatement, IfStatement, ForStatement, WhileStatement,
    BreakStatement, ContinueStatement, FunctionDeclaration,
    ClassDeclaration, FunctionCall, ReturnStatement,
)
class BreakSignal(Exception):
    pass
class ContinueSignal(Exception):
    pass
class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value
class AevyClass:
    def __init__(self, name, methods, parent=None):
        self.name = name
        self.methods = {method.name: method for method in methods}
        self.parent = parent
    def find_method(self, name):
        """Look for a method on this class, then walk up its parent chain."""
        if name in self.methods:
            return self.methods[name]
        if self.parent is not None:
            return self.parent.find_method(name)
        return None
    def find_method_owner(self, name):
        """Return the class that defines the first matching method."""
        if name in self.methods:
            return self
        if self.parent is not None:
            return self.parent.find_method_owner(name)
        return None
    def __repr__(self):
        return f"<class {self.name}>"
class AevyInstance:
    def __init__(self, klass):
        self.klass = klass
        self.attributes = {}
    def __repr__(self):
        return f"<{self.klass.name} instance>"
class BoundMethod:
    def __init__(self, instance, declaration, owner=None):
        self.instance = instance
        self.declaration = declaration
        self.owner = owner
class SuperProxy:
    """Represents the parent-class view available inside an instance method."""
    def __init__(self, instance, parent_class):
        self.instance = instance
        self.parent_class = parent_class
class Interpreter:
    def __init__(self):
        self.environment = {}
        self.global_environment = self.environment
        self.functions = {}
        self.classes = {}
        self.loop_depth = 0
        self.function_depth = 0
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
            self.environment[statement.name] = self.evaluate(statement.value)
        elif isinstance(statement, AttributeAssignment):
            instance = self.evaluate(statement.object_expression)
            if not isinstance(instance, AevyInstance):
                raise TypeError("Only objects can have attributes assigned")
            instance.attributes[statement.name] = self.evaluate(statement.value)
        elif isinstance(statement, ShowStatement):
            print(self.evaluate(statement.value))
        elif isinstance(statement, ExpressionStatement):
            self.evaluate(statement.expression)
        elif isinstance(statement, FunctionDeclaration):
            self.functions[statement.name] = statement
        elif isinstance(statement, ClassDeclaration):
            if statement.name in self.classes:
                raise RuntimeError(f"Class '{statement.name}' is already defined")
            parent = None
            if statement.parent_name is not None:
                if statement.parent_name == statement.name:
                    raise RuntimeError("A class cannot inherit from itself")
                parent = self.classes.get(statement.parent_name)
                if parent is None:
                    raise NameError(
                        f"Undefined parent class '{statement.parent_name}'"
                    )
            self.classes[statement.name] = AevyClass(
                statement.name, statement.methods, parent
            )
        elif isinstance(statement, ReturnStatement):
            if self.function_depth == 0:
                raise RuntimeError("'return' can only be used inside a function")
            value = None if statement.value is None else self.evaluate(statement.value)
            raise ReturnSignal(value)
        elif isinstance(statement, BreakStatement):
            if self.loop_depth == 0:
                raise RuntimeError("'break' can only be used inside a loop")
            raise BreakSignal()
        elif isinstance(statement, ContinueStatement):
            if self.loop_depth == 0:
                raise RuntimeError("'continue' can only be used inside a loop")
            raise ContinueSignal()
        elif isinstance(statement, IfStatement):
            condition = self.evaluate(statement.condition)
            if not isinstance(condition, bool):
                raise TypeError("An if condition must evaluate to True or False")
            if condition:
                self.execute_block(statement.then_branch)
                return
            for branch in statement.elif_branches:
                result = self.evaluate(branch.condition)
                if not isinstance(result, bool):
                    raise TypeError("An elif condition must evaluate to True or False")
                if result:
                    self.execute_block(branch.statements)
                    return
            self.execute_block(statement.else_branch)
        elif isinstance(statement, ForStatement):
            start = self.evaluate(statement.start)
            end = self.evaluate(statement.end)
            if (
                isinstance(start, bool) or not isinstance(start, int)
                or isinstance(end, bool) or not isinstance(end, int)
            ):
                raise TypeError("For-loop range boundaries must be integers")
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
                        raise TypeError("A while condition must evaluate to True or False")
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
            raise RuntimeError(f"Unknown statement: {type(statement).__name__}")
    def call_function_declaration(self, function, values, instance=None, method_owner=None):
        expected = len(function.parameters)
        if len(values) != expected:
            raise TypeError(
                f"Function '{function.name}' expects {expected} argument(s), "
                f"but received {len(values)}"
            )
        local_environment = dict(zip(function.parameters, values))
        if instance is not None:
            local_environment["self"] = instance
            # "super" starts at the parent of the class that defines this method.
            parent_class = method_owner.parent if method_owner is not None else instance.klass.parent
            if parent_class is not None:
                local_environment["super"] = SuperProxy(instance, parent_class)
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
        return None
    def call_function(self, expression):
        if isinstance(expression.callee, Variable):
            name = expression.callee.name
            values = [self.evaluate(argument) for argument in expression.arguments]
            if name in self.classes:
                if name not in self.classes:
                    raise NameError(f"Undefined class '{name}'")
                klass = self.classes[name]
                instance = AevyInstance(klass)
                initializer = klass.find_method("init")
                if initializer is not None:
                    self.call_function_declaration(initializer, values, instance)
                elif values:
                    raise TypeError(
                        f"Class '{name}' has no init method and accepts no arguments"
                    )
                return instance
            if name not in self.functions:
                raise NameError(f"Undefined function or class '{name}'")
            return self.call_function_declaration(self.functions[name], values)
        if isinstance(expression.callee, AttributeAccess):
            receiver = self.evaluate(expression.callee.object_expression)
            method_name = expression.callee.name
            values = [self.evaluate(argument) for argument in expression.arguments]

            if isinstance(receiver, SuperProxy):
                parent = receiver.parent_class
                method = parent.find_method(method_name)
                if method is None:
                    raise NameError(
                        f"Parent class '{parent.name}' has no method '{method_name}'"
                    )
                owner = parent.find_method_owner(method_name)
                return self.call_function_declaration(
                    method, values, receiver.instance, owner
                )

            if not isinstance(receiver, AevyInstance):
                raise TypeError("Methods can only be called on objects")
            method = receiver.klass.find_method(method_name)
            if method is None:
                raise NameError(
                    f"Class '{receiver.klass.name}' has no method '{method_name}'"
                )
            owner = receiver.klass.find_method_owner(method_name)
            return self.call_function_declaration(method, values, receiver, owner)
        raise RuntimeError("Only named functions and object methods can be called")
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
        if isinstance(expression, AttributeAccess):
            instance = self.evaluate(expression.object_expression)
            if not isinstance(instance, AevyInstance):
                raise TypeError("Only objects have accessible attributes")
            if expression.name in instance.attributes:
                return instance.attributes[expression.name]
            method = instance.klass.find_method(expression.name)
            if method is not None:
                return BoundMethod(instance, method, instance.klass.find_method_owner(expression.name))
            raise NameError(
                f"Object of class '{instance.klass.name}' has no attribute "
                f"'{expression.name}'"
            )
        if isinstance(expression, FunctionCall):
            return self.call_function(expression)
        if isinstance(expression, UnaryExpression):
            right = self.evaluate(expression.operand)
            if expression.operator == "-":
                if isinstance(right, bool) or not isinstance(right, (int, float)):
                    raise TypeError("Unary '-' requires a number")
                return -right
            if expression.operator == "not":
                if not isinstance(right, bool):
                    raise TypeError("'not' requires a boolean")
                return not right
            raise RuntimeError(f"Unknown unary operator: {expression.operator}")
        if isinstance(expression, BinaryExpression):
            operator = expression.operator
            if operator == "or":
                left = self.evaluate(expression.left)
                if not isinstance(left, bool):
                    raise TypeError("'or' requires boolean operands")
                if left:
                    return True
                right = self.evaluate(expression.right)
                if not isinstance(right, bool):
                    raise TypeError("'or' requires boolean operands")
                return right
            if operator == "and":
                left = self.evaluate(expression.left)
                if not isinstance(left, bool):
                    raise TypeError("'and' requires boolean operands")
                if not left:
                    return False
                right = self.evaluate(expression.right)
                if not isinstance(right, bool):
                    raise TypeError("'and' requires boolean operands")
                return right
            left = self.evaluate(expression.left)
            right = self.evaluate(expression.right)
            if operator == "+": return left + right
            if operator == "-": return left - right
            if operator == "*": return left * right
            if operator == "/": return left / right
            if operator == "==": return left == right
            if operator == "!=": return left != right
            if operator == "<": return left < right
            if operator == "<=": return left <= right
            if operator == ">": return left > right
            if operator == ">=": return left >= right
            raise RuntimeError(f"Unknown binary operator: {operator}")
        raise RuntimeError(f"Unsupported expression: {type(expression).__name__}")
