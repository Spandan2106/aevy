
from dataclasses import dataclass


class ASTNode:
    pass


@dataclass
class Literal(ASTNode):
    value: object


@dataclass
class Variable(ASTNode):
    name: str


@dataclass
class BinaryExpression(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryExpression(ASTNode):
    operator: str
    operand: ASTNode


@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode


@dataclass
class ShowStatement(ASTNode):
    value: ASTNode


@dataclass
class ExpressionStatement(ASTNode):
    expression: ASTNode


@dataclass
class Program(ASTNode):
    statements: list


@dataclass
class ElifBranch(ASTNode):
    condition: ASTNode
    statements: list


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_branch: list
    else_branch: list
    elif_branches: list


@dataclass
class ForStatement(ASTNode):
    variable: str
    start: ASTNode
    end: ASTNode
    body: list


@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: list


@dataclass
class BreakStatement(ASTNode):
    pass


@dataclass
class ContinueStatement(ASTNode):
    pass


# Function declaration: func add(a, b) { ... }
@dataclass
class FunctionDeclaration(ASTNode):
    name: str
    parameters: list
    body: list


# Function call: add(10, 20)
@dataclass
class FunctionCall(ASTNode):
    callee: ASTNode
    arguments: list


# Return statement: return expression
@dataclass
class ReturnStatement(ASTNode):
    value: object = None
