from .ast_nodes import (
    Program, Literal, Variable, BinaryExpression, UnaryExpression,
    Assignment, AttributeAccess, AttributeAssignment, ListLiteral,
    IndexAccess, IndexAssignment, ShowStatement,
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
        # Private attributes remember which class declared them.
        self.private_attribute_owners = {}
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
    def __init__(self, source=None, input_func=input):
        self.source = source
        self.input_func = input_func
        self.source_lines = source.splitlines() if source is not None else []
        self.environment = {}
        self.global_environment = self.environment
        self.functions = {}
        self.classes = {}
        self.loop_depth = 0
        self.function_depth = 0
        self.current_method_owner = None
    def interpret(self, program):
        if not isinstance(program, Program):
            raise TypeError("Expected a Program AST node")
        for statement in program.statements:
            self.execute(statement)
    def execute_block(self, statements):
        for statement in statements:
            self.execute(statement)
    def execute(self, statement):
        try:
            return self._execute(statement)
        except Exception as error:
            self._attach_location(error, statement)
            raise

    def _execute(self, statement):
        if isinstance(statement, Assignment):
            self.environment[statement.name] = self.evaluate(statement.value)
        elif isinstance(statement, IndexAssignment):
            target = self.evaluate(statement.object_expression)
            if not isinstance(target, list):
                raise TypeError("Indexed assignment requires a list")
            index = self._list_index(self.evaluate(statement.index), len(target), allow_end=False)
            target[index] = self.evaluate(statement.value)
        elif isinstance(statement, AttributeAssignment):
            instance = self.evaluate(statement.object_expression)
            if not isinstance(instance, AevyInstance):
                raise TypeError("Only objects can have attributes assigned")
            name = statement.name
            is_private = name.startswith("_")
            is_self = (
                isinstance(statement.object_expression, Variable)
                and statement.object_expression.name == "self"
            )
            owner = self.current_method_owner
            if is_private and not (
                is_self and owner is not None
            ):
                raise PermissionError(
                    f"Private attribute '{name}' can only be accessed inside "
                    "a method of its declaring class"
                )
            if is_private:
                existing_owner = instance.private_attribute_owners.get(name)
                if existing_owner is not None and existing_owner is not owner:
                    raise PermissionError(
                        f"Private attribute '{name}' belongs to class "
                        f"'{existing_owner.name}'"
                    )
                instance.private_attribute_owners[name] = owner
            instance.attributes[name] = self.evaluate(statement.value)
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
            if statement.iterable is not None:
                values = self.evaluate(statement.iterable)
                if not isinstance(values, list):
                    raise TypeError("For-loop iteration requires a list")
            else:
                start = self.evaluate(statement.start)
                end = self.evaluate(statement.end)
                if (
                    isinstance(start, bool) or not isinstance(start, int)
                    or isinstance(end, bool) or not isinstance(end, int)
                ):
                    raise TypeError("For-loop range boundaries must be integers")
                values = range(start, end)
            existed = statement.variable in self.environment
            old_value = self.environment.get(statement.variable)
            self.loop_depth += 1
            try:
                for value in values:
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
        previous_method_owner = self.current_method_owner
        self.current_method_owner = method_owner if instance is not None else None
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
            self.current_method_owner = previous_method_owner
            self.function_depth -= 1
        return None
    @staticmethod
    def call_standard_library(name, values):
        """Execute Aevy's small, validated standard-library built-ins."""
        arities = {
            "length": (1, 1), "upper": (1, 1), "lower": (1, 1),
            "trim": (1, 1), "contains": (2, 2), "abs": (1, 1),
            "min": (2, None), "max": (2, None), "round": (1, 2),
            "append": (2, 2), "pop": (1, 1),
            "remove": (2, 2), "insert": (3, 3), "index_of": (2, 2),
            "reverse": (1, 1), "sum": (1, 1), "sort": (1, 1),
        }
        minimum, maximum = arities[name]
        if len(values) < minimum or (maximum is not None and len(values) > maximum):
            if maximum == minimum:
                expected = f"exactly {minimum}"
            elif maximum is None:
                expected = f"at least {minimum}"
            else:
                expected = f"{minimum} or {maximum}"
            raise TypeError(
                f"Built-in '{name}' expects {expected} argument(s), received {len(values)}"
            )

        def require_string(value, position=1):
            if not isinstance(value, str):
                raise TypeError(
                    f"Built-in '{name}' argument {position} must be text"
                )
            return value

        def require_number(value, position=1):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(
                    f"Built-in '{name}' argument {position} must be a number"
                )
            return value

        if name == "length":
            value = values[0]
            if isinstance(value, (str, list)):
                return len(value)
            raise TypeError("Built-in 'length' argument 1 must be text or a list")
        if name == "append":
            target = values[0]
            if not isinstance(target, list):
                raise TypeError("Built-in 'append' argument 1 must be a list")
            target.append(values[1])
            return None
        if name == "pop":
            target = values[0]
            if not isinstance(target, list):
                raise TypeError("Built-in 'pop' argument 1 must be a list")
            if not target:
                raise IndexError("Cannot pop from an empty list")
            return target.pop()
        if name == "remove":
            target = values[0]
            if not isinstance(target, list):
                raise TypeError("Built-in 'remove' argument 1 must be a list")
            try:
                target.remove(values[1])
            except ValueError:
                raise ValueError(f"Value {values[1]!r} was not found in the list") from None
            return None
        if name == "insert":
            target = values[0]
            if not isinstance(target, list):
                raise TypeError("Built-in 'insert' argument 1 must be a list")
            index = values[1]
            if isinstance(index, bool) or not isinstance(index, int):
                raise TypeError("Built-in 'insert' argument 2 must be an integer")
            if index < 0 or index > len(target):
                raise IndexError(f"Insert index {index} is out of range for a list of length {len(target)}")
            target.insert(index, values[2])
            return None
        if name == "index_of":
            target = values[0]
            if not isinstance(target, list):
                raise TypeError("Built-in 'index_of' argument 1 must be a list")
            try:
                return target.index(values[1])
            except ValueError:
                return -1
        if name == "reverse":
            target = values[0]
            if not isinstance(target, list):
                raise TypeError("Built-in 'reverse' argument 1 must be a list")
            target.reverse()
            return target
        if name == "sum":
            target = values[0]
            if not isinstance(target, list):
                raise TypeError("Built-in 'sum' argument 1 must be a list")
            total = 0
            for item in target:
                require_number(item)
                total += item
            return total
        if name == "sort":
            target = values[0]
            if not isinstance(target, list):
                raise TypeError("Built-in 'sort' argument 1 must be a list")
            try:
                return sorted(target)
            except TypeError:
                raise TypeError("Built-in 'sort' requires mutually comparable list elements") from None
        if name == "upper":
            return require_string(values[0]).upper()
        if name == "lower":
            return require_string(values[0]).lower()
        if name == "trim":
            return require_string(values[0]).strip()
        if name == "contains":
            haystack = values[0]
            if isinstance(haystack, str):
                needle = require_string(values[1], 2)
                return needle in haystack
            if isinstance(haystack, list):
                return values[1] in haystack
            raise TypeError("Built-in 'contains' argument 1 must be text or a list")
        if name == "abs":
            return abs(require_number(values[0]))
        if name in {"min", "max"}:
            numbers = [require_number(value, i + 1) for i, value in enumerate(values)]
            return min(numbers) if name == "min" else max(numbers)
        if name == "round":
            number = require_number(values[0], 1)
            digits = 0
            if len(values) == 2:
                digits = values[1]
                if isinstance(digits, bool) or not isinstance(digits, int):
                    raise TypeError("Built-in 'round' argument 2 must be an integer")
            return round(number, digits)
        raise RuntimeError(f"Unknown standard-library function '{name}'")

    def call_function(self, expression):
        if isinstance(expression.callee, Variable):
            name = expression.callee.name
            values = [self.evaluate(argument) for argument in expression.arguments]

            # Built-ins are reserved names and are implemented explicitly so
            # Aevy programs never gain access to Python's global namespace.
            if name in {"length", "upper", "lower", "trim", "contains", "abs", "min", "max", "round", "append", "pop", "remove", "insert", "index_of", "reverse", "sum", "sort"}:
                return self.call_standard_library(name, values)

            # Built-in conversion functions are reserved names.
            if name in {"number", "integer", "decimal", "text", "boolean"}:
                if len(values) != 1:
                    raise TypeError(f"Built-in '{name}' expects exactly 1 argument, received {len(values)}")
                value = values[0]
                try:
                    if name == "number":
                        if isinstance(value, bool):
                            raise ValueError("booleans cannot be converted to numbers")
                        if isinstance(value, (int, float)):
                            return value
                        if not isinstance(value, str):
                            raise ValueError("expected a string or number")
                        cleaned = value.strip()
                        if not cleaned:
                            raise ValueError("cannot convert an empty string to a number")
                        try:
                            return int(cleaned)
                        except ValueError:
                            return float(cleaned)
                    if name == "integer":
                        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
                            raise ValueError("expected a numeric value or numeric string")
                        return int(value.strip()) if isinstance(value, str) else int(value)
                    if name == "decimal":
                        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
                            raise ValueError("expected a numeric value or numeric string")
                        return float(value.strip()) if isinstance(value, str) else float(value)
                    if name == "text":
                        if value is True:
                            return "True"
                        if value is False:
                            return "False"
                        return str(value)
                    if name == "boolean":
                        if isinstance(value, bool):
                            return value
                        if isinstance(value, str):
                            normalized = value.strip().lower()
                            if normalized == "true":
                                return True
                            if normalized == "false":
                                return False
                        raise ValueError("expected True or False")
                except (ValueError, OverflowError) as error:
                    raise ValueError(f"Cannot convert value to {name}: {error}") from None

            if name in self.classes:
                if name not in self.classes:
                    raise NameError(f"Undefined class '{name}'")
                klass = self.classes[name]
                instance = AevyInstance(klass)
                initializer = klass.find_method("init")
                if initializer is not None:
                    owner = klass.find_method_owner("init")
                    self.call_function_declaration(initializer, values, instance, owner)
                elif values:
                    raise TypeError(
                        f"Class '{name}' has no init method and accepts no arguments"
                    )
                return instance
            if name not in self.functions:
                raise NameError(f"Undefined function or class '{name}'")
            return self.call_function_declaration(self.functions[name], values)
        if isinstance(expression.callee, AttributeAccess):
            # give.input(prompt) is Aevy's built-in input syntax. Recognize it
            # before evaluating `give`, which is not a user-defined variable.
            if (
                isinstance(expression.callee.object_expression, Variable)
                and expression.callee.object_expression.name == "give"
                and expression.callee.name == "input"
            ):
                if len(expression.arguments) > 1:
                    raise TypeError(
                        f"Built-in 'give.input' expects 0 or 1 argument, received {len(expression.arguments)}"
                    )
                prompt = "" if not expression.arguments else self.evaluate(expression.arguments[0])
                if not isinstance(prompt, str):
                    raise TypeError("The prompt passed to give.input() must be a string")
                try:
                    return self.input_func(prompt)
                except EOFError:
                    raise RuntimeError("No input was available for give.input()") from None

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
    @staticmethod
    def _list_index(index, length, allow_end=False):
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError("List index must be an integer")
        if index < 0 or index >= length:
            raise IndexError(f"List index {index} is out of range for a list of length {length}")
        return index

    def evaluate(self, expression):
        try:
            return self._evaluate(expression)
        except Exception as error:
            self._attach_location(error, expression)
            raise

    @staticmethod
    def _attach_location(error, node):
        # Preserve the most specific location: an inner expression that raised
        # the error wins over any enclosing statement or expression.
        if not hasattr(error, "aevy_line") and hasattr(node, "line"):
            error.aevy_line = node.line
            error.aevy_column = node.column

    def _evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value
        if isinstance(expression, ListLiteral):
            return [self.evaluate(element) for element in expression.elements]
        if isinstance(expression, IndexAccess):
            target = self.evaluate(expression.object_expression)
            if not isinstance(target, list):
                raise TypeError("Indexing requires a list")
            index = self._list_index(self.evaluate(expression.index), len(target), allow_end=False)
            return target[index]
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
                if expression.name.startswith("_"):
                    owner = instance.private_attribute_owners.get(expression.name)
                    is_self = (
                        isinstance(expression.object_expression, Variable)
                        and expression.object_expression.name == "self"
                    )
                    if not (
                        is_self
                        and self.current_method_owner is not None
                        and self.current_method_owner is owner
                    ):
                        owner_name = owner.name if owner is not None else "unknown"
                        raise PermissionError(
                            f"Private attribute '{expression.name}' of class "
                            f"'{owner_name}' cannot be accessed here"
                        )
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
            if operator == "+":
                if isinstance(left, list) or isinstance(right, list):
                    if isinstance(left, list) and isinstance(right, list):
                        return left + right
                    raise TypeError("List concatenation requires two lists")
                return left + right
            if operator == "-": return left - right
            if operator == "*":
                if isinstance(left, list) or isinstance(right, list):
                    if isinstance(left, list) and isinstance(right, int) and not isinstance(right, bool) and right >= 0:
                        return left * right
                    if isinstance(right, list) and isinstance(left, int) and not isinstance(left, bool) and left >= 0:
                        return right * left
                    raise TypeError("List repetition requires a list and a non-negative integer")
                return left * right
            if operator == "/": return left / right
            if operator == "==": return left == right
            if operator == "!=": return left != right
            if operator == "in":
                if isinstance(right, (list, str)):
                    return left in right
                raise TypeError("Right operand of 'in' must be a list or text")
            if operator == "<": return left < right
            if operator == "<=": return left <= right
            if operator == ">": return left > right
            if operator == ">=": return left >= right
            raise RuntimeError(f"Unknown binary operator: {operator}")
        raise RuntimeError(f"Unsupported expression: {type(expression).__name__}")
