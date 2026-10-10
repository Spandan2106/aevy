
from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # Names and literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    TRUE = auto()
    FALSE = auto()

    # Keywords
    FUNC = auto()
    CLASS = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    IN = auto()
    AND = auto()
    OR = auto()
    NOT = auto()

    # Operators
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    COLON = auto()
    DOT = auto()

    # Layout
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: object
    line: int
    column: int

    def __repr__(self):
        return (
            f"Token({self.type.name}, {self.value!r}, "
            f"line={self.line}, column={self.column})"
        )
